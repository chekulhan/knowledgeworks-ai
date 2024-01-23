# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from openai import OpenAI
from time import sleep

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Knowledge Works AI",
        page_icon="👋",
    )

    st.write("# Welcome to Knowledge Works AI! 👋")

    st.sidebar.success("Select a demo above.")


    st.image('assets/kw_small.png')
    """
    # Knowledge Works - AI 
    """

    client = OpenAI(api_key=st.secrets["API_KEY"])
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

    if 'start_chat' not in st.session_state:
        st.session_state.start_chat = False

    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None

    if 'messages' not in st.session_state:
        st.session_state.messages = []



    #st.set_page_config(page_title="Knowledge Works demo", page_icon=":speech_balloon:")

    if st.sidebar.button("Empezar Chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id=thread.id

    if st.button("Exit Chat"):
        st.session_state.messages=[]
        st.session_state.start_chat = False
        st.session_state.thread_id = None

    if st.session_state.start_chat == True:
        st.session_state.start_chat = True
        if "messages" not in st.session_state.messages:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_input(message["role"]):
                st.markdown(message["content"])
        
        if prompt:=st.chat_input("Pregunta...?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

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
                st.write(f"Esperando respuesta... {run.status}")
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
                sleep(8)

            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id)
            
            assistant_messages=[
                message for message in messages
                if message.run_id== run.id and message.role=="assistant"
            ]
            for message in assistant_messages:
                st.session_state.messages.append({"role":"assistant", "content":message.content[0].text.value})
                with st.chat_message("assistant"):
                    st.markdown(message.content[0].text.value)
    else:
        st.write("Pinchar 'Empezar Chat' para comenzar")
    


if __name__ == "__main__":
    run()
