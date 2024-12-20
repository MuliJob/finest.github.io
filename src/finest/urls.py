""" Finest app urls """
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from finest import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/overview/', views.dashboard, name='dashboard'),
    path('dashboard/explore/', views.explore, name='explore'),
    path('dashboard/my-posts/', views.my_post, name='my_post'),
    path("dashboard/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path('dashboard/favorites/', views.favorite, name='favorite'),
    path('dashboard/submit-website/', views.submit_website, name='submit_website'),
    path('dashboard/details/<int:pk>', views.my_post_detail, name='my_post_detail'),
    path('dashboard/all/details/<int:pk>', views.all_post_details, name='all_post_details'),
    path('dashboard/<int:pk>/add-review/', views.add_review, name='add_review'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('api/profiles/', views.ProfileListAPIView.as_view(), name='api-profiles'),
    path('api/projects/', views.SubmittedWebsiteListAPIView.as_view(), name='api-projects'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)