import argparse
import os
from src.audioprocessor import AudioProcessor
from src.textprocessor import TextProcessor

def main():
    parser = argparse.ArgumentParser(description="TTS Project Entry Point")
    # Added 'metadata' as a valid mode
    parser.add_argument("--mode", choices=["process", "check", "metadata", "all"], default="all")
    parser.add_argument("--target_dbfs", type=float, default=23.0)
    parser.add_argument("--path_in", type=str, help="Custom directory for raw audio scans")
    parser.add_argument("--path_out", type=str, help="Custom directory for processed audio scans")
    parser.add_argument("--spreadsheet", type=str, help="Path to your transcript spreadsheet (xlsx/csv)", default="data/raw/metadata.xlsx")
    parser.add_argument("--use_ipa", action='store_true', help="Transcript IPA instead of text")

    args = parser.parse_args()

    # --- MODE 1 & 2: AUDIO PROCESSING & CHECKING ---
    if args.mode in ["process", "check"]:
        input_dir = args.path_in if args.path_in else "data/raw"
        output_dir = args.path_out if args.path_out else "data/processed"

        print(f">>> Starting Audio Phase (Mode: {args.mode})")
        audio_proc = AudioProcessor(target_i=-abs(args.target_dbfs))
        audio_proc.run_sequential(input_dir, output_dir, mode=args.mode)

    # --- MODE 3: METADATA GENERATION ---
    elif args.mode == "metadata":
        output_dir = args.path_out if args.path_out else "data/processed"
        print(f"\n>>> Starting Metadata Phase using: {args.spreadsheet}")
        tm = TextProcessor(args.spreadsheet, args.use_ipa)
        tm.create_tts_metadata(output_dir)

    # --- MODE 4: END TO END ---
    elif args.mode == "all":
        input_dir = args.path_in if args.path_in else "data/raw"
        output_dir = args.path_out if args.path_out else "data/processed"

        print(f">>> Starting Audio Phase (Mode: process)")
        audio_proc = AudioProcessor(target_i=-abs(args.target_dbfs))
        audio_proc.run_sequential(input_dir, output_dir, mode=args.mode)

        print(f"\n>>> Starting Metadata Phase using: {args.spreadsheet}")
        tm = TextProcessor(args.spreadsheet, args.use_ipa)
        tm.create_tts_metadata(output_dir)

    print("\nPipeline execution finished.")

if __name__ == "__main__":
    main()
