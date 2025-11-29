# Edge AI vs. Cloud AI Comparison

This repository contains a suite of tests to compare the performance of a local AI model (Gemma 2) against a cloud-based AI model (Gemini).

## Structure

- `/scripts`: Contains the Python scripts for running the benchmark tests.
- `/results`: Stores the output of the tests, including raw logs, CSV files, and generated charts.
- `instructions.md`: The detailed test plan.

## Quick Start

Get started with the Edge AI vs. Cloud AI benchmark in three simple steps:

1.  **Set Your Gemini API Key:** Create a `.env` file in the project root with `GEMINI_API_KEY="YOUR_GEMINI_API_KEY"`.

2.  **Run the Benchmark:** Execute `docker-compose up` in your terminal. This will build the environment, set up Gemma 2, and run the tests.

3.  **Analyze Results:** After the benchmark completes, run `docker-compose run --rm benchmark python scripts/analyse.py` to generate summary charts and tables.

---

## Usage

This project is designed to be "plug and play" using Docker and Docker Compose.

### 1. Prerequisites

- **Docker:** Must be installed and running.
- **Gemini API Key:** You need a Gemini API key to run the cloud-based tests.

### 2. Running the Benchmark (Recommended Method)

1.  **Set Your API Key:**
    Create a `.env` file in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    Replace `YOUR_GEMINI_API_KEY` with your actual key.

2.  **Run with Docker Compose:**
    Open your terminal and run:
    ```bash
    docker-compose up
    ```
    This single command will:
    - Build the Docker image.
    - Install Ollama and pull the Gemma 2 model inside the container.
    - Run the benchmark script (`scripts/benchmark.py`).

    The results will be saved to the `results/` directory on your host machine.

### Optional: Running with a GPU

If you have an NVIDIA GPU and the [NVIDIA Container Toolkit](https.docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed, you can accelerate the local model's performance.

To enable GPU support:

1.  **Uncomment the `deploy` section in the `docker-compose.yaml` file:**

    ```yaml
    services:
      benchmark:
        build: .
        volumes:
          - ./results:/app/results
        environment:
          - GEMINI_API_KEY=${GEMINI_API_KEY}
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]
    ```

2.  **Run Docker Compose as usual:**
    ```bash
    docker-compose up
    ```

    Ollama will automatically detect and use the GPU inside the container.


### 3. Analyzing the Results

After the benchmark is complete, you can analyze the results.

1.  **Run the analysis script using Docker Compose:**
    ```bash
    docker-compose run --rm benchmark python scripts/analyse.py
    ```
    This will execute the `analyse.py` script within the container, which reads the `results.json` file and generates summary tables and charts in the `results/charts` directory.

### 4. Cleanup

To remove all Docker-related artifacts (containers, images, volumes) and local files such as the `results` directory and `.env` file, run the `cleanup.sh` script:

```bash
./cleanup.sh
```




