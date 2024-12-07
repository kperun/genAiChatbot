from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from openai import OpenAI
import os

create_sample_request = False


class Chatbot:
    def __init__(self):
        # Setup the API key
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("OpenAI API Key loaded: " + api_key[0:10])
        else:
            print("OpenAI API Key not loaded")
            exit(0)
        # Create the connection to the API
        self.client = OpenAI()

        index = None
        try:
            storage_context = StorageContext.from_defaults(persist_dir='ml_index')
            index = load_index_from_storage(storage_context)
            print("Index loaded from storage")
        except:
            # Load the documents and create an embedding
            # documents = SimpleDirectoryReader('resources/pdf_easy').load_data()
            documents = SimpleDirectoryReader('resources/pdf_hard').load_data()
            # create an index to search over
            index = VectorStoreIndex.from_documents(documents)
            # Store the index so it is not required to be regenerated
            index.storage_context.persist('ml_index')
            print("Index created")

        # create a search engine to search in the index with
        self.engine = index.as_query_engine()

    def create_sample_request(self):
        completion = self.client.chat.completions.create(
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

    def query_engine(self, request: str):
        # Get the result, it uses the documents + open ai (with RAG) to retrieve the information from the context given
        return self.engine.query(request)
