from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from openai import OpenAI
import os

create_sample_request = False

# Setup the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("OpenAI API Key loaded: " + api_key[0:10])
else:
    print("OpenAI API Key not loaded")
    exit(0)

# Create the connection to the API
client = OpenAI()

if create_sample_request:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )
    print(completion.choices[0].message.content)

# Load the documents and create an embedding
documents = SimpleDirectoryReader('resources/PDF').load_data()

# create an index to search over
index = VectorStoreIndex.from_documents(documents)

# create a search engine to search in the index with
engine = index.as_query_engine()

# Get the result, it uses the documents + open ai (with RAG) to retrieve the information from the context given
result = engine.query('What is python?')

# Store the index so it is not required to be regenerated
index.storage_context.persist('ml_index')

