from django.urls import path
from appmovie.views import movies_trending, movie_details
urlpatterns=[
    path('',movies_trending,name='home'),
    path('movie/<int:id>/',movie_details,name='movie_details')
]