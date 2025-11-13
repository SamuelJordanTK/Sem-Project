import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(" Country Analysis Agent - Version 3")
print("Adding note engine...")

# Load CSV
population_df = pd.read_csv('data/population.csv')
print(" CSV loaded")

# Create note engine
def save_note(note):
    note_file = os.path.join("data", "notes.txt")
    if not os.path.exists(note_file):
        open(note_file, "w")
    
    with open(note_file, "a") as f:
        f.writelines([note + "\n"])
    
    return "note saved"

print(" Note function defined")

# Test note function
try:
    result = save_note("Test note from Country Agent")
    print(f" Note function test: {result}")
except Exception as e:
    print(f" Note function error: {e}")

print("\n Note engine working! Ready for final version.")