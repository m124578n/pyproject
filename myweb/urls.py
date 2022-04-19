from django.urls import path
from regex import P
from . import views

urlpatterns = [
    path('',views.home),
    path('login/',views.login),
    path('signup/',views.signup),

]
