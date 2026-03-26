---

# 🎙️ Abkhazian TTS Dataset (Pilot Version)

Welcome to the pilot release of the Abkhazian Text-to-Speech dataset. This repository contains high-quality, processed speech samples designed for training and evaluating TTS models.

## 📂 Dataset Structure

The dataset is organized into the following components:

* **/wavs/**: A directory containing all raw and processed audio files.
* **metadata.csv**: The primary mapping file for training.
* **audio_analysis.xlsx**: Detailed statistical insights into the audio distribution.

---

## 📝 Metadata Format

The `metadata.csv` file follows a standard pipe-delimited format compatible with most TTS frameworks (like Coqui or ESPnet):

`[File_Name].wav|[Abkhazian_Sentence]`

> **Example:** > `sample_001.wav|Аибабара аус ауеит.`

---

## 🛠️ Audio Processing Pipeline

To ensure consistency and model stability, all audio files have undergone a two-stage digital signal processing (DSP) workflow:

1. **Noise Reduction**: Advanced filtering to minimize ambient floor noise while preserving vocal clarity.
2. **Loudness Normalization**: Standardized gain levels to prevent clipping and ensure uniform volume across the entire corpus.

---

## ⚙️ Technical Specifications

These settings are optimized for high-fidelity speech synthesis while maintaining manageable file sizes.

| Feature | Specification |
| --- | --- |
| **Channels** | Mono (Single Channel) |
| **Bit Depth** | 24-bit PCM |
| **Sample Rate** | 22.05 kHz |
| **Format** | .wav |

---

## ⚖️ Usage & Licensing

This dataset is dedicated to the Public Domain under Creative Commons 1.0 Universal (CC0 1.0).

You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission. While not legally required, a link to this repository or a mention of the project is greatly appreciated by the creators to help track the impact of this data on Abkhazian language technology.

---
