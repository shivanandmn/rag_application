from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context,
)
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import WeaviateVectorStore
import weaviate
from llama_index.prompts import PromptTemplate
from weaviate.embedded import EmbeddedOptions
from pathlib import Path
from llama_index.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine
from src.models.huggingface import MODELS

# os.system("rm -rf ~/.local/share/weaviate")
import json


def indexing_from_directory(config):
    service_context = ServiceContext.from_defaults(
        embed_model=config["embed_model"],
        llm=MODELS[config["llm_model_repo_name"]](),
        chunk_size=180,
        chunk_overlap=10,
    )
    service_context.embed_model.embed_batch_size = 4
    set_global_service_context(service_context)

    client = weaviate.Client(
        embedded_options=EmbeddedOptions(),
    )
    index_name = Path(config["data_dir"]).stem.capitalize()
    schema_exists = client.schema.exists(index_name)

    vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)

    if schema_exists:
        print("Schema Exist!")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store, service_context=service_context
        )
    else:
        print("Schema Creating!")
        documents = SimpleDirectoryReader(config["data_dir"]).load_data()
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, use_async=False
        )

    return index, service_context
