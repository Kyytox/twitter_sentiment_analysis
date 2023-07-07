import datetime
import calendar
import streamlit as st
import pandas as pd


# lib for graphs
import plotly.express as px
import plotly.graph_objects as go

# functions 
from vizualisation.process_graph import *
from vizualisation.widgets import get_freq_option


sentiments = ['Positive','Neutral','Negative']

# color in graphs
# colors = ["rgb(0,114,27)", "rgb(195,195,0)", "rgb(145,0,13)"]
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]


##################################################
# Graphs Sentiments 

# Pie charts 
# distribution of the number of tweets by sentiments
def get_pie_charts_by_sent(df):
    data_pie = get_nb_tweets_sent(df)
    fig = go.Figure(
        data=[
            go.Pie(
                labels=data_pie['sentiment'],
                values=data_pie['nb_tweets'],
                pull=[0.015, 0.015, 0.015],
                marker_colors=colors,
            )
        ]
    )

    fig.update_layout(showlegend=False)
    return fig


# Bar charts 
# number of tweets by Sentiments 
def get_bar_charts_by_sent(df):
    data_bar = get_nb_tweets_sent(df)
    fig = px.bar(
        data_bar, 
        x='sentiment', 
        y='nb_tweets', 
        color='sentiment', 
        color_discrete_sequence=colors, 
        labels={'nb_tweets':'Tweet number analyzed'}, 
        text='nb_tweets')
    
    fig.update_layout(showlegend=False)
    fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    return fig




# Score line chart
# Mean of score by freq_option and by sentiment
def get_line_chart_score(df):
    freq_option = get_freq_option(1)

    # group dataframe by day and sentiment and calculate the mean of score 
    df_data_line = df.groupby([pd.Grouper(key='date_tweet',freq=freq_option), 'sentiment']).agg({'score': 'mean'}).reset_index()

    fig = px.line(df_data_line, 
                x='date_tweet', 
                y='score', 
                color='sentiment', 
                color_discrete_sequence=colors, 
                labels={'score':'Score moyen'},
                width=800,
                height=600)
    
    fig.update_layout(showlegend=False)
    fig.update_traces(mode='lines+markers')
    return fig



# Bar Charts Day
# Number of tweets by month and by sentiment
def get_bar_charts_month(df):
    
    # group dataframe by day and sentiment and calculate number of tweets
    df_data = df.groupby([pd.Grouper(key='date_tweet',freq='M'), 'sentiment'])\
        .agg({'sentiment': 'size'})\
        .rename(columns={'sentiment':'nb_tweets'})\
        .reset_index()


    # filter dataframe by year
    lst_year = df_data['date_tweet'].dt.strftime("%Y").unique()
    report_year = st.selectbox('Choose a year', lst_year, index=0, key=5)
    df_data = df_data[df_data['date_tweet'].dt.year == int(report_year)]

    # convert month to string
    df_data['date_tweet'] = df_data['date_tweet'].dt.strftime("%B")

    # create bar chart
    fig = px.bar(df_data, 
                x='date_tweet', 
                y='nb_tweets', 
                color='sentiment', 
                color_discrete_sequence=colors, 
                labels={'nb_tweets':'Number Tweets'},
                text='nb_tweets')

    fig.update_layout(showlegend=False)
    fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    return fig



# Number of tweets by day and by sentiment
def get_bar_charts_day(df):
    # Group dataframe by day and sentiment and count the number of tweets
    df_data = df.groupby([pd.Grouper(key='date_tweet', freq='D'), 'sentiment']) \
                            .agg({'sentiment': 'size'}) \
                            .rename(columns={'sentiment': 'nb_tweets'}) \
                            .reset_index()

    # Create year and month selection widgets
    lst_year = df_data['date_tweet'].dt.strftime("%Y").unique()
    report_year = st.selectbox('', lst_year, index=1, key=6)
    

    lst_month = df_data.query(f'date_tweet.dt.strftime("%Y") == "{report_year}"')['date_tweet'].dt.strftime("%B").unique()
    report_month_str = st.radio('Choose a month', lst_month, index=0, key=7, horizontal=True)
    report_month = list(calendar.month_name).index(str(report_month_str))

    # Filter dataframe by year and month
    df_data = df_data[df_data['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

    # Create a bar chart
    fig = px.bar(
        df_data,
        x='date_tweet',
        y='nb_tweets',
        color='sentiment', 
        color_discrete_sequence=colors, 
        labels={'nb_tweets':'Tweets'}, 
        text_auto=True)

    fig.update_layout(showlegend=False)
    fig.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
    return fig

# box charts of score by sentiment
def get_box_charts_score(df):
    # regroup df by sentiment 
    df_data_box = df.groupby(['sentiment'])\
        .agg({'score': ['mean', 'median', 'min', 'max', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]})\
        .reset_index()
        
    fig = go.Figure()

    # add trace for each sentiment
    for count_color, sentiment in enumerate(df_data_box['sentiment'].unique()):

        # extract all score for the sentiment and place them in a list
        list_data = df_data_box[df_data_box['sentiment'] == sentiment]['score'].values[0].tolist()

        # add trace for the sentiment
        fig.add_trace(go.Box(y=list_data,
                            name=sentiment, 
                            boxpoints='all', 
                            jitter=0,
                            marker_color=colors[count_color],
                            marker_size=3, 
                            line_width=1, 
                            width=0.4))
    fig.update_layout(
        xaxis_title='Sentiment',
        yaxis_title='Score',
        width=500,
        height=600,
        boxmode='group',
        showlegend=False
    )

    return fig

# heatmap of mean score by day and by sentiment
def get_heatmap_score(df):

    freq_option = get_freq_option(8)

    # Group by day and sentiment, calculate the mean score, and pivot the table
    df_data_heatmap = df.groupby([pd.Grouper(key='date_tweet', freq=freq_option), 'sentiment']) \
                        .agg({'score': 'mean'}) \
                        .reset_index() \
                        .pivot(index='sentiment', columns='date_tweet', values='score')


    # create a heatmap
    fig = go.Figure(
        data=go.Heatmap(
        z=df_data_heatmap.values,
        x=df_data_heatmap.columns,
        y=df_data_heatmap.index,
        colorscale='plasma')
    )
    
    fig.update_layout(
        xaxis_title='Sentiment',
        yaxis_title='Date',
        height=500,
        autosize=True,
    )
    return fig


#  heat map of number of tweets by hour and by sentiment
def get_heatmap_nb_tweets(df):
    df['jour_semaine'] = pd.to_datetime(df['date_tweet']).dt.day_name()
    df['heure'] = pd.to_datetime(df['date_tweet']).dt.hour

    # Create a dataframe regroup by day and hour and sentiment and calculate the number of tweets
    df_heatmap = df.groupby(['jour_semaine', 'heure', 'sentiment'])\
        .agg({'sentiment': 'size'})\
        .rename(columns={'sentiment':'count'})\
        .reset_index()

    fig = go.Figure(data=go.Heatmap(
                    z=df_heatmap['count'],
                    x=df_heatmap['heure'], 
                    y=df_heatmap['sentiment'],
                    colorscale='plasma',
                    hoverongaps = False))
    

    fig.update_traces(hovertemplate='Heure: %{x}<br>Nombre de tweets: %{z}')

    fig.update_layout(
        xaxis_title='Heure',
        yaxis_title='Sentiment',
        width=550,
        height=500,
        autosize=True,
    )
    return fig
