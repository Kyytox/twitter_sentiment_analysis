import streamlit as st
import matplotlib.pyplot as plt

# lib for graphs
from wordcloud import WordCloud

# functions 
import vizualisation.utils_frequents_words as fw
import vizualisation.graph_sentiments as gs
import vizualisation.graph_interactions as gi
import vizualisation.utils as ut 


#####################s
# Graphs Sentiments #
#####################
def tabs_sentiments(df):

    col1, col2 = st.columns([5,6])
    with col1:
        st.subheader('Distribution of the number of tweets by sentiments')
        st.plotly_chart(gs.get_pie_charts_by_sent(df))
    with col2:
        st.subheader('Number of tweets by Sentiments')
        st.plotly_chart(gs.get_bar_charts_by_sent(df))

    st.subheader('Heatmap of feelings by feeling')
    st.plotly_chart(gs.get_heatmap_score(df),use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Mustache box of feelings by feeling')
        st.plotly_chart(gs.get_box_charts_score(df))
    with col4:
        st.subheader('Heatmap of the number of tweets per feeling')
        st.plotly_chart(gs.get_heatmap_nb_tweets(df))


    st.subheader('Average scores by feeling')
    st.plotly_chart(gs.get_line_chart_score(df),use_container_width=True)

    st.subheader('Number of tweets by month')
    st.plotly_chart(gs.get_bar_charts_month(df) ,use_container_width=True)

    st.subheader('Number of tweets by day')
    st.plotly_chart(gs.get_bar_charts_day(df) ,use_container_width=True)
    



#######################
# Graphs interactions #
#######################
def tabs_interactions(df):
    #  display the graph line of the sum of interactions
    st.subheader('Sum of interactions')
    st.plotly_chart(gi.get_line_chart_interactions(df),use_container_width=True)

    with st.container():
        df_data_interac = ut.get_data_interactions(df)
        col5, col6 = st.columns(2)
        with col5:
            st.subheader('Bar: Number of interactions by sentiment')
            st.plotly_chart(gi.get_bar_charts_interactions(df_data_interac))

        with col6:
            st.subheader('Pie: Number of interactions by sentiment')
            st.plotly_chart(gi.get_pie_charts_interactions(df_data_interac))



#########################
# Graphs frequent words #
#########################
def tabs_frequent_words(df):
    list_frequent_words = fw.get_frequent_words(df)
    text_wordCloud = ' '.join([f"{d['text']} " * d['value'] for d in list_frequent_words])
    
    # generate wordcloud
    wordcloud = WordCloud(width=600, 
                        height=400, 
                        max_font_size=40, 
                        collocations=False, 
                        colormap="Reds",
                        contour_width=1,
                        ).generate(text_wordCloud)

    with st.container():
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.margins(x=0, y=0)
        st.subheader('Most frequent words')
        st.pyplot(fig)
