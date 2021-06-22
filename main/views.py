from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Film, Basket, Result
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CreateNewBasket
# Create your views here.

def search_results(request, id):
    if request.method=="POST":
        
        if request.POST.get("Add"):
            results = Result.objects.filter(Num=id)
            search_result = results[len(results) - 1 ]
            
            basket = Basket.objects.get(id=id)
            basket.film_set.create(name=search_result.result)
            Result.objects.all().delete()
            
            return redirect("main:homepage")
        
        search = request.POST.get('search')
        r = Result(result=search, Num=id)
        r.save()
        
        return render(request, "main/search_results.html", {"search":search, "id":id})

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
                if request.POST.get("Save"):
                    for i in films:
                        if request.POST.get("c" + str(i.id)) == "clicked":
                            i.done = True
                        else:
                            i.done = False
                        i.save()
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
        
