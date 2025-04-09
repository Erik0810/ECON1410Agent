# Flask Web Application

This Flask web app uses OpenAI platform and vector stores to create an AI agent trained on the ECON1410 curriculum slides (PDFs). It combines this knowledge base with standard LLM capabilities to provide well-structured, informative responses. The app is optimized for both desktop and mobile use.

To use the app for a different course you can simply swap out the PDFs in the ECON1410 directory and tailor the system prompt inside document_store.py.

## Running the Application

1. Clone the repository
2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask development server:

```bash
flask run
```

5. Open your mobile browser and navigate to http://localhost:5000
