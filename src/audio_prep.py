import os
import subprocess
import re
import argparse

class AudioProcessor:
    def __init__(self, target_i=-23.0, peak_limit=-6.0):
        self.target_i = target_i
        self.peak_limit = peak_limit

    def get_ebur128_stats(self, file_path):
        """Extracts Loudness (I), Peak (TP), and LRA using FFmpeg."""
        cmd = ["ffmpeg", "-i", file_path, "-filter:a", "ebur128=peak=true", "-f", "null", "-"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stderr
        try:
            i = re.findall(r"I:\s+([\d.-]+)\s+LUFS", output)[-1]
            tp = re.findall(r"Peak:\s+([\d.-]+)\s+dBFS", output)[-1]
            return float(i), float(tp)
        except (IndexError, ValueError):
            return 0.0, 0.0

    def process(self, in_p, out_p):
        """Denoise and Normalize audio for TTS training."""
        filter_chain = f"afftdn=nr=12:nf=-30, loudnorm=I={self.target_i}:TP={self.peak_limit}:LRA=7"
        cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", in_p, 
               "-af", filter_chain, "-c:a", "pcm_s24le", "-ac", "1", "-ar", "22050", out_p]
        subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="TTS Data Prep Tool")
    parser.add_argument("--mode", choices=["process", "check"], default="process")
    args = parser.parse_args()

    proc = AudioProcessor()
    search_dir = "processed" if args.mode == "check" else "."
    os.makedirs("processed", exist_ok=True)

    print(f"{'File':<25} | {'Loudness':<10} | {'Peak':<10} | {'Crest':<10}")
    print("-" * 65)

    for f in os.listdir(search_dir):
        if not f.lower().endswith(".wav"): continue
        in_file = os.path.join(search_dir, f)
        out_file = os.path.join("processed", f)

        if args.mode != "check":
            proc.process(in_file, out_file)
            measure_file = out_file
        else:
            measure_file = in_file

        i, tp = proc.get_ebur128_stats(measure_file)
        crest = abs(tp - i)
        color = "\033[92m" if crest >= 12 else "\033[93m"
        print(f"{f[:24]:<25} | {i:>7} dB | {tp:>7} dB | {color}{crest:>7.2f} dB\033[0m")

if __name__ == "__main__":
    main()
