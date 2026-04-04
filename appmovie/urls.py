from django.urls import path
from appmovie.views import frontpage,user_likes,register,verify_otp, movies_trending,search_multi, person_info, movie_details, series,series_details
urlpatterns=[
    path('',frontpage,name='frontpage'),
    path('home/',movies_trending,name='home'),
    path('movie/<int:id>/',movie_details,name='movie_details'),
    path('series/',series,name='series'),
    path('tv/<int:id>/',series_details,name='series_details'),
    path('person/<int:id>/',person_info,name='person_info'),
    path('search/',search_multi,name='search_multi'),
    path("register/", register, name="register"),
    path("verify-otp/", verify_otp, name="verify-otp"),
    path("list/", user_likes, name="list"),
]