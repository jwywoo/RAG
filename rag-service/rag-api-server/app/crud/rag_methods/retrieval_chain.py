from langchain.load import dumps, loads
import faiss
from langchain_community.vectorstores import FAISS


from .query_chain import get_query_chain

def get_unique_union(documents: list[list]):
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]

def get_retrieval_chain(vector_store_path, embeddings, template, model_name):
    vector_store = load_vector_store(index_dir_name=vector_store_path, embeddings=embeddings)
    retrieval = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5}
    )
    retrieval_chain = get_query_chain(template=template, model_name=model_name) | retrieval.map() | get_unique_union
    return retrieval_chain


def load_vector_store(index_dir_name, embeddings):
    try:
        return FAISS.load_local(
            index_dir_name, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(e)
        return None