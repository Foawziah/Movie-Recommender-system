
from surprise import Reader
import pandas as pd
import numpy as np
from surprise import SVD
from surprise import Dataset
from collections import defaultdict
movies = pd.read_csv('movies.csv') 
ratings_df = pd.read_csv("ratings.csv")

reader = Reader(rating_scale=(0.5, 5)) #line_format by default order of the fields

# Surprise Dataset Load method
data = Dataset.load_from_df(ratings_df[["userId","movieId","rating"]], reader=reader)

trainset = data.build_full_trainset()

testset = trainset.build_anti_testset()

testset = data.build_full_trainset().build_testset()
# Train the SVD model
svd = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.4)
svd.fit(trainset)
# Generate the predictions using the SVD model
predictions = svd.test(testset)


def get_top_n(predictions, userId, movies, ratings, n = 10):
    '''Return the top N (default) movieId for a user,.i.e. userID and history for comparisom
    Args:
    Returns: 
  
    '''
    
    #First map the predictions to each user.
    
"""
UTILS 
- Helper functions to use for your recommender funcions, etc
- Data: import files/models here e.g.
    - movies: list of movie titles and assigned cluster
    - ratings
    - user_item_matrix
    - item-item matrix 
- Models:
    - nmf_model: trained sklearn NMF model
"""




def movie_to_id(string_titles):
    '''
    converts movie title to id for use in algorithms'''
    
    movieID = movies.set_index('title').loc[string_titles]['movieId']
    movieID = movieID.tolist()
    
    return movieID

def id_to_movie(movieID):
    '''j
    converts movie Id to title
    '''
    rec_title = movies.set_index('movieId').loc[movieID]['title']
    
    return rec_title

def rating_to_id(string_titles):
    '''
    converts movie title to id for use in algorithms'''
    
    ratingId = ratings.set_index('title').loc[string_titles]['movieid']
    ratingId = ratings.tolist()
    
    return ratingId