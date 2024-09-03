from enum import Enum


class PromptsEnum(Enum):
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
