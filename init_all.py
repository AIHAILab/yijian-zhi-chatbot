from langchain_qdrant import QdrantVectorStore

from index import create_or_get_vector_store
from split import split_word


def init_all() -> QdrantVectorStore:
    input_path = "data/original/yijian_zhi.docx"
    output_path = "data/splitted"
    split_word(input_path, output_path)
    return create_or_get_vector_store(docs_path=output_path)


if __name__ == "__main__":
    vector_store = init_all()
    print(vector_store)
    results = vector_store.similarity_search(query="魚", k=1)
    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")
