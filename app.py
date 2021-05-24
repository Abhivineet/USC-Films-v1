from flask import Flask, jsonify, request, send_file
import requests
import json

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "c7678dbba6272b0fd8397ddd755e6a3a"
app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/get_home_data')
def get_home_data():
    home_movies = json.loads(requests.get(BASE_URL + "/trending/movie/week?api_key=" + API_KEY).content)
    movie_data = []
    for i in range(5):
        temp = {
            'title' : home_movies['results'][i]['title'] if 'title' in home_movies['results'][i] and home_movies['results'][i]['title'] != None and home_movies['results'][i]['title']!= "" else "N/A" ,
            'backdrop_path' : "https://image.tmdb.org/t/p/w780" + str(home_movies['results'][i]['backdrop_path']) if 'backdrop_path' in home_movies['results'][i] and home_movies['results'][i]['backdrop_path'] != None and home_movies['results'][i]['backdrop_path']!= "" else "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg",
            'year' : home_movies['results'][i]['release_date'].split('-')[0] if 'release_date' in home_movies['results'][i] and home_movies['results'][i]['release_date'] != None and home_movies['results'][i]['release_date']!="" else "N/A"   
        }
        movie_data.append(temp)
    home_tv = json.loads(requests.get(BASE_URL + "/tv/airing_today?api_key=" + API_KEY).content)
    tv_data = []
    for i in range(5):
        temp = {
            'name' : home_tv['results'][i]['name'] if 'name' in home_tv['results'][i] and home_tv['results'][i]['name'] != None and home_tv['results'][i]['name']!= "" else "N/A" ,
            'backdrop_path' : "https://image.tmdb.org/t/p/w780" + str(home_tv['results'][i]['backdrop_path']) if 'backdrop_path' in home_tv['results'][i] and home_tv['results'][i]['backdrop_path'] != None and home_tv['results'][i]['backdrop_path']!= "" else "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg",
            'year' : home_tv['results'][i]['first_air_date'].split('-')[0] if 'first_air_date' in home_tv['results'][i] and home_tv['results'][i]['first_air_date'] != None and home_tv['results'][i]['first_air_date']!="" else "N/A"   
        }
        tv_data.append(temp)
    response = {"movie": movie_data, "tv": tv_data}
    return jsonify(response)

