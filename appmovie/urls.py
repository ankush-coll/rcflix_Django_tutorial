from django.urls import path
from appmovie.views import movies_trending
urlpatterns=[
    path('',movies_trending,name='home')
]