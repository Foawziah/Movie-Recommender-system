from flask import Flask,render_template,request
from recommender import recommend_random,recommend_neighborhood,  get_top_n
from utils import movies, movie_to_id,id_to_movie, ratings_df

app = Flask(__name__)

@app.route('/')
def hello():
    # print(movies.title.to_list())
    return render_template('index.html', name='Foawzi', movies=movies.title.to_list())

@app.route('/movies')
def recommendation():
    print(request.args)

    if request.args.get('option') =='Random':
        recommendation_list = recommend_random()
        print(recommendation_list)
        userid = request.args.getlist('userid')
        print(userid)
        print(int(userid[0]))
        titles = request.args.getlist('title')
        ratings = request.args.getlist('rating')
        movieid = movie_to_id(titles[0])
        query = {'userId': int(userid[0]), 'movieId': movieid[0], 'rating': ratings_df}

        # for movie in query:
        #     query[movie] = float(query[movie])


        
        print(query)

        return render_template('recommend.html', recommendation=recommendation_list)
    
    if request.args.get('option') =='SVD':
        #print(recommendation_list)

        titles = request.args.getlist('title')
        ratings = request.args.getlist('rating')
        
        query = dict(zip(titles,ratings))

        for movie in query:
            query[movie] = float(query[movie])
        
        print(query)
        old_SVD, pred_SVD = get_top_n(movies = movies, userId = 1, ratings = ratings_df)
        recomm_movie =[]
        for title in pred_SVD.movieId.to_list():
            recomm_movie.append(id_to_movie(title))
            # print(recomm_movie)

        return render_template('recommend.html', recommendation=recomm_movie)
    
    else:
        recommendation_list = recommend_neighborhood()
        return f'Function not defined'

if __name__=='__main__':
    app.run(port=5001,debug=True)
    