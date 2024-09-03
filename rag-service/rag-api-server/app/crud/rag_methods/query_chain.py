from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def get_query_chain(template, model_name):
    prompt_perspectives = ChatPromptTemplate.from_template(template)
    generate_queries = (
        prompt_perspectives
        | ChatOpenAI(model=model_name, temperature=0)
        | StrOutputParser()
        | (lambda x: x.split("\n"))
        )
    return generate_queries 