# Audio-to-Text: Local vs. Cloud Benchmark

This project provides a framework for benchmarking local and cloud-based audio-to-text (ASR) models. It is set up to be run inside a Docker container for portability.

## How to Run

1.  **Add Audio Samples:**
    Place the audio files you want to transcribe into the `audio_samples` directory.

2.  **Build and Run with Docker:**
    From the `audio-to-text-vs-cloud` directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image, install the dependencies, and run the benchmark and analysis scripts.

## How it Works

1.  **`benchmark.py`:**
    - This script uses the `openai-whisper` library to transcribe the audio files in the `audio_samples` directory.
    - It measures the time taken for each transcription.
    - The results (filename, transcription, and duration) are saved to `results/results.json`.
    - Currently, it uses the `base` Whisper model. You can change this in the script.

2.  **`analyse.py`:**
    - This script reads the `results.json` file.
    - It generates a markdown report named `comparison.md` in the `results` directory.
    - It also creates a bar chart (`latency_comparison.png`) in the `results/charts` directory, visualizing the transcription durations.

## Project Structure
```
.
├── Dockerfile
├── docker-compose.yaml
├── entrypoint.sh
├── requirements.txt
├── audio_samples/
│   └── (your audio files here, e.g., Test .m4a)
├── results/
│   ├── charts/
│   │   └── latency_comparison.png
│   ├── comparison.md
│   └── results.json
└── scripts/
    ├── analyse.py
    └── benchmark.py
```