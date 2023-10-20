import streamlit as st
from streamlit_chat import message
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.llms import Replicate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

import os
from dotenv import load_dotenv
import tempfile

#Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = "r8_bnj7RZGhbYp1ECDF5fwCFjDZwy4MDJg2LoAjg"




#Inicializando la sesion del chatbot 
def initialize_session_state():
    
    #['history'] almacena el historial de conversaciones del usuario cuando está en Streamlit.
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    #['generated'] almacena a las respuestas del chatbot.
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hola! Pregúntame acerca de tus documentos... 🤗"]

    #['past'] almacena los mensajes proporcionados por el usuario.
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hola! 👋"]
        

#función que recibe como argumento la pregunta del usuario, el objeto chain y el historial 
def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    
    #container para el chat history
    reply_container = st.container()
    
    #container para la entrada de texto del usuario
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Pregunta:", placeholder="Pregunta acerca de tus documentos", key='input')
            submit_button = st.form_submit_button(label='Enviar')

        if submit_button and user_input:
            with st.spinner('Generando respuesta...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])
                
           
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    #Se muestran los mensajes del usuario y del chatbot en Streamlit 
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")               


def create_conversational_chain(vector_store):
    load_dotenv()

    
    # Create llm
    llm = Replicate(
        streaming = True,
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781", 
        callbacks=[StreamingStdOutCallbackHandler()],
        input = {"temperature": 0.01, "max_length" :500,"top_p":1})
    
    #si la temperartura tiende a cero entonces es racional sino temperatura mas alta pensamiento divergente 
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    #obtención del chatbot con memoria a la vez que se depende del vector_store para encontrar información relevante de los documentos
    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)

    return chain

def main():
    load_dotenv()
    
    # Inicializar session state
    initialize_session_state()
    st.title("ChatBot using llama2 :books:")
    
    # Inicializar Streamlit
    st.sidebar.title("Document Processing")
    uploaded_files = st.sidebar.file_uploader("Upload files", accept_multiple_files=True)


    if uploaded_files:
        text = []
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            #Carga de documentos 

            loader = None
            if file_extension == ".pdf":
                loader = PyPDFLoader(temp_file_path)
            elif file_extension == ".docx" or file_extension == ".doc":
                loader = Docx2txtLoader(temp_file_path)
            elif file_extension == ".txt":
                loader = TextLoader(temp_file_path)

            if loader:
                text.extend(loader.load())
                os.remove(temp_file_path)
                
        #Dividimos los documentos en segmentos de 1000 caracteres con una coincidencia de 100 characteres entre las partes segmentadas

        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100, length_function=len)
        text_chunks = text_splitter.split_documents(text)

        # Creación de embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                           model_kwargs={'device': 'cpu'})

        # Creación del vector 
        vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
        
        # Creación del objeto chain
        chain = create_conversational_chain(vector_store)

        
        display_chat_history(chain)

if __name__ == "__main__":
    main()

#streamlit run app.py
