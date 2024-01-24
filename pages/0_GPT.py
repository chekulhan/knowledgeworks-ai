import streamlit as st
from streamlit.logger import get_logger
from openai import OpenAI
from time import sleep
from annotated_text import annotated_text

# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-chatgpt-like-app

LOGGER = get_logger(__name__)


def run():

    client = OpenAI(api_key=st.secrets["API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id=thread.id

    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Preguntar...?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""


            assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

            message = client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt,
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant.id
            )

            while (run.status != "completed"):
  
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
                with st.spinner('Esperando respuesta...' + run.status):
                    sleep(10)

                if run.status == "failed":
                    st.write("Hay un limite de 3 peticiones al minuto. Intentálo de nuevo en 60 segundos...")
                    break
            
            
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id)
            
            assistant_messages=[
                message for message in messages
                if message.run_id==run.id and message.role=="assistant"
            ]
            for message in assistant_messages:
                st.session_state.messages.append({"role":"assistant", "content":message.content[0].text.value})
                message_placeholder.markdown(full_response + "▌")

                full_response += (message.content[0].text.value or "")
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

                                      
# main

st.set_page_config(
        page_title="Knowledge Works AI",
        page_icon="assets/kw_small.png",
    )
st.image('assets/kw_small.png')
st.write("# Knowledge Works AI!")
st.caption("Con nuestro Inteligencia Artificial sobre una máquina industrial, puedes hacer preguntas sobre nuestra máquina cortadora, e incluso preguntarla para generar preguntas para un examen.")
st.caption("Limitaciones: Con este modelo, no hay soporte para imágenes")

st.warning("De momento, hay un limite de 3 preguntas cada mínuto.", icon="⚠️")

annotated_text(
    "Puedes preguntarme",
    ("sobre los procedimientos de la máquina cortadora", "¿Dónde están las bobinas?"),
    " o otra información sobre",
    ("la máquina cortadora", "¿Qué hay que hacer al comienzo del turno?"),
    ".Incluso, soy capaz de generar un",
    ("quiz con preguntas y respuestas", "Generar 2 preguntas sobre el producto terminado. Incluir respuestas.")
)


run()