from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from .rag_methods.retrieval_chain import get_retrieval_chain
from .rag_methods.rag_chain import get_rag_chain
from .rag_methods.result_parsing import get_dto

from ..prompt_templates.prompt_templates_enum import PromptsEnum
from ..schema.response_dto.dating_generation_response_dto import DatingGenResponseDto
from ..schema.request_dto.dating_generation_request_dto import DatingGenRequestDto
from ..core.config import settings


import os
import faiss
import time

SEP = "[SEP]"


def dating_generation(request: DatingGenRequestDto) -> list[DatingGenResponseDto]:
    """Generate a list of activities based on given request

    Args:
        request (DatingGenRequestDto): Contains features of dating and its activities

    Returns:
        list[DatingGenResponseDto]: Result of generation
    """
    start_time = time.time()

    # Question query
    question_query = request.title + SEP + request.description + \
        SEP + request.dateTime + SEP + request.activityDescription

    # Load Vector Store
    # Embedding: OpenAI
    print("embeddings")
    embeddings = load_embeddings(
        model_name="text-embedding-3-large"
    )

    # Templates for query and answer generation
    templates_enum = PromptsEnum
    query_gen_template = templates_enum.query_gen_template.value
    answer_gen_template = templates_enum.answer_gen_template.value

    # Retrieval Chain + Query Analysis
    # for local test: "combined_faiss_index"
    # for deployment: "app.combined_faiss_index"
    print("Retrieval Chain")
    retrieval_chain = get_retrieval_chain(
        template=query_gen_template,
        model_name="gpt-3.5-turbo",
        vector_store_path="combined_faiss_index",
        embeddings=embeddings
    )

    # RAG Chain
    print("Rag Chain")
    rag_chain = get_rag_chain(
        template=answer_gen_template,
        model_name="gpt-3.5-turbo",
        retrieval_chain=retrieval_chain,
    )

    generated_answer = rag_chain.invoke({"question": question_query})
    generate_dating_responses = get_dto(generated_answer)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"FAISS index initialization took {elapsed_time:.4f} seconds")
    return generate_dating_responses


def load_embeddings(model_name):
    return OpenAIEmbeddings(
        model=model_name
    )
