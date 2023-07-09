import pathlib
import streamlit as st
import pandas as pd
import os

import re
import spacy
import spacy.cli
from nltk.corpus import stopwords
import nltk

def load_nltk():

    if not pathlib.Path("./nltk").exists():
        os.mkdir("./nltk")

        # download stopwords
        spacy.cli.download("fr_core_news_sm")
        nltk.download('stopwords', download_dir="./nltk")
    
    # download model for french language
    nlp = spacy.load("fr_core_news_sm")
    nltk.data.path.append("./nltk")
    stopWords = set(stopwords.words('french'))

    return nlp, stopWords



# Tokenise sentence
def token_text(sentence, nlp):
    doc = nlp(sentence)
    return [X.text for X in doc]



# remove stopwords
def format_text_freq_words(text):
    # remove alla caract usefull for the analysis
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[?\%\(\)\/\|\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)
    text = re.sub(r"httpst.co", "", text)

    return text


# collect fréquents words in tweets
@st.cache_data
def get_frequent_words(df):

    # Load frequent words
    nlp, stopWords = load_nltk()

    list_freq_words_fr = ["oeclfybyif", "agindre", "après", "plus", "ans", "qu'", "qu’", "...", "avoir", "deux", "fait", "selon", "faire", "cette", "entre", "veut", "être", "tout", "depuis", "trois", "moins", "très", "lors", "mois", "avant", "sans", "faut", "cet", "peut", "près", "chez", "jusqu'",
                        "sous", "vers", "mis", "tous", "soir", "vais", "dit", "comme", "mecredi", "janvier", "toutes", "fois", "devant", "sait", "pendant", "leurs", "leur", "vont", "dont", "malgré", "quand", "quoi", "quel", "met", "doit", "mardi", "demain", "déjà", "dés", "toute", "trop", "lundi", "peux"]
    
    # in variable list_tweets retrieve columns text_tweet of df
    list_tweets = df[['text_formatted_tweet']].values.tolist()

    dict_words = {}

    for text in list_tweets:
        format_text = format_text_freq_words(text[0])

        # Remove frequents words FR with stopWords
        clean_words = [token for token in token_text(format_text, nlp) if token not in stopWords]

        list_words = [word for word in clean_words if len(
            word) > 2 and word not in list_freq_words_fr]

        # sum duplicate words and add it in dict
        for x in list_words:
            if x in dict_words:
                dict_words[x] += 1
            else:
                dict_words[x] = 1

    df_words = pd.DataFrame(dict_words.items(), columns=['text', 'value'])

    list_frequent_words = df_words.sort_values(by='value', ascending=False).head(200).to_dict('records')

    return list_frequent_words
