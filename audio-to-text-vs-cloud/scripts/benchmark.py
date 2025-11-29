import os
import json
import time
import whisper
import pandas as pd
from tqdm import tqdm

# Define paths
AUDIO_SAMPLES_DIR = "audio_samples"
RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.json")

# Create results directory if it doesn't exist
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_audio_files():
    """Get a list of audio files from the audio_samples directory."""
    if not os.path.exists(AUDIO_SAMPLES_DIR):
        print(f"Error: The directory '{AUDIO_SAMPLES_DIR}' does not exist.")
        print("Please create it and add some audio files to transcribe.")
        return []
    
    files = [f for f in os.listdir(AUDIO_SAMPLES_DIR) if os.path.isfile(os.path.join(AUDIO_SAMPLES_DIR, f))]
    if not files:
        print(f"No audio files found in '{AUDIO_SAMPLES_DIR}'.")
        print("Please add some audio files to transcribe.")
    return files

def benchmark_local_whisper(audio_files):
    """Benchmark the local Whisper model."""
    print("Loading Whisper model...")
    # Using the 'base' model for a balance of speed and accuracy.
    # Other options: 'tiny', 'small', 'medium', 'large'
    model = whisper.load_model("base")
    print("Whisper model loaded.")

    results = []
    
    print("Starting local Whisper benchmark...")
    for audio_file in tqdm(audio_files, desc="Transcribing audio files"):
        audio_path = os.path.join(AUDIO_SAMPLES_DIR, audio_file)
        
        start_time = time.time()
        try:
            result = model.transcribe(audio_path)
            end_time = time.time()
            
            duration = end_time - start_time
            
            results.append({
                "model": "local_whisper_base",
                "file": audio_file,
                "transcription": result["text"],
                "duration_seconds": duration
            })
        except Exception as e:
            print(f"Error transcribing {audio_file}: {e}")
            results.append({
                "model": "local_whisper_base",
                "file": audio_file,
                "transcription": "Error",
                "duration_seconds": -1,
                "error": str(e)
            })

    return results

if __name__ == "__main__":
    audio_files = get_audio_files()
    
    if audio_files:
        local_results = benchmark_local_whisper(audio_files)
        
        # Save results to JSON
        with open(RESULTS_FILE, "w") as f:
            json.dump(local_results, f, indent=4)
            
        print(f"Benchmark complete. Results saved to {RESULTS_FILE}")

        # Optional: Print results as a table
        df = pd.DataFrame(local_results)
        print("\n--- Benchmark Results ---")
        print(df.to_string())
        print("-----------------------\n")

