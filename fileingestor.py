import streamlit as st # type: ignore
from langchain.document_loaders import PyMuPDFLoader # type: ignore
from loadllm import Loadllm
from streamlit_chat import message # type: ignore
import tempfile
from langchain.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain.vectorstores import FAISS # type: ignore
from langchain.chains import ConversationalRetrievalChain # type: ignore

DB_FAISS_PATH = 'vectorstore/db_faiss'

class FileIngestor:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def handlefileandingest(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyMuPDFLoader(file_path=tmp_file_path)
        data = loader.load()

        # Create embeddings using Sentence Transformers
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        # Create a FAISS vector store and save embeddings
        db = FAISS.from_documents(data, embeddings)
        db.save_local(DB_FAISS_PATH)

        # Load the language model
        llm = Loadllm.load_llm()

        # Create a conversational chain
        chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

        # Function for conversational chat
        def conversational_chat(query):
            result = chain({"question": query, "chat_history": st.session_state['history']})
            st.session_state['history'].append((query, result["answer"]))
            return result["answer"]

        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello ! Ask me(LLAMA2) about " + self.uploaded_file.name + " 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! 👋"]

        # Create containers for chat history and user input
        response_container = st.container()
        container = st.container()

        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Talk to PDF data 🧮", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        # Display chat history
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
