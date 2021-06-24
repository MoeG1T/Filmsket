from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("register/", views.register, name = "register"),
    path("logout/", views.logout_request, name = "logout"),
    path("login/", views.login_request, name = "login"),
    path("<int:id>/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:id>/search_results/", views.search_results, name='search_results'),
    path("<int:id>/film_info/", views.film_info, name='film'),
]