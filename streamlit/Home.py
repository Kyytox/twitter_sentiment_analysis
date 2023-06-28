import streamlit as st
import pandas as pd
import numpy as np

import tweepy
import dotenv
import os

# load env variables
dotenv.load_dotenv()


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


# AWS utils 
from airflow.plugins.aws.aws_utils import get_file_aws


# Set page config 
st.set_page_config(
    page_title="Home",
    page_icon="🧊",
    # layout="wide",
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
if "df_history_tech" not in st.session_state:
    # get df_history_tech from AWS S3
    try:
        st.session_state.df_history_tech = get_file_aws("history_tech.parquet")
    except:
        st.session_state.df_history_tech = None



st.write(st.session_state.df_history_tech)