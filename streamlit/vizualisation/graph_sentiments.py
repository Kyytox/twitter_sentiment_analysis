import datetime
import streamlit as st
import pandas as pd


# lib for graphs
import plotly.express as px
import plotly.graph_objects as go

# functions 
from vizualisation.process_graph import *
from vizualisation.widgets import get_freq_option, create_year_month_selection


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

    return fig


# Bar charts 
# number of tweets by Sentiments 
def get_bar_charts_by_sent(df):
    data_bar = get_nb_tweets_sent(df)
    fig = px.bar(data_bar, x='sentiment', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets analysés'}, text='nb_tweets')
    fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    return fig




# Score line chart
# Mean of score by freq_option and by sentiment
def get_line_chart_score(df):

    freq_option = get_freq_option(1)

    # group dataframe by day and sentiment and calculate the mean of score 
    # create a new data frame with 3 columns [date_tweet sentiment score]
    df_data_line = df.groupby([pd.Grouper(key='date_tweet',freq=freq_option), 'sentiment']).agg({'score': 'mean'}).reset_index()

    fig = px.line(df_data_line, 
                x='date_tweet', 
                y='score', 
                color='sentiment', 
                color_discrete_sequence=colors, 
                labels={'score':'Score moyen'},
                width=800,
                height=600)
    fig.update_traces(mode='lines+markers')
    return fig



# Bar Charts Day
# Number of tweets by day
def get_bar_charts_day(df):
    # group dataframe by month and sentiment and count the nb of tweets  
    # create a new data frame with 3 columns [date_tweet sentiment count]
    df_data_bar_month = df.groupby([pd.Grouper(key='date_tweet',freq='M'), 'sentiment']).agg({'sentiment': 'size'}).rename(columns={'sentiment':'nb_tweets'}).reset_index()

    # create slide menu with year 
    # create calendar with month  
    this_year = datetime.date.today().year

    report_year = st.selectbox('', range(this_year, this_year - 4, -1), index=1, key=5)
    # report_year = get_selected_year(this_year)

    data = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y").str.startswith(f'{report_year}')]

    fig = px.bar(data, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets'},text='nb_tweets')
    fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    return fig



# Bar Charts Month 
# Number of tweets by month
# def get_bar_charts_month_(df):
#     # group dataframe by day and sentiment and count the nb of tweets  
#     # create a new data frame with 3 columns [date_tweet sentiment count]
#     df_data_bar_month = df.groupby([pd.Grouper(key='date_tweet',freq='D'), 'sentiment']).agg({'sentiment': 'size'}).rename(columns={'sentiment':'nb_tweets'}).reset_index()
#     # filter dataframe by year and month
#     df_data_bar_month = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

#     fig = px.bar(df_data_bar_month, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweetswwwwww '},text_auto=True)
#     fig.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
#     return fig


def get_bar_charts_month(df):
    # Group dataframe by day and sentiment and count the number of tweets
    # Create a new data frame with 3 columns [date_tweet sentiment count]
    df_data_bar_month = df.groupby([pd.Grouper(key='date_tweet', freq='D'), 'sentiment']) \
                            .agg({'sentiment': 'size'}) \
                            .rename(columns={'sentiment': 'nb_tweets'}) \
                            .reset_index()

    # Create year and month selection widgets
    report_year, report_month = create_year_month_selection()

    # Filter dataframe by year and month
    df_data_bar_month = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

    # Create a bar chart
    fig = px.bar(df_data_bar_month, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets'}, text_auto=True)
    fig.update_traces(textfont_size=14, textangle=0, cliponaxis=False)

    return fig

# box charts of score by sentiment
def get_box_charts_score(df):
    # regroup df by sentiment 
    df_data_box = df.groupby(['sentiment']).agg({'score': ['mean', 'median', 'min', 'max', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]}).reset_index()
    fig = go.Figure()

    # add trace for each sentiment
    for count_color, sentiment in enumerate(df_data_box['sentiment'].unique()):
        # extract all score for the sentiment and place them in a list
        data = df_data_box[df_data_box['sentiment'] == sentiment]['score'].values
        data = str(data)

        # Supprimer les crochets [ ] et diviser les valeurs en une liste
        list_data = data.strip('[]').split()

        # Convertir les éléments de la liste en flottants
        list_data = [float(x) for x in list_data]

        print(list_data)

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
        title='Box plot of score by sentiment',
        xaxis_title='Sentiment',
        yaxis_title='Score',
        width=500,
        height=600,
        boxmode='group'
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
        title='Heatmap of mean score by day and by sentiment',
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
        title='Heatmap of mean score by day and by sentiment',
        xaxis_title='Heure',
        yaxis_title='Sentiment',
        width=550,
        height=500,
        autosize=True,
    )
    return fig
