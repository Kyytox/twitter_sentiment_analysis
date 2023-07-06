import streamlit as st
import pandas as pd

# lib for graphs
import plotly.express as px

# functions
from vizualisation.widgets import get_freq_option

sentiments = ['Positive','Neutral','Negative']

# color in graphs
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]


##################################################
# Graphs interactions 

# Interactions Line chart
# Number of interactions by freq_option
def get_line_chart_interactions(df):
    
        freq_option = get_freq_option(2)
    
        # group dataframe by day and sentiment and calculate the mean of score 
        # create a new data frame with 3 columns [date_tweet sentiment score]
        df_data_line = df.groupby([pd.Grouper(key='date_tweet',freq=freq_option)]).agg({'nb_interactions': 'sum'}).reset_index()
    
        fig = px.line(df_data_line, 
                    x='date_tweet', 
                    y='nb_interactions', 
                    color_discrete_sequence=colors, 
                    labels={'nb_interactions':'Nombre d\'interactions'},
                    width=800,
                    height=600)
        fig.update_traces(mode='lines+markers')
        return fig



# bar charts interactions
# Number of interactions by sentiment
def get_bar_charts_interactions(df):
    fig5 = px.bar(df, x="sentiment", y="count", color="interactions", color_discrete_sequence=['rgb(0, 186, 24)', 'rgb(29, 155, 240)','rgb(249, 24, 128)', 'rgb(218, 223, 0)'] , text="interactions")
    fig5.update_traces(hovertemplate='%{label}<br>%{value}') # data when hover graph
    st.plotly_chart(fig5, use_container_width=True)


# pie charts interactions
# Number of interactions by sentiment
def get_pie_charts_interactions(df):
    fig6 = px.sunburst(df, path=["sentiment","interactions"], values='count', color='sentiment', color_discrete_sequence=["rgb(145,0,13)","rgb(195,195,0)", "rgb(0,114,27)"])
    fig6.update_traces(hovertemplate='%{label}<br>%{value}') # data when hover graph 
    st.plotly_chart(fig6,use_container_width=True)
