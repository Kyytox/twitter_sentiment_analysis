import streamlit as st

# lib for graphs
from wordcloud import WordCloud

# functions 
import vizualisation.process_graph as pg
import vizualisation.frequents_words as fw
import vizualisation.graph_sentiments as gs
import vizualisation.graph_interactions as gi
import vizualisation.graph_frequent_words as gfw



def display_graph(df):   
    current_tab = st.sidebar.radio("Sélectionnez une section :", ["Sentiments", "Interactions", "Frequent Words"])
    
    if current_tab == "Sentiments":
        load_data(df, "Sentiments")
    elif current_tab == "Interactions":
        load_data(df, "Interactions")
    elif current_tab == "Frequent Words":
        load_data(df, "Frequent Words")



def load_data(df, tab):
    if tab == "Sentiments":
        tabs_sentiments(df)
    elif tab == "Interactions":
        tabs_interactions(df)
    elif tab == "Frequent Words":
        tabs_frequent_words(df)


##################################################
# Tabs Sentiments 

def tabs_sentiments(df):

    col1, col2 = st.columns([7,10])
    with col1:
        # display the graph box of the score
        st.subheader('Boîte à moustache des scores par sentiment')
        st.plotly_chart(gs._get_box_charts_score(df))

        # display the graph heatmap of the number of tweets
        st.subheader('Heatmap du nombre de tweets par sentiment')
        st.plotly_chart(gs._get_heatmap_nb_tweets(df))

    with col2:
        # display the graoh heatmap of the score
        st.subheader('Heatmap des scores par sentiment')
        st.plotly_chart(gs._get_heatmap_score(df))



    #  display the graph line of the score
    st.subheader('Moyenne des scores par sentiment')
    st.plotly_chart(gs._get_line_chart_score(df),use_container_width=True)

    # Graph 1 - 2
    col1, col2 = st.columns([7,10])
    with col1:
        # Pie charts
        # distribution of the number of tweets by sentiments
        col1.plotly_chart(gs._get_pie_charts_by_sent(df),use_container_width=True)
    with col2:
        # Bar charts
        # number of tweets by Sentiments
        gs._get_bar_charts_by_sent(df)


    # Graph 3 - 4
    col3, col4 = st.columns([7,10])
    with col3:
        # Bar Charts Month
        # Number of tweets by month
        gs._get_bar_charts_day(df)
    with col4:
        # Bar Charts Day
        # Number of tweets by day
        gs._get_bar_charts_month(df)




##################################################
# Graphs interactions 

def tabs_interactions(df):
    #  display the graph line of the sum of interactions
    st.subheader('Somme des interactions')
    st.plotly_chart(gi._get_line_chart_interactions(df),use_container_width=True)


    with st.container():
        df_data_interac = pg.get_data_interactions(df)
        col5, col6 = st.columns(2)
        with col5:
            gi._get_bar_charts_interactions(df_data_interac)

        with col6:
            gi._get_pie_charts_interactions(df_data_interac)



##################################################
# Graphs frequent words

def tabs_frequent_words(df):
    # with st.spinner("Loading word cloud ..."):
    list_frequent_words = fw.get_frequent_words(df)
    text_wordCloud = ' '.join([f"{d['text']} " * d['value'] for d in list_frequent_words])
    wordcloud = WordCloud(width=600, height=400, max_font_size=90, collocations=False, colormap="Reds").generate(text_wordCloud)

    with st.container():
        gfw._get_wordcloud(wordcloud)

