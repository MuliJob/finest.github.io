""" Finest app urls """
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/overview/', views.dashboard, name='dashboard'),
    path('dashboard/my-posts/', views.my_post, name='my_post'),
    path("dashboard/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path('dashboard/favorites/', views.favorite, name='favorite'),
    path('dashboard/submit-website/', views.submit_website, name='submit_website'),
    path('dashboard/details/<int:pk>', views.my_post_detail, name='my_post_detail'),
    path('contact_us/', views.contact_us, name='contact_us')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)