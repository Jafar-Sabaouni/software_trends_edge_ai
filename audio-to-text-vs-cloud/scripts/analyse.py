import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define paths
RESULTS_DIR = "results"
CHARTS_DIR = os.path.join(RESULTS_DIR, "charts")
LOCAL_RESULTS_FILE = os.path.join(RESULTS_DIR, "local_results.json")
CLOUD_RESULTS_FILE = os.path.join(RESULTS_DIR, "cloud_results.json") # Static data
COMPARISON_MD = os.path.join(RESULTS_DIR, "comparison.md")

def analyze_results():
    """Analyze the benchmark results and generate a report."""
    if not os.path.exists(LOCAL_RESULTS_FILE):
        print(f"Error: Local results file not found at '{LOCAL_RESULTS_FILE}'")
        print("Please run the benchmark first.")
        return

    # Load local results
    with open(LOCAL_RESULTS_FILE, "r") as f:
        local_data = json.load(f)

    # Load static cloud results
    if os.path.exists(CLOUD_RESULTS_FILE):
        with open(CLOUD_RESULTS_FILE, "r") as f:
            cloud_data = json.load(f)
    else:
        print(f"Warning: Static cloud results file not found at '{CLOUD_RESULTS_FILE}'.")
        cloud_data = []

    # Combine results
    all_results = local_data + cloud_data
    
    if not all_results:
        print("No results to analyze.")
        return
        
    df = pd.DataFrame(all_results)
    
    # Match local files with cloud files for a clean comparison
    local_files = set(d['file'] for d in local_data)
    df = df[df['file'].isin(local_files)]

    # --- Generate Markdown Report ---
    with open(COMPARISON_MD, "w") as f:
        f.write("# Audio-to-Text Benchmark Analysis\n\n")
        f.write("This report summarizes the performance of a local Whisper model compared to estimated cloud performance.\n\n")
        f.write("### Note on Cloud Data\n")
        f.write("The 'Cloud' data presented in this report is **estimated** and derived from static, pre-computed values found in `results/cloud_results.json`. This approach was adopted because free-tier cloud transcription APIs proved unreliable for consistent benchmarking. As such, the cloud performance metrics do not reflect real-time API calls but rather serve as a theoretical benchmark based on expected performance.\n\n")
        f.write("### Cloud Estimation Formula\n")
        f.write("The estimation for cloud transcription time (T) is calculated using the following formula:\n")
        f.write("```\n")
        f.write("T = D * RTF + L\n")
        f.write("```\n")
        f.write("Where:\n")
        f.write("- `D` is the audio length in seconds.\n")
        f.write("- `RTF` is the Real-Time Factor. (e.g., 0.1 means 10 seconds of audio are processed in 1 second).\n")
        f.write("- `L` is extra latency, including upload time and network delays, in seconds.\n\n")
        f.write("#### How to get values:\n")
        f.write("- **Real-Time Factor (RTF):** Based on benchmarks from Whisper API tests and community data, Whisper Large on a GPU typically achieves an RTF around `0.1` (processing 10 seconds of audio in 1 second).\n")
        f.write("- **Latency (L):** Based on average API round-trip and upload delays reported by developers testing Whisper in cloud setups, this is typically around `1 to 3` seconds.\n\n")
        f.write("#### Example:\n")
        f.write("For a 120-second audio file (D = 120):\n")
        f.write("```\n")
        f.write("RTF = 0.1\n")
        f.write("L = 2 seconds (average)\n\n")
        f.write("T = 120 * 0.1 + 2\n")
        f.write("T = 12 + 2\n")
        f.write("T = 14 seconds\n")
        f.write("```\n")
        f.write("This estimation is not perfect but provides a good basis for planning or rough scaling estimates.\n\n")
        
        # Pivot table for easier comparison
        pivot_df = df.pivot_table(index='file', columns='model', values='duration_seconds')
        
        f.write("## Latency Comparison (in seconds)\n\n")
        f.write(pivot_df.to_markdown())
        f.write("\n\n")

        f.write("## Full Results\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n")

    print(f"Markdown report saved to {COMPARISON_MD}")
