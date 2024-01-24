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

from typing import Any
from urllib.error import URLError

import numpy as np
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

import tensorflow
from transformers import AutoModelForTableQuestionAnswering, AutoTokenizer, pipeline



def apply_model_qa(df):
    MODEL = "google/tapas-large-finetuned-wtq"


    pipe = pipeline(model="lysandre/tiny-vit-random")

    t_tokenizer = AutoTokenizer.from_pretrained(MODEL)

    qa = pipeline("table-question-answering", model=MODEL, tokenizer=t_tokenizer)

    

    #df = df.astype(str)

    #qa = pipeline(task="table-question-answering", model=MODEL)
    #question = "How much did Albania produce in 1961?"

    #return qa(table=df, query=question)['cells'][0]

    return "OK"


def display_data() -> None:

    if 'start_questioning' not in st.session_state:
        st.session_state.start_questioning = False



    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        
        
        data = df
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
            
            
            
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )

    if st.button("Start Questioning"):
        st.session_state.start_questioning= True

    if st.session_state.start_questioning == True:
        st.session_state.start_questioning = True
        
        if prompt:=st.chat_input("Start questioning...?"):

            result = apply_model_qa(df)
            st.write("doing something" + result)




st.set_page_config(page_title="World Bank Q & A", page_icon=":world_map:")
st.markdown("# World Bank")
st.sidebar.header("World Bank")
st.write(
    """This app shows how you can use natural language for Questioning and Answering functionality on a model."""
)

display_data()

