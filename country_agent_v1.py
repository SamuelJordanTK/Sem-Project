import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(" Country Analysis Agent - Version 1")
print("Testing basic AI components...")

# Test CSV loading
try:
    population_df = pd.read_csv('data/population.csv')
    print(" CSV loaded successfully")
    print("Sample data:")
    print(population_df.head())
except Exception as e:
    print(f" CSV error: {e}")
    exit()

# Test basic AI imports
try:
    from llama_index.llms import OpenAI
    from llama_index.query_engine import PandasQueryEngine
    
    # Initialize LLM
    llm = OpenAI(model="gpt-3.5-turbo-0613")
    print(" OpenAI LLM initialized")
    
    # Create simple query engine
    query_engine = PandasQueryEngine(df=population_df, verbose=True)
    print(" Pandas query engine created")
    
    # Test a simple query
    test_query = "What is the total population?"
    print(f"\nTesting query: {test_query}")
    result = query_engine.query(test_query)
    print(f"Result: {result}")
    
except Exception as e:
    print(f" AI components error: {e}")
    exit()

print("\n Basic AI components working! Ready for next step.")