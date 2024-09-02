import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from .rag_methods.retrieval_chain import get_retrieval_chain
from .rag_methods.rag_chain import get_rag_chain
from .rag_methods.result_parsing import get_dto

from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto

from ..core.config import settings

import os
import time

SEP = "[SEP]"

def dating_generation(request):
    start_time = time.time()

    question_query = request.title + SEP + request.description + SEP + request.dateTime + SEP + request.activityDescription
    # Load Vector Store
    ## Embedding: OpenAI
    print("embeddings")
    embeddings = load_embeddings(
        model_name="text-embedding-3-large"
    )

    ## Templates for query and answer generation
    query_gen_template = """
        You are an expert planning a date for loved one, family and friends.
        Your task is retrieving relevant data to generate a date plan.
        You have access to a database of locations for dating in Seoul.
        Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector
        database.
        By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search.


        Each row in the table represents a location and its features.
        Features are separated by [SEP].
        If a row have 'None' in the feature, it means that the row doesn't have that feature.
        Every row is in Korean while column names are in English.
        Provide these alternative questions separated by newlines.
        Original question: {question}
    """
    
    answer_gen_template = """
        - You are a helpful assistant that answers questions about the context below.
        - You do not make up answers to questions that cannot be found in the context.
        - If you don't know the answer to a question, just say that you don't know. Don't try to make up an answer.
        - You will generate a list of activities and please follow the format:
        [
        {{
            "activityTitle": Get the name of the place,
            "activityLoc": Get the address of the place,
            "timeTotal": Generate your expected time about the place or just put 1 hour,
            "activityDescription": Generate a description of the place based on your understanding,
            "activityImage": Get url of the place
        }},
        ...
        ]
        - Make sure the list contains at least 5 activities
        - You have to answer in Korean.

        Answer the following question based on this context:

        {context}

        Question: {question}
    """

    ## Retrieval Chain + Query Analysis
    ### for local test: "combined_faiss_index"
    ### for deployment: "app.combined_faiss_index"
    print("Retrieval Chain")
    retrieval_chain = get_retrieval_chain(
        template=query_gen_template,
        model_name ="gpt-3.5-turbo",
        vector_store_path="combined_faiss_index",
        embeddings=embeddings
    )

    ## RAG Chain
    print("Rag Chain")
    rag_chain = get_rag_chain(
        template=answer_gen_template,
        model_name="gpt-3.5-turbo",
        retrieval_chain=retrieval_chain,
    )

    generated_answer = rag_chain.invoke({"question":question_query})
    generate_dating_responses = get_dto(generated_answer)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"FAISS index initialization took {elapsed_time:.4f} seconds")
    return generate_dating_responses

def load_embeddings(model_name):
    return OpenAIEmbeddings(
        model=model_name
    )
