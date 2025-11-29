import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Define paths
RESULTS_DIR = "results"
CHARTS_DIR = os.path.join(RESULTS_DIR, "charts")
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")
COMPARISON_MD = os.path.join(RESULTS_DIR, "comparison.md")

def analyze_results():
    """Analyze the benchmark results and generate a report."""
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at '{RESULTS_FILE}'")
        print("Please run the benchmark first.")
        return

    with open(RESULTS_FILE, "r") as f:
        results_data = json.load(f)
    
    df = pd.DataFrame(results_data)

    if df.empty:
        print("No results to analyze.")
        return
        
    # --- Generate Markdown Report ---
    with open(COMPARISON_MD, "w") as f:
        f.write("# Audio-to-Text Benchmark Analysis\n\n")
        f.write("This report summarizes the performance of the audio-to-text models.\n\n")
        f.write("## Transcription Durations\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n")

    print(f"Markdown report saved to {COMPARISON_MD}")

    # --- Generate Chart ---
    plt.figure(figsize=(10, 6))
    
    # Bar chart for duration
    bars = plt.bar(df['file'], df['duration_seconds'], color='skyblue')
    plt.ylabel('Duration (seconds)')
    plt.xlabel('Audio File')
    plt.title('Transcription Duration per Audio File')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}s', va='bottom', ha='center')


    latency_chart_path = os.path.join(CHARTS_DIR, 'latency_comparison.png')
    plt.savefig(latency_chart_path)
    print(f"Latency comparison chart saved to {latency_chart_path}")
    plt.close()


if __name__ == "__main__":
    analyze_results()
