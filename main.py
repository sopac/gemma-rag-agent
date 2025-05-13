from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.workflow import Context
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
import chromadb
import asyncio
import os,sys

model = "ebdm/gemma3-enhanced:12b"
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(model=model, request_timeout=360.0)
Settings.chunk_size = 512


#vector store
chroma_collection = "rag"
chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.get_collection(chroma_collection)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

#get index
index = VectorStoreIndex.from_vector_store(
    vector_store,
)


query_engine = index.as_query_engine(
    # llm=Settings.llm,
)

async def search_documents(query: str) -> str:
    response = await query_engine.aquery(query)
    return str(response)


# agent
agent = AgentWorkflow.from_tools_or_functions(
    [search_documents],
    llm=Settings.llm,
    #system_prompt="""*""",
)

ctx = Context(agent)

# ask
async def main():
    print(f"Gemma3 ({model}) RAG Agent. (type /q to quit)")
    while True:
        query = input("Q: ")
        if query == "/q":
            sys.exit(0)
        response = await agent.run(
            query, ctx=ctx
        )
        print(response + "\n")
        #response.print_response_stream()


# run
if __name__ == "__main__":
    asyncio.run(main())