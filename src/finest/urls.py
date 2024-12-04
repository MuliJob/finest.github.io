from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/overview/', views.dashboard, name='dashboard'),
    path('dashboard/my-posts/', views.my_post, name='my_post'),
    path('dashboard/posted/', views.posted, name='posted'),
    path('dashboard/submit-website/', views.submit_website, name='submit_website'),
    path('dashboard/details/', views.my_post_detail, name='my_post_detail'),
    path('contactus/', views.contactus, name='contactus')
]