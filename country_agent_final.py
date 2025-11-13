import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(" Smart Country Analysis Agent")
print("Loading data with correct column names...")

# Load your data
df = pd.read_csv('data/population.csv')
print(f" Loaded data for {len(df)} countries")
print("Available columns:", df.columns.tolist())

# Use your actual column names
country_column = 'Country'
population_column = 'Population2023'

print(f"Using '{country_column}' as country column")
print(f"Using '{population_column}' as population column")

def smart_country_analysis(question):
    """Use OpenAI to analyze country data intelligently"""
    import openai
    
    # Get sample data with the actual column names
    sample_data = df[[country_column, population_column, 'YearlyChange', 'WorldShare']].head(8).to_string()
    
    # Create a prompt that includes our data context
    prompt = f"""
    You are a country analysis expert. Use the provided dataset to answer questions.

    DATASET INFORMATION:
    - Contains {len(df)} countries
    - Columns available: {', '.join(df.columns.tolist())}
    
    SAMPLE DATA (first 8 rows):
    {sample_data}

    USER QUESTION: {question}

    INSTRUCTIONS:
    1. If the question is about country populations, growth rates, rankings, or world share - use the exact data from the dataset
    2. For specific countries, look up their data in the sample above or mention we have data for 234 countries
    3. For general knowledge questions (capitals, culture, etc.), provide helpful information but note it's general knowledge
    4. Be precise and data-driven when using the dataset

    ANSWER:
    """
    
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise country data analyst who uses datasets accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error analyzing question: {str(e)}"

def quick_data_lookup(question):
    """Quick lookup for common population questions"""
    question_lower = question.lower()
    
    # Check if asking about a specific country's population
    for country in df[country_column].dropna():
        if country.lower() in question_lower and any(word in question_lower for word in ['population', 'populate', 'people']):
            country_data = df[df[country_column].str.lower() == country.lower()]
            if not country_data.empty:
                pop = country_data[population_column].iloc[0]
                yearly_change = country_data['YearlyChange'].iloc[0]
                world_share = country_data['WorldShare'].iloc[0]
                return f"{country}: Population = {pop:,} (Change: {yearly_change}, World Share: {world_share})"
    
    # Check for top countries
    if 'top' in question_lower or 'highest' in question_lower:
        if 'population' in question_lower:
            top_countries = df.nlargest(3, population_column)[[country_column, population_column]]
            result = "Top 3 countries by population:\n"
            for _, row in top_countries.iterrows():
                result += f"- {row[country_column]}: {row[population_column]:,}\n"
            return result
    
    return None  # No quick answer found

def save_note(note_text):
    """Save notes to file"""
    with open('data/notes.txt', 'a', encoding='utf-8') as f:
        f.write(f"{note_text}\n")
    return "Note saved successfully!"

# Enhanced main loop
print("\n" + "="*60)
print(" SMART COUNTRY AGENT READY!")
print("="*60)
print("I have access to detailed country data including:")
print("• Population 2023 numbers")
print("• Yearly change percentages") 
print("• World share percentages")
print("• Country rankings")
print("• And more demographic data")
print("\nTry these questions:")
print("- What is India's population in 2023?")
print("- Which country has the highest population?")
print("- What is the yearly change for China?")
print("- Compare population growth of India and China")
print("- Save a note: Interesting population trends")
print("- Capital of France (general knowledge)")
print("="*60)

while True:
    question = input("\nAsk about countries (q to quit): ").strip()
    
    if question.lower() == 'q':
        break
        
    if not question:
        continue
        
    # Handle note saving
    if question.lower().startswith('save note') or question.lower().startswith('save a note'):
        note_text = question.replace('save note', '').replace('Save note', '').strip()
        if note_text:
            result = save_note(note_text)
            print(f": {result}")
        else:
            print(" Please provide note content after 'save note'")
        continue
    
    # First try quick lookup for simple population questions
    quick_answer = quick_data_lookup(question)
    if quick_answer:
        print(f": {quick_answer}")
    else:
        # Use AI for more complex analysis
        print(" Analyzing with AI...")
        answer = smart_country_analysis(question)
        print(f": {answer}")

print("\nThank you for using the Smart Country Agent! ")