
import json
import time
import os
# It is recommended to install the following dependencies:
# pip install google-generativeai ollama
import ollama
import google.generativeai as genai

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
        "input": """
        The following is an article about the history of the internet.
        The internet started as a project by the U.S. Department of Defense called ARPANET. It was designed to be a decentralized network that could withstand a nuclear attack. The first message was sent over ARPANET in 1969. It was from a computer at UCLA to a computer at Stanford. The message was \"lo\". It was supposed to be \"login\", but the system crashed after the first two letters.
        In the 1980s, the National Science Foundation created a network of supercomputers called NSFNET. This network was much faster than ARPANET and was open to all academic researchers. This was the beginning of the internet as we know it today.
        In 1991, Tim Berners-Lee created the World Wide Web. This made the internet much more user-friendly and led to its explosive growth.
        Today, the internet is a global network of computers that connects billions of people. It is used for everything from communication to commerce to entertainment.
        
        Question: What was the first message sent over ARPANET?
        """
    },
    "P5": {
        "category": "Creative writing",
        "input": "Write a short story about a robot discovering emotions."
    }
}

RESULTS_DIR = "results"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# --- Model Interfaces ---

def run_gemma_test(prompt_id, prompt):
    """
    Runs a test on the local Gemma 2 model using Ollama.
    """
    start_time = time.time()
    
    try:
        # Assuming Ollama is running and has the "gemma3:4b" model
        response = ollama.chat(model='gemma3:4b', messages=[{'role': 'user', 'content': prompt}])
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Extracting metrics
        tokens_per_second = response.get('eval_count', 0) / response.get('eval_duration', 1) * 1_000_000_000
        
        result = {
            "model": "Gemma3 (4B)",
            "prompt_id": prompt_id,
            "latency_ms": latency_ms,
            "tokens_per_second": tokens_per_second,
            "quality_score": -1,  # Manual rating needed
            "offline_capable": True,
            "cost": 0,
            "response" : response['message']['content'],
            "notes": f"Tokens: {response.get('eval_count')}"
        }
        return result

    except Exception as e:
        return {
            "model": "Gemma3 (4B)",
            "prompt_id": prompt_id,
            "error": str(e)
        }

def run_gemini_test(prompt_id, prompt):
    """
    Runs a test on the Gemini API.
    """
    if not GEMINI_API_KEY:
        return {
            "model": "Gemini",
            "prompt_id": prompt_id,
            "error": "GEMINI_API_KEY environment variable not set."
        }

    start_time = time.time()
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        response = model.generate_content(prompt)
        latency_ms = (time.time() - start_time) * 1000
        
        # Gemini API does not provide token speed directly. 
        # This is a placeholder; a more accurate measurement might involve counting tokens in the response.
        
        result = {
            "model": "Gemini",
            "prompt_id": prompt_id,
            "latency_ms": latency_ms,
            "tokens_per_second": -1, # Not directly available
            "quality_score": -1,  # Manual rating needed
            "offline_capable": False,
            "cost": -1,  # Placeholder for cost calculation
            "response" : response.text,
            "notes": ""
        }
        return result

    except Exception as e:
        return {
            "model": "Gemini",
            "prompt_id": prompt_id,
            "error": str(e)
        }

# --- Test Runner ---

def main():
    """
    Main function to run the benchmark tests.
    """
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    results = []

    print("Running tests on Gemma 3 (4B Local)...\n")
    for prompt_id, prompt_data in PROMPTS.items():
        print(f"  Running prompt: {prompt_id} ({prompt_data['category']})")
        result = run_gemma_test(prompt_id, prompt_data['input'])
        results.append(result)
        print(f"  Result: {result}")


    print("\nRunning tests on Gemini (Cloud)...\n")
    for prompt_id, prompt_data in PROMPTS.items():
        print(f"  Running prompt: {prompt_id} ({prompt_data['category']})")
        result = run_gemini_test(prompt_id, prompt_data['input'])
        results.append(result)

    # Save results
    results_path = os.path.join(RESULTS_DIR, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nTests complete. Results saved to {results_path}")

if __name__ == "__main__":
    main()
