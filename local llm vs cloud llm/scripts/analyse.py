import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---

PROMPTS = {
    "P1": {
        "category": "General knowledge",
        "input": "Explain what OSI model is in one paragraph."
    },
    "P2": {
        "category": "Reasoning",
        "input": "If a train leaves at 10, travels 300km at 100kmh, when does it arrive."
    },
    "P3": {
        "category": "Code generation",
        "input": "Generate a Python function that sorts a list using bubble sort."
    },
    "P4": {
        "category": "Context memory",
        "input": "\n        The following is an article about the history of the internet.\n        The internet started as a project by the U.S. Department of Defense called ARPANET. It was designed to be a decentralized network that could withstand a nuclear attack. The first message was sent over ARPANET in 1969. It was from a computer at UCLA to a computer at Stanford. The message was \"lo\". It was supposed to be \"login\", but the system crashed after the first two letters.\n        In the 1980s, the National Science Foundation created a network of supercomputers called NSFNET. This network was much faster than ARPANET and was open to all academic researchers. This was the beginning of the internet as we know it today.\n        In 1991, Tim Berners-Lee created the World Wide Web. This made the internet much more user-friendly and led to its explosive growth.\n        Today, the internet is a global network of computers that connects billions of people. It is used for everything from communication to commerce to entertainment.\n        \n        Question: What was the first message sent over ARPANET?\n        "
    },
    "P5": {
        "category": "Creative writing",
        "input": "Write a short story about a robot discovering emotions."
    }
}

RESULTS_FILE = "./results/results.json"
CHARTS_DIR = "./results/charts"
COMPARISON_FILE = "./results/comparison.md"

def analyze_results():
    """
    Analyzes the benchmark results, generates summary tables and visualizations,
    and creates a side-by-side comparison of model responses.
    """
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at {RESULTS_FILE}")
        return

    with open(RESULTS_FILE, "r") as f:
        results = json.load(f)

    df = pd.DataFrame(results)

    # --- Summary Table ---
    print("--- Benchmark Summary ---")
    
    # Handle potential errors in results
    if 'error' in df.columns:
        df_no_errors = df[df['error'].isnull()].copy()
    else:
        df_no_errors = df.copy()
    
    summary = df_no_errors.pivot_table(
        index='prompt_id',
        columns='model',
        values=['latency_ms', 'tokens_per_second']
    )
    print(summary)

    # --- Visualizations ---
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR)

    # Latency Comparison
    plt.figure(figsize=(10, 6))
    summary['latency_ms'].plot(kind='bar', ax=plt.gca())
    plt.title('Latency Comparison (ms)')
    plt.ylabel('Latency (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "latency_comparison.png"))
    print(f"\nSaved latency comparison chart to {CHARTS_DIR}/latency_comparison.png")

    # Tokens per Second Comparison
    plt.figure(figsize=(10, 6))
    tps_data = df_no_errors[df_no_errors['tokens_per_second'] > 0]
    if not tps_data.empty:
        tps_data.pivot(index='prompt_id', columns='model', values='tokens_per_second').plot(kind='bar', ax=plt.gca())
        plt.title('Tokens per Second Comparison')
        plt.ylabel('Tokens/sec')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CHARTS_DIR, "tokens_per_second_comparison.png"))
        print(f"Saved tokens per second chart to {CHARTS_DIR}/tokens_per_second_comparison.png")

    # --- Side-by-Side Comparison ---
    grouped_results = {}
    for result in results:
        prompt_id = result['prompt_id']
        if prompt_id not in grouped_results:
            grouped_results[prompt_id] = {}
        grouped_results[prompt_id][result['model']] = result.get('response', 'Error: ' + result.get('error', 'Unknown'))

    with open(COMPARISON_FILE, "w") as f:
        f.write("# Model Response Comparison\n\n")
        for prompt_id, prompt_data in PROMPTS.items():
            prompt_text = prompt_data['input']
            category = prompt_data['category']
            gemma_response = grouped_results.get(prompt_id, {}).get('Gemma2', 'Response not found.')
            gemini_response = grouped_results.get(prompt_id, {}).get('Gemini', 'Response not found.')

            # Sanitize for Markdown table
            gemma_response = gemma_response.replace('|', '\\|').replace('\n', '<br>')
            gemini_response = gemini_response.replace('|', '\\|').replace('\n', '<br>')

            f.write(f"### Prompt {prompt_id}: {category}\n")
            f.write(f"**Prompt:** `{prompt_text.strip()}`\n\n")
            f.write("| Gemma2 Response | Gemini Response |\n")
            f.write("| :--- | :--- |\n")
            f.write(f"| {gemma_response} | {gemini_response} |\n\n")
            f.write("---\n\n")
    
    print(f"Saved side-by-side comparison to {COMPARISON_FILE}")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    analyze_results()