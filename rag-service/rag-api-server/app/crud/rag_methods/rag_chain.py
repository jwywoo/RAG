from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_rag_chain(template, retrieval_chain, model_name):
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model=model_name, temperature=0)
    final_rag_chain = (
        {"context": retrieval_chain,
        "question": itemgetter("question")}
        | prompt
        | llm
        | StrOutputParser()
    )
    return final_rag_chain