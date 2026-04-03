from django.shortcuts import render, redirect, HttpResponse
import requests
from appmovie.services.tmdbservices import fetchfromDB
from datetime import datetime
import json
import random
from django.contrib.auth.decorators import login_required
from .models import EmailOTP
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import timedelta
from django.utils import timezone
import base64
from django.contrib.auth.models import User

from appmovie.forms import RegisterForm
# Create your views here.

@login_required
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
        release_date = random_movie.get("release_date")

        if release_date:
            random_movie["release_date"] = datetime.strptime(release_date, "%Y-%m-%d")


        return render(request,'home.html',{"randommovie":random_movie,"data":jdata["results"],"toprated":trdata["results"],"now_playing":npdata["results"],"upcoming":udata["results"]})
    except Exception as error:
        return HttpResponse(str(error))

@login_required   
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
            if v["site"]=="Youtube" and  v.get("official") and v["type"]=="Trailer":
                trailers.append(v["key"])

        return render(request,'moviedetails.html',{"trailers": trailers,"info":info_data,"cast":credit_data["cast"],"similar":similar_data["results"]})
    except Exception as error:
        return HttpResponse(str(error))
@login_required     
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

@login_required    
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
                trailers.append(v["id"])

        return render(request,'seriesdetails.html',{"trailers": trailers,"info":info_data,"credits":credits_data["cast"],"similar":similar_data["results"]})
    except Exception as error:
        return HttpResponse(str(error))

@login_required   
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
@login_required   
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

def frontpage(request):
    return render(request,'frontpage.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Delete old OTP
            EmailOTP.objects.filter(user=user).delete()

            # Generate OTP
            raw_otp = str(random.randint(100000, 999999))
            hashed_otp = make_password(raw_otp)

            EmailOTP.objects.create(
                user=user,
                otphash=hashed_otp
            )
            subject = "Verify Your Account"

            html_content = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #d63384;">Hello dear RCFLix User: {user}</h2>

                <p style="font-weight:bold;">Here’s your OTP:</p>

                <h1 style="color: #ff1493; letter-spacing: 3px;">
                    {raw_otp}
                </h1>

                <p style="font-weight:bold;">
                    Please note that this OTP is valid for 5 minutes and can only be used 5 times. If you did not request this, please ignore this email.
                </p>

                <br>
                <p>
                    Thanks,<br>
                    <strong>RCFlix Admin Team</strong>
                </p>
            </div>
            """

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                         subject,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
            try:
                email.attach_alternative(html_content, "text/html")
                email.send()
            except Exception as e:
                print("Email error:", str(e))

            # Send email
            # send_mail(
            #     "Verify your account",
            #     f"Your OTP is {raw_otp}",
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            # )
            #

            return redirect("verify-otp")
    # If form NOT valid, it must return here
        return render(request, "registration.html", {"form": form})
    else:
        form = RegisterForm()

    return render(request, "registration.html", {"form": form})

def verify_otp(request):
    otp_valid = False
    if request.method == "POST":
        username = request.POST.get("username").strip()
        entered_otp = request.POST.get("otp").strip()

        user = User.objects.filter(username=username).first()
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if not otp_obj:
            return render(request, "verify_otp.html", {"error": "No OTP found"})

        # Expiry check (5 mins)
        if otp_obj.created_at < timezone.now() - timedelta(minutes=5):
            return render(request, "verify_otp.html", {"error": "OTP expired"})

        # Attempt limit
        if otp_obj.attempts >= 5:
            return render(request, "verify_otp.html", {"error": "Too many attempts"})

        if check_password(entered_otp, otp_obj.otphash):
            otp_valid = True
            user.is_active = True
            user.save()
            otp_obj.delete()
            return redirect("login")
        else:
            otp_obj.attempts += 1
            otp_obj.save()
            return render(request, "verify_otp.html", {"error": "Invalid OTP"})

    return render(request, "verify_otp.html",{"otp_valid":otp_valid})

def root_redirect(request):
    return redirect('/accounts/login/')
