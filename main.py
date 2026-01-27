import argparse
import os
from src.audioprocessor import AudioProcessor

def main():
    parser = argparse.ArgumentParser(description="TTS Project Entry Point")
    parser.add_argument("--mode", choices=["process", "check"], default="process")
    parser.add_argument("--target_lufs", type=float, default=23.0)
    # Added path argument to point to any directory
    parser.add_argument("--path", type=str, help="Specify a custom directory to scan or process")
    
    args = parser.parse_args()

    # Determine which directory to use
    if args.path:
        input_dir = args.path
        output_dir = "data/processed" # Default output if processing
    else:
        # Fallback to defaults
        input_dir = "data/processed" if args.mode == "check" else "data/raw"
        output_dir = "data/processed"

    print(f">>> Starting Audio Phase (Mode: {args.mode})")
    print(f">>> Target Directory: {input_dir}")
    
    audio_proc = AudioProcessor(target_i=-abs(args.target_lufs))
    
    audio_proc.run_sequential(
        input_dir=input_dir, 
        output_dir=output_dir, 
        mode=args.mode
    )

    print("\nPipeline complete.")

if __name__ == "__main__":
    main()
