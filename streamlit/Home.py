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
import vizualisation.display_graph as dg



# Constants
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]

# Set page config 
st.set_page_config(
    page_title="Home",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Set page Subtitle
st.markdown(
    """
    This is a simple sentiment analysis app that uses the Twitter API to fetch tweets and perform sentiment analysis on them. \n
    :red[A few data is missing, because Twitter has restricted his api]. \n
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


if "lst_user" not in st.session_state:
    if st.session_state.df_data is None:
        st.session_state.lst_user = []
    else:
        st.session_state.lst_user = st.session_state.df_data['name_user'].unique().tolist()


if len(st.session_state.lst_user) == 0:
    st.write("No data available")
else:
    with st.sidebar:

        # Styles CSS for legend
        legend_style = """
            display: inline-block;
            margin-right: 10px;
            padding: 5px;
            border-radius: 10px;
        """

        # Legendary display
        st.subheader("Légend Graph")
        st.markdown(
            f'<span style="{legend_style} background-color: {colors[0]};">Negative</span>'
            f'<span style="{legend_style} background-color: {colors[1]};">Neutral</span>'
            f'<span style="{legend_style} background-color: {colors[2]};">Positive</span>',
            unsafe_allow_html=True
        )

        # User
        selected_user = st.selectbox("Select a user",st.session_state.lst_user, key='user_selector')

        # Tab
        current_tab = st.sidebar.radio("Select a section :", ["Sentiments", "Interactions", "Frequent Words"])



with st.container():
    if st.session_state.df_data is None:
        st.write("No data available")
    else:
        df = st.session_state.df_data[st.session_state.df_data['name_user'] == selected_user]
        st.title(f"Sentiment Analysis of :blue[{selected_user}]'s tweets")

        st.divider()

        if current_tab == "Sentiments":
            dg.tabs_sentiments(df)
        elif current_tab == "Interactions":
            dg.tabs_interactions(df)
        elif current_tab == "Frequent Words":
            dg.tabs_frequent_words(df)
