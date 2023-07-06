import streamlit as st
import pandas as pd
import numpy as np

import sys
from pathlib import Path
import dotenv


# load env variables
dotenv.load_dotenv()

sys.path.append(str(Path(__file__).parent.parent))

# AWS utils 
from airflow.plugins.helpers.aws_utils import get_partitionned_file_aws

# Data Viz utils
from vizualisation.display_graph import *


# Set page config 
st.set_page_config(
    page_title="Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set page Title
st.title("Twitter Sentiment Analysis")


# Set page Subtitle
st.markdown(
    """
    This is a simple sentiment analysis app that uses the Twitter API to fetch tweets and perform sentiment analysis on them.
    """
)



# Session State
if "df_data" not in st.session_state:
    with st.spinner("Loading data..."):
        try:
            st.session_state.df_data = get_partitionned_file_aws("Gold/tweets_transform.parquet")
            st.session_state.df_data['date_tweet'] = pd.to_datetime(st.session_state.df_data['date_tweet'] , format='%Y-%m-%d %H:%M:%S')
        except:
            st.session_state.df_data = None

st.write(st.session_state.df_data.shape)
st.write(st.session_state.df_data.head())

if "lst_user" not in st.session_state:
    st.session_state.lst_user = st.session_state.df_data['name_user'].unique().tolist()


if len(st.session_state.lst_user) == 0:
    st.write("No data available")
else:
    with st.sidebar:
        selected_user = st.selectbox("Select a user",
                                    st.session_state.lst_user, key='user_selector')
        



with st.container():
    df = st.session_state.df_data[st.session_state.df_data['name_user'] == selected_user]
    st.title(f"Sentiment Analysis of {selected_user}'s tweets")

    display_graph(df)
