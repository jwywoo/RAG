import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA


from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto

from ..core.config import settings

import os

def dating_generation(request):
    # Load Vector Store
    
    ## Embedding: OpenAI
    print("embeddings")
    embeddings = load_embeddings(
        model_name="text-embedding-3-large"
    )
    ## Vector Store: FAISS
    ### for local test: index_path="combined_faiss_index"
    print("Vector Store")
    vector_store = load_vector_store(
        index_dir_name="combined_faiss_index",
        embeddings=embeddings
    )
    
    # Init retriever 
    print("Retriever")
    retriever = load_retriever(
        vector_store=vector_store,
        search_type="mmr",
        k=5
    )

    # Init Chain
    print("QA Chain")
    qa_chain = load_llm_chain(
        model_name="gpt-3.5-turbo",
        retriever=retriever
    )
    # Generate result
    generated_result = qa_chain.invoke(request.query)
    generated_dating_response_dto = DatingGenResponseDto(dating=generated_result['result'])
    return generated_dating_response_dto

def load_embeddings(model_name):
    return OpenAIEmbeddings(
        model=model_name
    )

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

def load_retriever(vector_store, search_type ,k):
    return vector_store.as_retriever(
        search_type=search_type, 
        search_kwargs={"k": k}
    )


def load_llm_chain(model_name, retriever):
    llm = ChatOpenAI(model_name=model_name) 
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever
    )
    return qa_chain