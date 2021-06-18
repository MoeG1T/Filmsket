from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Film, Basket
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CreateNewBasket
# Create your views here.

def create(request):
    if request.method == "POST":
        form = CreateNewBasket(request.POST)

        if form.is_valid():
            new_basket = form.cleaned_data["name"]
            c = Basket(BasketGenre=new_basket)
            c.save()
            messages.success(request, f"New Film Basket Made: {new_basket}")
            return redirect("main:homepage")
    
    form = CreateNewBasket()
    return render(request, "main/create.html", {"form":form})

    
def index(request, id):
    baskets = Basket.objects.get(id=id)
    films = baskets.film_set.all()

    if request.method=="POST":
        
        if request.POST.get("NewFilm"):
            pass
        
        elif request.POST.get("Save"):
            for i in films:
                if request.POST.get("c" + str(i.id)) == "clicked":
                    i.done = True
                else:
                    i.done = False
                i.save()
            return render(request, "main/basket.html", {"films":films})
        
    return render(request, "main/basket.html", {"films":films})

def homepage(request):
    return render(request=request, 
                  template_name="main/baskets.html", 
                  context={"Baskets":Basket.objects.all()})

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
        
