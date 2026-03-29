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
        trailers = []
        video_data=json.loads(movie_videos)
        for v in video_data["results"]:
            if v["site"]=="Youtube" and  v.get("official"):
                trailers.append(v["key"])

        return render(request,'moviedetails.html',{"trailers": trailers})
    except Exception as error:
        return HttpResponse(str(error))