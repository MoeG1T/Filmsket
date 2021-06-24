from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Film, Basket, Result
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CreateNewBasket
import imdb
import urllib.request
import re
# Create your views here.


def film_info(request, id):
    film = Film.objects.get(id=id)
    return render(request, "main/film.html", {"Film":film})

def search_results(request, id):
    moviesDB = imdb.IMDb()
    if request.method=="POST":
        
        if request.POST.get("Add"):
            results = Result.objects.filter(Num=id)
            search_result = results[len(results) - 1 ]
            
            basket = Basket.objects.get(id=id)
            basket.film_set.create(summary=search_result.result, poster=search_result.poster, url=search_result.url)
            Result.objects.all().delete()
            
            return redirect("main:index", id=id)
        
        search = request.POST.get('search')
        
        movies = moviesDB.search_movie(search)[0]
        movie_id = movies.getID()
        movie = moviesDB.get_movie(movie_id)

        title = (movie["title"] + " " + str(movie["year"]) + " Trailer").replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + title)
        results = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/embed/" + results[0]

        r = Result(result=movie.summary(), url=url, Num=id, poster=movie['full-size cover url'])
        r.save()
        
        description = r.result
        li = list(description.split("\n"))
        
        return render(request, "main/search_results.html", {"result":r, "id":id, "summary":li})

def create(request):
    if request.method == "POST":
        form = CreateNewBasket(request.POST)

        if form.is_valid():
            new_basket = form.cleaned_data["name"]
            c = Basket(BasketGenre=new_basket)
            c.save()
            request.user.basket.add(c)
            messages.success(request, f"New Film Basket Made: {new_basket}")
            return redirect("main:homepage")
    
    form = CreateNewBasket()
    return render(request, "main/create.html", {"form":form})

    
def index(request, id): 
    baskets = Basket.objects.get(id=id)
    films = baskets.film_set.all()
    
    if not request.user.is_anonymous:
        if baskets in request.user.basket.all():
            
            if request.method=="POST": 
                for i in films:  
                    if request.POST.get("c" + str(i.id)) == "clicked":
                        i.delete()

                baskets = Basket.objects.get(id=id)
                films = baskets.film_set.all()
                    
                return render(request, "main/basket.html", {"films":films , "id":id}) 

            return render(request, "main/basket.html", {"films":films, "id":id})

        return render(request,"main/baskets.html",{})
    else:
        return redirect("main:homepage")
    

def homepage(request):
    return render(request, 
                  "main/baskets.html", 
                  {})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])             

    form = NewUserForm
    return render(request, 
           "main/register.html", 
           context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    
    form = AuthenticationForm()
    return render(request, "main/login.html", {"form":form})
        
