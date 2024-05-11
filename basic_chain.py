import os

from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace

from dotenv import load_dotenv


ZEPHYR_ID = "HuggingFaceH4/zephyr-7b-beta"

def get_model(repo_id=ZEPHYR_ID):
    huggingfacehub_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN", None)
    os.environ["HF_TOKEN"] = huggingfacehub_api_token

    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        task="text-generation",
        max_new_tokens=512,
        top_k=30,
        temperature=0.1,
        repetition_penalty=1.03,
        huggingfacehub_api_token=huggingfacehub_api_token
        )
    chat_model = ChatHuggingFace(llm=llm)
    return chat_model


def basic_chain(model=None, prompt=None):
    if not model:
        model = get_model()
    if not prompt:
        prompt = ChatPromptTemplate.from_template("Tell me the most common mental health disorders from {book}")

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    return chain


def main():
    load_dotenv()

    chain = basic_chain()

    result = chain.invoke({"book": "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition (DSM-5)"})
    print(result)


if __name__ == '__main__':
    main()
