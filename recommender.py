"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import pandas as pd
import numpy as np
from utils import movies, ratings_df
from collections import defaultdict
from surprise import Reader
from surprise import accuracy
from surprise.prediction_algorithms.random_pred import NormalPredictor
import seaborn as sns
from surprise.model_selection.split import train_test_split
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
import pickle
with open('svd_model.pkl','rb') as file:
    svd = pickle.load(file)

def recommend_random(k=3):
    return movies['title'].sample(k).to_list()

def get_top_n(userId, movies, ratings, n = 10):
    '''Return the top N (default) movieId for a user,.i.e. userID and history for comparisom
    Args:
    Returns: 
  
    '''
    
    #First map the predictions to each user.
    top_n = defaultdict(list)
    reader = Reader(rating_scale=(0.5, 5)) #line_format by default order of the fields

# Surprise Dataset Load method
    data = Dataset.load_from_df(ratings[["userId","movieId","rating"]], reader=reader)

    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()

    # Define the testset
    testset = data.build_full_trainset().build_testset()
# Train the SVD model
# Generate the predictions using the SVD model
    predictions = svd.test(testset)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    #Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key = lambda x: x[1], reverse = True)
        top_n[uid] = user_ratings[: n ]
    
    
    #Tells how many movies the user has already rated
    user_data = ratings[ratings.userId == (userId)]
    print('User {0} has already rated {1} movies.'.format(userId, user_data.shape[0]))

    
    #4. Data Frame with predictions. 
    preds_df = pd.DataFrame([(id, pair[0],pair[1]) for id, row in top_n.items() for pair in row],
                        columns=["userId" ,"movieId","rat_pred"])
    
    
    #Return pred_usr, i.e. top N recommended movies with (merged) titles and genres. 
    pred_usr = preds_df[preds_df["userId"] == (userId)].merge(movies, how = 'left', left_on = 'movieId', right_on = 'movieId')
            
    #Return hist_usr, i.e. top N historically rated movies with (merged) titles and genres for holistic evaluation
    old_usr = ratings[ratings.userId == (userId) ].sort_values("rating", ascending = False).merge\
    (movies, how = 'left', left_on = 'movieId', right_on = 'movieId')
    
    
    return old_usr, pred_usr
    

def recommend_neighborhood(query, model, k=3):
    """
    Filters and recommends the top k movies for any given input query based on a trained nearest neighbors model. 
    Returns a list of k movie ids.
    """   
    pass
    
