from dotenv import load_dotenv
from document_store import DocumentStore

# Environment variables
load_dotenv()

# Init document store with specific name and model
doc_store = DocumentStore(
    store_name="ECON1410_Knowledge_Base",
    model="gpt-4o-mini"  # Cheap model :) Might swap to more expensive one if it proves to be bad
)

def get_ai_response(message):
    """
    Get a response based on the ECON1410 course materials using OpenAI's vector store.
    """
    try:
        # Query the vector store and get AI response
        response = doc_store.query_documents(message)
        
        # Handle empty response
        if not response or response.strip() == "":
            return ("I'm not sure about that based on the course materials. "
                   "Could you please rephrase your question or ask something else?")
        
        return response.strip()
    
    # Add functionality to answer based on users language here?
    except Exception as e:
        print(f"Error in document query: {str(e)}")
        return "I apologize, but I encountered an error. Please try again."
