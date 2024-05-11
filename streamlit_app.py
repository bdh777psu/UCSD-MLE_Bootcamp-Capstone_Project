import streamlit as st

from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from ensemble import ensemble_retriever_from_docs
from full_chain import create_full_chain
from remote_loader import download_csv
from local_loader import load_csv_files


st.set_page_config(page_title="UCSD MLE Bootcamp Capstone - Diogo Lessa")
st.image(image="static/cover_image.png") 
st.title("Mental Health in the Tech Industry Q&A Chatbot")  
st.markdown("""Ask me questions such as: "What are the main findings in the 'Mental Health in the Tech Industry Survey'?"
                (contribute to the Survey at: https://forms.gle/CzRFVaxMy5S3asVp6)""")


def run(prompt_to_user="What would you like to know?"):
    chain = get_chain()

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖"):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = chain.invoke(
                    {"question": prompt},
                    config={"configurable": {"session_id": "foo"}}
                    )

                st.markdown(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


@st.cache_resource
def get_retriever():
    survey_responses = "https://docs.google.com/spreadsheets/d/1Oj8ROLPcsq_I8h3Au7bE9cUSFhTFQx3eEIr8BXV1Jx4/export?format=csv"
    download_csv(survey_responses, filename='Mental Health in the Tech Industry Survey')

    docs = load_csv_files()
    
    return ensemble_retriever_from_docs(docs)


def get_chain():
    ensemble_retriever = get_retriever()
    chain = create_full_chain(ensemble_retriever,
                              chat_memory=StreamlitChatMessageHistory(key="langchain_messages")
                              )
    return chain
    
    
run()