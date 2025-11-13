import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from prompts import instruction_str, context  # Remove new_prompt_template from imports
from note_engine import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import india_engine

# Verify API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file")
os.environ["OPENAI_API_KEY"] = api_key

# Load your existing population CSV
population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

from llama_index.query_engine import PandasQueryEngine
population_query_engine = PandasQueryEngine(
    df=population_df,
    verbose=True,
    instruction_str=instruction_str
)
# REMOVE THIS LINE: population_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Define tools with enhanced descriptions
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="world_population_data",
            description="This provides comprehensive world population statistics, demographics, country comparisons, and global trends. Use this for comparing countries, analyzing population growth, and understanding demographic patterns."
        ),
    ),
    QueryEngineTool(
        query_engine=india_engine,
        metadata=ToolMetadata(
            name="india_detailed_info",
            description="This provides detailed information about India including culture, economy, geography, history, and society. Use this for specific facts about India, its development, and unique characteristics."
        ),
    ),
]

# Create agent with updated context
llm = OpenAI(model="gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

print("🌍 Country Analysis Agent Ready!")
print("I can help you analyze countries, compare demographics, and learn about India!")
print("Available capabilities:")
print("- Compare India with other countries")
print("- Analyze population trends")
print("- Get detailed information about India")
print("- Save interesting facts as notes")
print("Type 'q' to quit.\n")

# Enhanced main loop with suggestions
while (prompt := input("Ask about countries or demographics: ")) != "q":
    if prompt.lower() in ['help', 'examples', '?']:
        print("\nTry these questions:")
        print("- How does India's population compare to China?")
        print("- What are the key facts about India's economy?")
        print("- Which countries have the highest population growth?")
        print("- Save a note about India's cultural heritage")
        print("- Compare population density across Asian countries")
        continue
    
    result = agent.query(prompt)
    print(f"🌍: {result}\n")