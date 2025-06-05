from pathlib import Path

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_core.documents import Document
from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


def is_directory_valid(directory: str) -> bool:
    return any(file.suffix == ".txt" for file in Path(directory).iterdir())


def load_documents(directory: str) -> list[Document]:
    if not is_directory_valid(directory):
        raise FileNotFoundError(f"Directory {directory} does not contain splitted txt files")
    loader = DirectoryLoader(directory, glob="*.txt")
    return loader.load()


def get_vector_store(
    embeddings: Embeddings = OpenAIEmbeddings(model="text-embedding-3-large"),
    collection_name: str = "collection",
    path: str = "./data/qdrant",
) -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        path=path,
    )


def create_or_get_vector_store(
    docs_path: str = "./data/splitted",
    store_path: str = "./data/qdrant",
    collection_name: str = "collection",
    embeddings: Embeddings = OpenAIEmbeddings(model="text-embedding-3-large"),
    dimensions: int = 3072,
) -> QdrantVectorStore:
    client = QdrantClient(path=store_path)
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dimensions, distance=Distance.COSINE),
        )
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )
        documents = load_documents(docs_path)
        _ = vector_store.add_documents(documents=documents)
        return vector_store
    except ValueError:
        client.close()
        return get_vector_store(embeddings, collection_name, store_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory {docs_path} does not contain txt files")
    except Exception as e:
        raise e


if __name__ == "__main__":
    vector_store = create_or_get_vector_store()
    results = vector_store.similarity_search(query="魚", k=1)
    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")
