import os

from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from basic_chain import get_model
from filter import ensemble_retriever_from_docs
from local_loader import load_csv_files
from memory import create_memory_chain
from rag_chain import make_rag_chain


def create_full_chain(retriever, chat_memory=ChatMessageHistory()):
    model = get_model()
    system_prompt = """You are a helpful AI assistant for busy IT professionals trying to improve their mental health.
    Use the following context and the users' chat history to help the user:
    If you don't know the answer, just say that you don't know. 
    
    Context: {context}
    
    Question: """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )

    rag_chain = make_rag_chain(model, retriever, rag_prompt=prompt)
    chain = create_memory_chain(model, rag_chain, chat_memory) | StrOutputParser()
    return chain


def main():
    load_dotenv()

    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()

    docs = load_csv_files()
    ensemble_retriever = ensemble_retriever_from_docs(docs)
    chain = create_full_chain(ensemble_retriever)

    queries = [
        "Generate a list of the most common mental health disorders reported in the 'Mental Health in the Tech Industry Survey'",
        "Summarize the findings in the 'Mental Health in the Tech Industry Survey'"
    ]

    for query in queries:
        response = chain.invoke(
            {"question": query},
            config={"configurable": {"session_id": "foo"}}
            )
        console.print(Markdown(response))


if __name__ == '__main__':
    # this is to quiet parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()
