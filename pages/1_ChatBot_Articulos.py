import streamlit as st
from streamlit.logger import get_logger
from annotated_text import annotated_text
import streamlit.components.v1 as components

# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-chatgpt-like-app

LOGGER = get_logger(__name__)

                                      
# main

st.set_page_config(
        page_title="Knowledge Works AI",
        page_icon="assets/kw_small.png",
    )
st.image('assets/kw_small.png')
st.write("# Knowledge Works AI!")
st.caption("Un chatbot con artículos escritos por Javier Martínez Aldanondo, Socio Gestión del Conocimiento en Knowledge Works, sobre el conocimiento crítico.")
st.warning("De momento, hay funciones que no están totalmente desarrollados.", icon="⚠️")
st.write("**Desplazarse hacia abajo** y pinchar el botón para hablar con ella. :female-teacher:")

components.html(
    """
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script src="https://mediafiles.botpress.cloud/f62897e7-ae56-459d-bf2f-ee0bf9cc07d7/webchat/config.js" defer></script>

    """,
    height=600,
    )
