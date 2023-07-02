import streamlit as st
import matplotlib.pyplot as plt

##################################################
# Graphs frequent words


# Word Cloud
def _get_wordcloud(wordcloud):
    # Display the generated Word Cloud
    fig, ax = plt.subplots(figsize = (4, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.margins(x=0, y=0)
    st.subheader('Mots les plus fréquents')
    st.pyplot(fig)
