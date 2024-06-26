import os

from dotenv import load_dotenv
from langchain import hub
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages.base import BaseMessage

from basic_chain import basic_chain, get_model
from local_loader import load_csv_files
from splitter import split_documents
from vector_store import create_vector_db


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_question(input):
    if not input:
        return None
    elif isinstance(input,str):
        return input
    elif isinstance(input,dict) and 'question' in input:
        return input['question']
    elif isinstance(input,BaseMessage):
        return input.content
    else:
        raise Exception("string or dict with 'question' key expected as RAG chain input.")


def make_rag_chain(model, retriever, rag_prompt=None):
    # We will use a prompt template from langchain hub.
    if not rag_prompt:
        rag_prompt = hub.pull("rlm/rag-prompt")

    # And we will use the LangChain RunnablePassthrough to add some custom processing into our chain.
    rag_chain = (
            {
                "context": RunnableLambda(get_question) | retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | rag_prompt
            | model
    )

    return rag_chain


def main():
    load_dotenv()
    model = get_model()
    docs = load_csv_files()
    texts = split_documents(docs)
    vs = create_vector_db(texts)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a mental health professional specialized in Psychiatry."),
        ("user", "{input}")
    ])
    # Besides similarly search, you can also use maximal marginal relevance (MMR) for selecting results.
    #retriever = vs.as_retriever(search_type="mmr")
    retriever = vs.as_retriever()

    chain = basic_chain(model, prompt)
    base_chain = chain | StrOutputParser()
    rag_chain = make_rag_chain(model, retriever) | StrOutputParser()

    questions = [
        "What are the most common mental health disorders according to the reported in the 'Mental Health in the Tech Industry Survey'",
        "What are the main findings of the 'Mental Health in the Tech Industry Survey'?"
    ]

    for q in questions:
        print("\n--- QUESTION: ", q)
        print("* BASE:\n", base_chain.invoke({"input": q}))
        print("* RAG:\n", rag_chain.invoke(q))


if __name__ == '__main__':
    # this is to quiet parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()
