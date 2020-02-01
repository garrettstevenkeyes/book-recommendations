import streamlit as st
import pandas as pd
import requests
import csv
import numpy as np
from urllib.request import Request, urlopen
import ast
import re
import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from spacy.matcher import Matcher
from gensim import corpora
import pickle
import gensim
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from statistics import mean, median, mode
import unicodedata
from spacy import displacy
import inflect
from pprint import pprint
import explacy
import seaborn as sns

# --------------  recommendation function --------------
#load dataset
model_df = pd.read_csv('tokenized_model.csv')
model_df = model_df.where((pd.notnull(model_df)), None)
model_df.set_index('title',inplace=True)
#load pickle
cosine_sim = pickle.load(open('rec_cosine_sim.pkl', 'rb'))

recommendation_list = []
plot_list = []

indices = pd.Series(model_df.index)
df_names = list(model_df['name'])
#define rec function
def recommendation(title, input_media_type,cosine_sim=cosine_sim):
    recommendations = []

    #getting the index of the movie that matches the title

    #If the desired output is a movie return a movie
    idx = indices[indices == title].index[0]

    #creating a series with the similarty scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    top_10_indexes = list(score_series.iloc[1:1000].index)

    #wcreate a unique id for each entry and write a search function
    for item in top_10_indexes:
        recommendations.append(list(model_df.index)[item])

    #only get movies if a movie is asked for
    if input_media_type == 'movie':
        recs = []
        for index1,rec in enumerate(recommendations):
            movie_title = rec
            for index2,name in enumerate(df_names):
                if name == movie_title:
                    movie_index = index2
                    searched_movie_title = model_df['name'][movie_index]
                    categorization = model_df['media_type'][movie_index]
                    if categorization != 'movie':
                        pass
                    else:
                        film_title = model_df['name'][movie_index]
                        film_score = model_df['score'][movie_index]
                        selected_image = model_df['image'][movie_index]
                        selected_plot = model_df['plot'][movie_index]
                        recs.append(searched_movie_title)
                        recommendation_list.append(searched_movie_title)
                        plot_list.append(selected_plot)
        # return recs

    #only get tv shows if a tv show is asked for
    if input_media_type == 'tv':
        recs = []
        for index1,rec in enumerate(recommendations):
            tv_title = rec
            for index2,name in enumerate(df_names):
                if name == tv_title:
                    tv_index = index2
                    searched_tv_title = model_df['name'][tv_index]
                    categorization = model_df['media_type'][tv_index]
                    if categorization != 'tv':
                        pass
                    else:
                        tv_title = model_df['name'][tv_index]
                        tv_score = model_df['score'][tv_index]
                        selected_tv_image = model_df['image'][tv_index]
                        selected_tv_plot = model_df['plot'][tv_index]
                        recs.append(searched_tv_title)
                        recommendation_list.append(searched_tv_title)
                        plot_list.append(selected_tv_plot)
        # return recs

    #only get books if a book is asked for
    if input_media_type == 'book':
        recs = []
        for index1,rec in enumerate(recommendations):
            book_title = rec
            for index2,name in enumerate(df_names):
                if name == book_title:
                    book_index = index2
                    searched_book_title = model_df['name'][book_index]
                    categorization = model_df['media_type'][book_index]
                    if categorization != 'book':
                        pass
                    else:
                        book_title = model_df['name'][book_index]
                        book_score = model_df['score'][book_index]
                        selected_book_image = model_df['image'][book_index]
                        selected_book_plot = model_df['plot'][book_index]
                        recs.append(searched_book_title)
                        recommendation_list.append(searched_book_title)
                        plot_list.append(selected_book_plot)
        # return recs

#------------------------------------------------------------------------

#-------------- Stream Lit dashboard ------------------------------------

my_dataset = 'tokenized_model.csv'
movie_dataset = 'formatted_movies.csv'
tv_dataset = 'formatted_tv.csv'
book_dataset = 'books.csv'

#Fxn to Load Dataset
@st.cache(persist=True)
def explore_data(dataset):
    df = pd.read_csv(dataset)
    df = df.where((pd.notnull(df)), None)
    # movie_df = pd.read_csv('movie.csv')
    # tv_df = pd.read_csv('tv.csv')
    # books_df = pd.read_csv('books.csv')
    return df

def rec_fxn(title, what_you_want):
    recommendation(title, what_you_want)
    st.write(recommendation_list[:10])
    st.write(plot_list[:10])

data = explore_data(my_dataset)
movie_data = explore_data(movie_dataset)
tv_data = explore_data(tv_dataset)
book_data = explore_data(book_dataset)

#Text/Title
st.title('What do you want to watch, or read?')
st.text('By Garrett Keyes')

st.subheader('Goodreads and Netflix Dataset')
if st.checkbox('Show Dataset'):
    if st.button('Head'):
        st.write(data.head())
    elif st.button('Tail'):
        st.write(data.tail())

#select box with list of Title
media_in_mind = st.selectbox('What do you want your recommendations to be based off?', ('Movie', 'TV', 'Book'))

if media_in_mind == 'Movie':
    st.write(movie_data.title)

elif media_in_mind == 'TV':
    st.write(tv_data.title)

elif media_in_mind == 'Book':
    st.write(book_data.name)

#Button
title = st.text_input('Your title here')
what_you_want = st.text_input('Do you want a movie, tv show, or book?')

if title and what_you_want:
    st.text('Here are your top 10 recommendations!')
    st.write(rec_fxn(title, what_you_want))
    st.balloons()
