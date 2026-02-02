import os
import subprocess
import re

class AudioProcessor:
    def __init__(self, target_i=-23.0, peak_limit=-6.0):
        self.target_i = target_i
        self.peak_limit = peak_limit
        self.target_sr = 22050

    def get_duration(self, file_path):
        """Extracts the duration of the audio file in seconds using ffprobe."""
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return float(result.stdout.strip())
        except (ValueError, TypeError):
            return 0.0

    def format_time(self, seconds):
        """Converts seconds into MM:SS format."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def get_ebur128_stats(self, file_path):
        """Extracts Loudness (I), Peak (TP), and Range (LRA) using FFmpeg."""
        cmd = ["ffmpeg", "-i", file_path, "-filter:a", "ebur128=peak=true", "-f", "null", "-"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stderr
        try:
            i = re.findall(r"I:\s+([\d.-]+)\s+LUFS", output)[-1]
            tp = re.findall(r"Peak:\s+([\d.-]+)\s+dBFS", output)[-1]
            lra = re.findall(r"LRA:\s+([\d.-]+)\s+LU", output)[-1]
            return float(i), float(tp), float(lra)
        except (IndexError, ValueError):
            return 0.0, 0.0, 0.0

    def process_file(self, in_p, out_p):
        """Applies denoiser and normalization filters."""
        filter_chain = f"afftdn=nr=12:nf=-30, loudnorm=I={self.target_i}:TP={self.peak_limit}:LRA=7"
        cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", in_p, 
               "-af", filter_chain, "-c:a", "pcm_s24le", "-ac", "1", "-ar", str(self.target_sr), out_p]
        subprocess.run(cmd)

    def run_sequential(self, input_dir, output_dir, mode="process"):
        """Runs the audio pipeline and displays a summary of averages."""
        os.makedirs(output_dir, exist_ok=True)
        search_dir = input_dir 

        if not os.path.exists(search_dir):
            print(f"Error: Directory '{search_dir}' not found.")
            return

        print(f"{'Filename':<25} | {'Length':<8} | {'Loudness':<10} | {'Peak':<10} | {'Range':<10} | {'Crest':<10}")
        print("-" * 95)

        total_i = 0; total_tp = 0; total_lra = 0; total_cf = 0; total_duration = 0; count = 0
        reset = "\033[0m"

        for f in sorted(os.listdir(search_dir)):
            if not f.lower().endswith(".wav"): continue
            
            in_file = os.path.join(search_dir, f)
            out_file = os.path.join(output_dir, f)

            if mode != "check":
                self.process_file(in_file, out_file)
                measure_file = out_file
            else:
                measure_file = in_file

            duration = self.get_duration(measure_file)
            i, tp, lra = self.get_ebur128_stats(measure_file)
            crest = abs(tp - i)
            
            total_i += i; total_tp += tp; total_lra += lra; total_cf += crest; total_duration += duration; count += 1

            i_color = "\033[93m" if abs(i - self.target_i) > 1.0 else "\033[92m"
            tp_color = "\033[93m" if tp > self.peak_limit else "\033[92m"
            lra_color = "\033[92m" if 3.0 <= lra <= 7.0 else "\033[93m"
            cf_color = "\033[92m" if crest >= 12 else "\033[93m"

            print(f"{f[:24]:<25} | "
                  f"{self.format_time(duration):<8} | "
                  f"{i_color}{i:>7.1f} dB{reset} | "
                  f"{tp_color}{tp:>7.1f} dB{reset} | "
                  f"{lra_color}{lra:>7.1f} dB{reset} | "
                  f"{cf_color}{crest:>7.2f} dB{reset}")

        # --- SUMMARY BLOCK ---
        if count > 0:
            avg_i = total_i / count
            avg_tp = total_tp / count
            avg_lra = total_lra / count
            avg_cf = total_cf / count
            avg_duration = total_duration / count # Calculation for Average Length

            print("-" * 95)
            print(f"SUMMARY FOR {count} FILES:")
            print(f"Total Duration:   {self.format_time(total_duration)}")
            print(f"Average Length:   {self.format_time(avg_duration)}") # Added to Summary
            print(f"Average Loudness: {avg_i:>7.2f} dBFS")
            print(f"Average Peak:     {avg_tp:>7.2f} dBFS")
            print(f"Average Range:    {avg_lra:>7.2f} dB")
            print(f"Average Crest:    {avg_cf:>7.2f} dB (Healthy range for speech: 12-18 dB)")
            print("-" * 95)