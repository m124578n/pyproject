from django.urls import path
from regex import P
from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('login/',views.sign_in, name='login'),
    path('signup/',views.register_view, name='register'),
    #path('test/',views.xxx),
    path('prs1/',views.prs1, name='prs1'),
    path('prs2/',views.prs2, name='prs2'),
    path('prs3/',views.prs3, name='prs3'),
    #path('register/', views.register_view, name='register'),
    path('update/<str:pk>', views.update, name='Update'),
    #path('delete/<str:pk>', views.delete, name='Delete'),
    #path('login01/', views.sign_in, name='Login'),
    path('logout', views.log_out, name='Logout'),
    path('indexx', views.indexx, name='index'),


]
