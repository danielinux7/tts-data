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
python src/audio_prep.py --mode process --target 23

```

Processed files will be saved in `data/processed/`.

### Check Mode

To scan and validate audio health for files already in the `data/processed/` folder:

```bash
python src/audio_prep.py --mode check

```

## 🔬 Understanding the Output

The script monitors the **Crest Factor**, which is the difference between the **True Peak** and the **Integrated Loudness (LUFS)**.

| Metric | Ideal Range | Description |
| --- | --- | --- |
| **Loudness** | -23.0 LUFS | The average perceived loudness of the clip. |
| **Peak** | -6.0 dBFS | The highest point of the waveform. |
| **Crest Factor** | 12.0 - 18.0 dB | Indicates the dynamic range. Values below 12.0 are highlighted as "too compressed." |
