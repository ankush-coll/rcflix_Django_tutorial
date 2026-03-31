from django.shortcuts import render, HttpResponse
import requests
from appmovie.services.tmdbservices import fetchfromDB
import json
import random
# Create your views here.
def movies_trending(request):
    try:
        popular_data=fetchfromDB("https://api.themoviedb.org/3/movie/popular")
        top_rated_data=fetchfromDB("https://api.themoviedb.org/3/movie/top_rated")
        now_playing_data=fetchfromDB("https://api.themoviedb.org/3/movie/now_playing")
        upcoming_data=fetchfromDB("https://api.themoviedb.org/3/movie/upcoming")

        jdata=json.loads(popular_data)
        trdata=json.loads(top_rated_data)
        npdata=json.loads(now_playing_data)
        udata=json.loads(upcoming_data)

        random_movie=random.choice(jdata["results"])


        return render(request,'home.html',{"randommovie":random_movie,"data":jdata["results"],"toprated":trdata["results"],"now_playing":npdata["results"],"upcoming":udata["results"]})
    except Exception as error:
        return HttpResponse(str(error))
    
def movie_details(request, id):
    try:
        movie_videos=fetchfromDB(f"https://api.themoviedb.org/3/movie/{id}/videos")
        movie_info=fetchfromDB(f"https://api.themoviedb.org/3/movie/{id}")
        movie_credits=fetchfromDB(f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US")
        similar_movies=fetchfromDB(f"https://api.themoviedb.org/3/movie/{id}/similar?language=en-US&page=1")

        trailers = []

        video_data=json.loads(movie_videos)
        info_data=json.loads(movie_info)
        credit_data=json.loads(movie_credits)
        similar_data=json.loads(similar_movies)

        for v in video_data["results"]:
            if v["site"]=="Youtube" and  v.get("official"):
                trailers.append(v["key"])

        return render(request,'moviedetails.html',{"trailers": trailers,"info":info_data,"cast":credit_data["cast"],"similar":similar_data["results"]})
    except Exception as error:
        return HttpResponse(str(error))
    
def series(request):
    try:
        popular_data=fetchfromDB("https://api.themoviedb.org/3/tv/popular?language=en-US&page=1")
        top_rated_data=fetchfromDB("https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1")
        now_playing_data=fetchfromDB("https://api.themoviedb.org/3/tv/on_the_air?language=en-US&page=1")
        upcoming_data=fetchfromDB("https://api.themoviedb.org/3/tv/airing_today?language=en-US&page=1")

        jdata=json.loads(popular_data)
        trdata=json.loads(top_rated_data)
        npdata=json.loads(now_playing_data)
        udata=json.loads(upcoming_data)

        random_tv=random.choice(jdata["results"])

        return render(request,'series.html',{"randomtv":random_tv,"data":jdata["results"],"toprated":trdata["results"],"now_playing":npdata["results"],"upcoming":udata["results"]})

    except Exception as error:
        return HttpResponse(str(error))
    
def series_details(request, id):
    try:
        tv_videos=fetchfromDB(f"https://api.themoviedb.org/3/tv/{id}/videos?language=en-US")
        tv_info=fetchfromDB(f"https://api.themoviedb.org/3/tv/{id}?language=en-US")
        tv_credits=fetchfromDB(f"https://api.themoviedb.org/3/tv/{id}/credits?language=en-US")
        tv_similar=fetchfromDB(f"https://api.themoviedb.org/3/tv/{id}/similar?language=en-US&page=1")
        
        trailers = []

        video_data=json.loads(tv_videos)
        info_data=json.loads(tv_info)
        credits_data=json.loads(tv_credits)
        similar_data=json.loads(tv_similar)

        for v in video_data["results"]:
            if v["site"]=="Youtube" and  v.get("official"):
                trailers.append(v["key"])

        return render(request,'seriesdetails.html',{"trailers": trailers,"info":info_data,"credits":credits_data["cast"],"similar":similar_data["results"]})
    except Exception as error:
        return HttpResponse(str(error))
    
def person_info(request, id):
    try:
        person=fetchfromDB(f"https://api.themoviedb.org/3/person/{id}?language=en-US")
        person_movie_credits=fetchfromDB(f"https://api.themoviedb.org/3/person/{id}/movie_credits?language=en-US")
        person_images=fetchfromDB(f"https://api.themoviedb.org/3/person/{id}/images")
        person_tv=fetchfromDB(f"https://api.themoviedb.org/3/person/{id}/tv_credits")

        person_data=json.loads(person)
        movie_data=json.loads(person_movie_credits)
        image_data=json.loads(person_images)
        person_cast=json.loads(person_tv)

        return render(request,'person.html',{"person":person_data,"movies":movie_data["cast"],"images":image_data["profiles"][:5],"tv":person_cast["cast"]})
    except Exception as error:
            return HttpResponse(str(error))

def search_multi(request):
    try:
        query = request.GET.get('q')
        multidata=fetchfromDB(f"https://api.themoviedb.org/3/search/multi?query={query}&include_adult=true&language=en-US&page=1")
        multi_jdata=json.loads(multidata)

        if not query:
            return render(request, 'search.html', {'data': []})
        else:
            return render(request,'search.html',{"multi":multi_jdata["results"]})

    except Exception as error:
            return HttpResponse(str(error))
