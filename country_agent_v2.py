import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Set API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

print(" Country Analysis Agent - Version 2")
print("Adding PDF processing...")

# Load CSV
population_df = pd.read_csv('data/population.csv')
print(" CSV loaded")

# Test PDF processing
try:
    from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
    from llama_index.readers import PDFReader
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Use test PDF first
    pdf_file = "India_test.pdf"  # Change to "India.pdf" if you want the full version
    pdf_path = os.path.join(BASE_DIR, "data", pdf_file)
    
    if os.path.exists(pdf_path):
        print(f" PDF found: {pdf_file}")
        
        # Load PDF
        india_pdf = PDFReader().load_data(file=pdf_path)
        print(" PDF loaded successfully")
        
        # Create index
        index_name = "india_test_index"
        if not os.path.exists(index_name):
            print("Building index...")
            india_index = VectorStoreIndex.from_documents(india_pdf, show_progress=True)
            india_index.storage_context.persist(persist_dir=index_name)
        else:
            india_index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name))
        
        india_engine = india_index.as_query_engine()
        print(" PDF query engine created")
        
        # Test PDF query
        test_query = "What is this document about?"
        print(f"\nTesting PDF query: {test_query}")
        result = india_engine.query(test_query)
        print(f"PDF Result: {result}")
        
    else:
        print(f" PDF file not found: {pdf_path}")
        
except Exception as e:
    print(f" PDF processing error: {e}")

print("\n PDF processing working! Ready for next step.")