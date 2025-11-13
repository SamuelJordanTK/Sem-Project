import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Simple version without complex imports
print(" Simple Country Agent")
print("This is a basic version to test your setup")

# Test CSV loading
try:
    df = pd.read_csv('data/population.csv')
    print(" CSV loaded successfully")
    print(df.head())
except Exception as e:
    print(f" CSV error: {e}")

print("\nSetup complete! Now we can add the AI components.")