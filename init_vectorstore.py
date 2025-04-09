from document_store import DocumentStore
import os
from dotenv import load_dotenv

def initialize_vector_store():
    """
    Initialize the OpenAI vector store and upload ECON1410 documents.
    This only needs to be run once, or when new documents are added.
    """
    print("Loading environment variables...")
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    print("Initializing OpenAI vector store...")
    try:
        # Init with specific store name
        doc_store = DocumentStore(store_name="ECON1410_Knowledge_Base")
        
        # Upload PDF files
        print("Uploading PDF files from ECON1410 folder...")
        doc_store.upload_files()
        
        print("\nInitialization complete!")
        print("The vector store is now ready for use.")
        print("You can now run the main Flask application (app.py)")
        
    except Exception as e:
        print(f"\nError during initialization: {str(e)}")
        print("\nPlease ensure:")
        print("1. The ECON1410 folder exists with PDF files")
        print("2. Your OpenAI API key is correctly set in .env")
        print("3. The PDF files are readable and not corrupted")
        print("4. You have an active internet connection")

if __name__ == "__main__":
    initialize_vector_store()