import os
from openai import OpenAI

class DocumentStore:
    def __init__(self,
                 store_name: str = "ECON1410_Knowledge_Base",
                 model: str = "gpt-4o-mini"):  # Testing with cheap model
        """
        Init the document store with OpenAI client
        
        Args:
            store_name: Name of the vector store
            model: OpenAI model to use (e.g., "gpt-4-0125-preview", "gpt-3.5-turbo")

        To swap to a different course change the system prompt inside the query_documents method
        """
        self.client = OpenAI()
        self.store_name = store_name
        self.model = model
        self.vector_store = None
        self.initialize_store()

    def initialize_store(self):
        """Create or get existing vector store"""
        try:
            # List existing vector stores to check if ours exists
            stores = self.client.vector_stores.list()
            existing_store = next(
                (store for store in stores.data if store.name == self.store_name),
                None
            )
            
            if existing_store:
                print(f"Using existing vector store: {self.store_name}")
                self.vector_store = existing_store
            else:
                print(f"Creating new vector store: {self.store_name}")
                self.vector_store = self.client.vector_stores.create(
                    name=self.store_name
                )
        except Exception as e:
            print(f"Error initializing vector store: {str(e)}")
            raise

    def upload_files(self, directory: str = "ECON1410"):
        """Upload PDF files from directory to vector store"""
        if not os.path.exists(directory):
            raise ValueError(f"Directory {directory} does not exist")

        # Get all PDF files in directory
        pdf_files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.endswith('.pdf')
        ]

        for pdf_path in pdf_files:
            try:
                print(f"Uploading {pdf_path}...")
                with open(pdf_path, 'rb') as file:
                    self.client.vector_stores.files.upload_and_poll(
                        vector_store_id=self.vector_store.id,
                        file=file
                    )
            except Exception as e:
                print(f"Error uploading {pdf_path}: {str(e)}")

    def query_documents(self, query: str) -> str:
        """Query the vector store and get a response"""
        try:
            # Search the vector store
            results = self.client.vector_stores.search(
                vector_store_id=self.vector_store.id,
                query=query
            )
            
            # Format the results into a single text
            formatted_results = '\n'.join(
                '\n'.join(c.text for c in result.content)
                for result in results.data
            )
            
            # Use formatted results to generate a response
            chat_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": ("You are an expert teaching assistant for the ECON1410 course. "
                                  "Produce a concise answer based on the provided sources. "
                                  "Focus on international economics and trade concepts."
                                  "If the user doesnt explicitly ask a question, DO NOT SPIT OUT RANDOM INFO")
                    },
                    {
                        "role": "user",
                        "content": f"Sources: {formatted_results}\n\nQuery: '{query}'"
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return chat_response.choices[0].message.content

        except Exception as e:
            print(f"Error querying documents: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

# Example usage:
# doc_store = DocumentStore()
# doc_store.upload_files()  # Only needed once
# response = doc_store.query_documents("What are the main topics in ECON1410?")