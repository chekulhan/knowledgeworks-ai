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


LOGGER = get_logger(__name__)




def run():
    st.set_page_config(
        page_title="Knowledge Works AI",
        page_icon="assets/kw_small.png",
    )
    
    st.image('assets/kw_small.png')
    st.write("# Bienvenidos a Knowledge Works AI!")
    st.caption("Con nuestro proyecto de Inteligencia Artificial, estamos probado diferentes funciones y limites de la IA.")
    st.caption("Para más información, ponte en contacto con https://knowledgeworks.cl/.")
    st.warning("Este proyecto es sólo una demonstración.", icon="⚠️")

    st.write("Use Case para mostrar las capabilidades de un modelo adaptado a un contexto industríal. ")
    if st.button("Ir a GPT basado en una máquina cortadora"):
        st.switch_page("pages/0_GPT.py")


    


if __name__ == "__main__":
    run()
