from django.urls import path
from appmovie.views import movies_trending, person_info, movie_details, series,series_details
urlpatterns=[
    path('',movies_trending,name='home'),
    path('movie/<int:id>/',movie_details,name='movie_details'),
    path('series/',series,name='series'),
    path('tv/<int:id>/',series_details,name='series_details'),
    path('person/<int:id>/',person_info,name='person_info')
]