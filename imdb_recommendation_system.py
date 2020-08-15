#!/usr/bin/env python
# coding: utf-8
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

###########################################################################################################

  # CHECK THE NOTEBOOK FILE (notebooks/movie-recommendation-system.ipynb) FOR EXPLANATION OF THIS CODE #

###########################################################################################################


imdb = pd.read_csv('dataset/imdb_sampled.csv')
titles_list = imdb['sortedTitle'].tolist()
cv = CountVectorizer(dtype=np.uint8)
dtm = cv.fit_transform(imdb['genres']).toarray()
new_matrix = np.concatenate((dtm, np.array(imdb['averageRating']).reshape(-1, 1)), axis=1)

MMS = MinMaxScaler()
numVotes = np.array(imdb['numVotes'])
numVotes = numVotes.reshape(-1, 1)
numVotes = MMS.fit_transform(numVotes)
new_matrix = np.concatenate((new_matrix, numVotes), axis=1)

similarities = cosine_similarity(new_matrix, dense_output=False)


def build_recommendations(title):
    try:
        title = title.lower()
        tv_shows = ['tvSeries', 'tvMovie', 'tvMiniSeries', 'video', 'tvSpecial']
        sorted_title_found = True in [True for t in imdb['sortedTitle'] if t.lower() == title]
        if sorted_title_found:
            idx = imdb[imdb['sortedTitle'].apply(lambda x: x.lower()) == title].index[0]
        else:
            idx = imdb[imdb['primaryTitle'].apply(lambda x: x.lower()) == title].index[0]

        recommendations = imdb['sortedTitle'].iloc[similarities[idx].argsort()[::-1]][0:500]

        if imdb.iloc[idx]['titleType'] in tv_shows:
            tv_recommendations = {rec: [imdb['tconst'].iloc[rec], imdb['sortedTitle'].iloc[rec]] for rec in
                                  recommendations.index if imdb['titleType'].iloc[rec] in tv_shows}
            return pd.DataFrame(tv_recommendations).transpose().iloc[1:11]

        else:
            movie_recommendations = {rec: [imdb['tconst'].iloc[rec], imdb['sortedTitle'].iloc[rec]] for rec in
                                     recommendations.index if imdb['titleType'].iloc[rec] == 'movie'}
            return pd.DataFrame(movie_recommendations).transpose().iloc[1:11]
    except:
        return None


def get_recommendations(title):
    recommendations = build_recommendations(title)
    if recommendations is None:
        return recommendations
    else:
        recommendations.rename(columns={0: 'tconst', 1: 'title'}, inplace=True)
        recommendations.reset_index(drop=True, inplace=True)
        recommendations['urls'] = [f'https://www.imdb.com/title/{title_id}/' for title_id in recommendations['tconst']]
        return recommendations.drop('tconst', axis=1)


def get_movie_data():
    return titles_list
