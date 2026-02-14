from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save/',views.save_beneficiary , name='save'),
    path('profile/',views.profile , name='profile'),

]
