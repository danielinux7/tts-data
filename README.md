# TTS Data Prep Pipeline

A Python-based utility for preparing high-quality audio datasets for Text-to-Speech (TTS) model training. This tool automates denoising, EBU R128 loudness normalization, and audio health validation.

## 📁 Project Structure

```text
github-tts-project/
├── venv/                 # Virtual environment (ignored by git)
├── data/
│   ├── raw/              # Your initial audiobook/recordings
│   └── processed/        # Output from the script
├── src/
│   └── audio_prep.py     # Core processing script
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation

```

## 🚀 Features

* **Denoising:** Uses the `afftdn` FFT-based denoiser to clean background floor noise.
* **Loudness Normalization:** Targets specific LUFS (default -23) using the `loudnorm` filter for consistency.
* **Crest Factor Validation:** Automatically calculates the Peak-to-Loudness ratio to ensure audio is not over-compressed.
* **Format Standardization:** Outputs mono, 24-bit PCM WAV files at 22050Hz (industry standard for TTS).
* **Metadata Phase:** Converts XLSX/CSV spreadsheets into the pipe-delimited (`|`) format used by industry trainers like Coqui, Piper, and ESPnet.

## 🛠️ Installation

1. **System Requirements:**
Ensure you have **FFmpeg** installed on your system.
```bash
# Ubuntu/Debian
sudo apt install ffmpeg
# macOS
brew install ffmpeg

```


2. **Setup:**
```bash
git clone https://github.com/your-username/github-tts-project.git
cd github-tts-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```



## 📈 Usage

### Processing Mode

Place your raw `.wav` files in `data/raw/` and run:

```bash
python3 -m main --mode process --target_lufs 23

```

Processed files will be saved in `data/processed/`.

### Checking mode
You can point the tool at any directory to audit audio health:
```bash
python3 -m main --mode check --path data/raw --target_dbfs 23

```

### 2. Metadata mode

Align your transcripts from a spreadsheet:

```bash
python main.py --mode metadata --spreadsheet metadata/metadata.xlsx

```

## 🔬 Understanding the Output

The script monitors the **Crest Factor**, which is the difference between the **True Peak** and the **Integrated Loudness (LUFS)**, and **Loudness Range** to ensure the audio maintains the quality necessary for natural-sounding TTS.

| Metric | Ideal Range | Description |
| --- | --- | --- |
| **Loudness** | -23.0 dBFS | The average perceived volume. |
| **Peak** | -6.0 dBFS | The maximum amplitude limit. |
| **Range (LRA)** | 3.0 - 7.0 dB | The statistical distribution of loudness. Lower is more consistent for training. |
| **Crest Factor** | 12.0 - 18.0 dB | Indicates dynamic range; < 12.0 suggests the audio is too compressed/squashed. |
