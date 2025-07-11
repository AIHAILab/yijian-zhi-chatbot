import logging
from pathlib import Path

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document
from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from settings import settings
from setup_logging import setup_logging

logger = logging.getLogger(__name__)


def is_directory_valid(directory: str) -> bool:
    return any(file.suffix == ".txt" for file in Path(directory).iterdir())


def load_documents(directory: str) -> list[Document]:
    if not is_directory_valid(directory):
        raise FileNotFoundError(f"Directory {directory} does not contain splitted txt files")
    loader = DirectoryLoader(directory, glob="*.txt")
    return loader.load()


def get_or_create_vector_store(
    input_dir: str = settings.data_source_splitted_dir,
    vector_store_dir: str = settings.vector_store_dir,
    collection_name: str = "collection",
    embeddings: Embeddings = OpenAIEmbeddings(model=settings.embedding_model),
    dimensions: int = settings.dimensions,
) -> QdrantVectorStore | None:
    """
    Get an existing vector store or create a new one.

    This function ensures that only one Qdrant client is active at a time
    to prevent file locking issues.
    """
    client = QdrantClient(path=vector_store_dir)

    try:
        # Check if the collection already exists.
        # The qdrant_client raises a ValueError if the collection does not exist.
        client.get_collection(collection_name=collection_name)
        logger.info(f"Collection '{collection_name}' already exists. Loading vector store.")
        return QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )
    except ValueError:
        logger.info(f"Collection '{collection_name}' not found. Creating a new one.")
        try:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=dimensions, distance=Distance.COSINE),
            )
            logger.info(f"Successfully created collection '{collection_name}'.")

            vector_store = QdrantVectorStore(
                client=client,
                collection_name=collection_name,
                embedding=embeddings,
            )
            documents = load_documents(input_dir)
            vector_store.add_documents(documents=documents)
            logger.info("Successfully added documents to the new vector store.")
            return vector_store
        except FileNotFoundError:
            logger.error(f"Directory {input_dir} does not contain txt files for indexing.")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating the vector store: {e}", exc_info=True)
            return None


def main():
    setup_logging()
    logger.info("Starting to create or get vector store...")
    vector_store = get_or_create_vector_store()
    results = vector_store.similarity_search(query="魚", k=1)  # type: ignore
    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")


if __name__ == "__main__":
    main()