@app.route('/search_movie')
def search_movie():
    query = request.args.get('query')
    movie_genres_dict = {}
    genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=97aae9f589f28a66fa4986f887e2362a").content)
    for g in genres['genres']:
        movie_genres_dict[g['id']] = g['name']
    results = json.loads(requests.get("https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + query + "&language=en-US&page=1&include_adult=false").content)
    results = results['results']
    search_results = []
    for item in results[:10]:
        temp = {
            'id': str(item['id']) if  'id' in item and item['id']!=None and item['id'] != "" else "N/A", 
            'title': item['title'] if  'title' in item  and item['title'] != None and item['title'] != "" else "",
            'overview': item['overview'] if 'overview' in item  and item['overview']!= None and item['overview'] != "" else "",
            'poster_path': item['poster_path'] if 'poster_path' in item else "N/A",
            'year':item['release_date'].split('-')[0] if 'release_date' in item and item['release_date'] != None and item['release_date']!= "" else "",
            'vote_average': str(round(item['vote_average']/2, 1)) + "/5" if 'vote_average' in item and item['vote_average'] != None and item['vote_average'] != "" else "",
            'vote_count': str(item['vote_count']) + ' Votes' if 'vote_count' in item and item['vote_count'] != None and item['vote_count'] != "" else "",
            'genre_ids': item['genre_ids'] if 'genre_ids' in item and item['genre_ids']!=None and item['genre_ids']!="" else "",
            'type':'movie'
            }
        if temp['genre_ids'] !="":
            t = []
            for i in temp['genre_ids']:
                t.append(movie_genres_dict[i])
            temp['genre_ids'] = ', '.join(t)
            
        if temp['poster_path']==None or temp['poster_path']=="" or temp['poster_path']=="N/A":
            temp['poster_path']="https://cinemaone.net/images/movie_placeholder.png"
        else:
            temp['poster_path'] = "https://image.tmdb.org/t/p/w185" + temp['poster_path']
        info = temp['year'] + " | " + temp['genre_ids']
        temp['info'] = info
        search_results.append(temp)
    return jsonify(search_results)

@app.route('/search_tv')
def search_tv():
    query = request.args.get('query')
    results = json.loads(requests.get("https://api.themoviedb.org/3/search/tv?api_key=" + API_KEY + "&query=" + query + "&language=en-US&page=1&include_adult=false").content)
    genres_dict = {}
    genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=97aae9f589f28a66fa4986f887e2362a").content)
    for g in genres['genres']:
        genres_dict[g['id']] = g['name']
    results = results['results']
    search_results = []
    for item in results[:10]:
        temp = {
            'id': str(item['id']) if 'id' in item and item['id'] != None and item['id'] != "" else "",
            'title': item['name'] if 'name' in item and item['name'] != None and item['name'] != "" else "",
            'overview': item['overview'] if 'overview' in item and item['overview'] != None and item['overview'] != "" else "",
            'poster_path': item['poster_path'] if 'poster_path' in item else "N/A",
            'year': item['first_air_date'].split('-')[0] if 'first_air_date' in item and item['first_air_date']!= None and item['first_air_date'] != "" else "",
            'vote_average': str(round(item['vote_average']/2, 1)) + "/5" if 'vote_average' in item and item['vote_average'] != None and item['vote_average'] != "" else "",
            'vote_count': str(item['vote_count']) + ' Votes' if 'vote_count' in item and item['vote_count'] != None and item['vote_count'] != "" else "",
            'genre_ids': item['genre_ids'] if 'genre_ids' in item and item['genre_ids']!= None and item['genre_ids'] != "" else "",
            'type':'tv'
            }
        if temp['genre_ids'] !="":
            t = []
            for i in temp['genre_ids']:
                t.append(genres_dict[i])
            temp['genre_ids'] = ', '.join(t)
        if temp['poster_path']==None or temp['poster_path']=="" or temp['poster_path']=="N/A":
            temp['poster_path']="https://cinemaone.net/images/movie_placeholder.png"
        else:
            temp['poster_path'] = "https://image.tmdb.org/t/p/w185" + temp['poster_path']
        info = temp['year'] + " | " + temp['genre_ids']
        temp['info'] = info
        search_results.append(temp)
    return jsonify(search_results)

@app.route('/search_multi')
def search_multi():
    query = request.args.get('query')
    results = json.loads(requests.get("https://api.themoviedb.org/3/search/multi?api_key=" + API_KEY + "&language=en-US&query=" + query + "&page=1&include_adult=false").content)
    results = results['results']
    movie_genres_dict = {}
    genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=97aae9f589f28a66fa4986f887e2362a").content)
    for g in genres['genres']:
        movie_genres_dict[g['id']] = g['name']
    tv_genres_dict = {}
    genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=97aae9f589f28a66fa4986f887e2362a").content)
    for g in genres['genres']:
        tv_genres_dict[g['id']] = g['name']
    search_results = []
    for item in results:
        if len(search_results)==10:
            break
        if item['media_type']=='tv':
            temp = {
                'id': str(item['id']) if 'id' in item and item['id'] != None and item['id'] != "" else "",
                'title': item['name'] if 'name' in item and item['name'] != None and item['name'] != "" else "",
                'overview': item['overview'] if 'overview' in item and item['overview'] != None else "",
                'poster_path': item['poster_path'] if 'poster_path' in item else "N/A",
                'year': item['first_air_date'].split('-')[0] if 'first_air_date' in item and item['first_air_date']!= None and item['first_air_date'] != "" else "",
                'vote_average': str(round(item['vote_average']/2, 1)) + "/5" if 'vote_average' in item and item['vote_average'] != None and item['vote_average'] != "" else "",
                'vote_count': str(item['vote_count']) + ' Votes' if 'vote_count' in item and item['vote_count'] != None and item['vote_count'] != "" else "",
                'genre_ids': item['genre_ids'] if 'genre_ids' in item and item['genre_ids']!= None and item['genre_ids'] != "" else "",
                'type':'tv'
                }
            if temp['genre_ids'] !="":
                t = []
                for i in temp['genre_ids']:
                    t.append(tv_genres_dict[i])
                temp['genre_ids'] = ', '.join(t)
        elif item['media_type']=='movie':
            temp = {
                'id': str(item['id']) if  'id' in item and item['id']!=None and item['id'] != "" else "", 
                'title': item['title'] if  'title' in item  and item['title'] != None and item['title'] != "" else "",
                'overview': item['overview'] if 'overview' in item  and item['overview']!= None and item['overview'] != "" else "",
                'poster_path': item['poster_path'] if 'poster_path' in item else "N/A",
                'year':item['release_date'].split('-')[0] if 'release_date' in item and item['release_date'] != None and item['release_date']!= "" else "",
                'vote_average': str(round(item['vote_average']/2, 1)) + "/5" if 'vote_average' in item and item['vote_average'] != None and item['vote_average'] != "" else "",
                'vote_count': str(item['vote_count']) + ' Votes' if 'vote_count' in item and item['vote_count'] != None and item['vote_count'] != "" else "",
                'genre_ids': item['genre_ids'] if 'genre_ids' in item and item['genre_ids']!=None and item['genre_ids']!="" else "",
                'type':'movie'
                }
            if temp['genre_ids'] != "":
                t = []
                for i in temp['genre_ids']:
                    t.append(movie_genres_dict[i])
                temp['genre_ids'] = ', '.join(t)
        else:
            continue
        if temp['poster_path']==None or temp['poster_path']=="" or temp['poster_path']=="N/A":
            temp['poster_path']="https://cinemaone.net/images/movie_placeholder.png"
        else:
            temp['poster_path'] = "https://image.tmdb.org/t/p/w185" + temp['poster_path']
            
        info = temp['year'] + " | " + temp['genre_ids']
        temp['info'] = info
        search_results.append(temp)
    return jsonify(search_results)


@app.route('/id_search')
def id_search():
    id = request.args.get('id')
    type = request.args.get('type')
    url1="https://api.themoviedb.org/3/" + type + "/" + id + "?api_key=" + API_KEY + "&language=en-US"
    url2 = "https://api.themoviedb.org/3/" + type + "/" + id + "/credits?api_key=" + API_KEY + "&language=en-US"
    url3 = "https://api.themoviedb.org/3/" + type + "/" + id + "/reviews?api_key=" + API_KEY + "&language=en-US&page=1"
    media = json.loads(requests.get(url1).content)
    credits = json.loads(requests.get(url2).content)
    reviews = json.loads(requests.get(url3).content)
    print(reviews)
    
    name = "N/A"
    if type=='movie' and 'title' in media and media['title']!= None:
        name = media['title']
    elif type=='tv' and 'name' in media and media['name']!= None:
        name = media['name']
        
    synopsis = "N/A"
    if 'overview' in media and media['overview']!= None:
        synopsis = media['overview']
        
    year ="N/A"
    if type=='movie' and 'release_date' in media and media['release_date']!= None:
        year = str(media['release_date'].split('-')[0])
    elif type=='tv' and 'first_air_date' in media and media['first_air_date'] != None:
        year = str(media['first_air_date'].split('-')[0])
    
    spoken_languages = "N/A"
    if 'spoken_languages' in media and media['spoken_languages'] != None:
        spoken_languages = ', '.join([l['english_name'] for l in media['spoken_languages']])
    votes = str(media['vote_count']) + " Votes" if 'vote_count' in media and media['vote_count'] != None else "N/A"
    rating = str(round(media['vote_average']/2, 1)) + "/5" if 'vote_average' in media and media['vote_average'] != None else "N/A"
    
    genres = "N/A"
    if 'genres' in media:
        genres = ', '.join([l['name'] for l in media['genres']])
    
    backdrop = "https://image.tmdb.org/t/p/w780" + media['backdrop_path'] if 'backdrop_path' in media and media['backdrop_path'] != None else "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg"
    
    genres = "N/A"
    if 'genres' in media:
        genres = ', '.join([g['name'] for g in media['genres']])
        
    cast = []
    for person in credits['cast'][:8]:
        temp = {
            'name' : person['name'] if 'name' in person and person['name'] != None else "N/A",
            'character' : person['character'] if 'character' in person and person['character'] != None and person['character']!="" else "N/A",
            'picture' : "https://image.tmdb.org/t/p/w185" + person['profile_path'] if 'profile_path' in person and person['profile_path']!=None else "https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/person-placeholder.png"
            }
        cast.append(temp)
    r = []
    for review in reviews['results'][:5]:
        temp = {
            'author' : review['author_details']['username'] if 'author_details' in review and 'username' in review['author_details'] and review['author_details']['username']!=None  else "N/A",
            'review_rating' : str(round(review['author_details']['rating']/2 ,1)) + '/5' if 'author_details' in review and 'rating' in review['author_details'] and review['author_details']['rating'] != None else "N/A",
            'content' : review['content'] if 'content' in review and review['content'] != None else "N/A",
            'review_date' : review['created_at'].split('T')[0].split('-') if 'created_at' in review and review['created_at'] != None and review['created_at']!="" else "N/A"
        }
        if temp['review_date'] != "N/A":
            t = temp['review_date'][1:] + temp['review_date'][:1]
            temp['review_date'] = '/'.join(t)
        r.append(temp)
    info = year + " | " + genres
    data = {
        'id': str(id),
        'name' : str(name),
        'type' : str(type),
        'synopsis' : str(synopsis),
        'info' : str(info),
        'spoken_languages' : "Spoken languages: " + str(spoken_languages),
        'votes' : str(votes),
        'rating': str(rating),
        'backdrop' : str(backdrop),
        'cast': cast,
        'reviews' : r
    }
    return jsonify(data)



if __name__ == '__main__':
    app.debug=True
    app.run()