# Audio-to-Text: Local vs. Cloud Benchmark

This project benchmarks a local Whisper model for audio-to-text transcription and compares the results against a fixed set of sample cloud performance data.

It is set up to be run inside a Docker container for portability.

## How to Run

1.  **Add Audio Samples:**
    Place the audio files you want to transcribe into the `audio_samples` directory. The analysis will only compare files that have a matching entry in the `results/cloud_results.json` file.

2.  **Build and Run with Docker:**
    From the `audio-to-text-vs-cloud` directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image, run the local benchmark, and then generate a comparison report.

## How it Works

1.  **`benchmark.py`:**
    - This script runs a benchmark on your local machine using the open-source `openai-whisper` library (`base` model).
    - It saves the transcription and performance results to `results/local_results.json`.

2.  **`analyse.py`:**
    - This script reads both `results/local_results.json` (from your benchmark) and `results/cloud_results.json` (a static file with example cloud performance).
    - It combines the data and generates a comparative markdown report (`comparison.md`) and a grouped bar chart (`latency_comparison.png`) to visualize the performance difference.

## Project Structure
```
.
├── Dockerfile
├── docker-compose.yaml
├── entrypoint.sh
├── requirements.txt
├── audio_samples/
│   └── (your audio files here)
├── results/
│   ├── charts/
│   │   └── latency_comparison.png
│   ├── comparison.md
│   ├── local_results.json
│   └── cloud_results.json (Static Data)
└── scripts/
    ├── analyse.py
    └── benchmark.py
```