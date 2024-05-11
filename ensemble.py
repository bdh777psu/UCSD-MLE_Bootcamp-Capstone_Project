import os

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.output_parsers.string import StrOutputParser

from basic_chain import get_model
from rag_chain import make_rag_chain
from local_loader import load_csv_files
from splitter import split_documents
from vector_store import create_vector_db
from dotenv import load_dotenv


def ensemble_retriever_from_docs(docs):
    texts = split_documents(docs)
    vs = create_vector_db(texts)
    vs_retriever = vs.as_retriever()

    bm25_retriever = BM25Retriever.from_texts([t.page_content for t in texts])

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vs_retriever],
        weights=[0.5, 0.5])

    return ensemble_retriever


def main():
    load_dotenv()

    docs = load_csv_files()
    
    model = get_model()
    ensemble_retriever = ensemble_retriever_from_docs(docs)
    output_parser = StrOutputParser()
    chain = make_rag_chain(model, ensemble_retriever) | output_parser

    result = chain.invoke("What are the most common mental health disorders reported in the 'Mental Health in the Tech Industry Survey'?")
    print(result)


if __name__ == "__main__":
    # this is to quite parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()

