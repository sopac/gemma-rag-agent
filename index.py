from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
import chromadb
import asyncio
import os

#paths = ["/Users/sachin/Downloads/", "/Users/sachin/Dropbox/", "/Users/sachin/Library/Mail"]
paths = []
with open('sources.txt') as f:
    paths = f.read().splitlines()

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

#vector store
chroma_client = chromadb.PersistentClient()
chroma_collection = "rag"

#reindex from scratch
for c in chroma_client.list_collections():
    if c.name == chroma_collection:
        chroma_client.delete_collection(chroma_collection)
        
chroma_collection = chroma_client.create_collection(chroma_collection)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# index
for path in paths:
    print(f"Indexing {path}...")
    documents = SimpleDirectoryReader(path).load_data(show_progress=True)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, transformations=[SentenceSplitter(chunk_size=512)]
    )

print("RAG Documents Indexed Into Vector Store.")
