from django.urls import path
from .views import *

app_name = 'spotify'

urlpatterns = [
    # Step 1. Check if user is authenticated with spotify
    path('is_authenticated', IsAuthenticated, name='is_authenticated'),
    path('get_auth_url', AuthURL.as_view(), name='get_auth'),
    path('redirect', spotify_callback, name='callback'),
    path('current_user', current_user, name='current_user'),
    path('get_top_ten', get_top_ten, name='get_top_ten'),
    path('get_user_history', get_user_history, name='get_user_history'),
    path('get_top_artists', get_top_artists, name='get_top_artists'),
    path('get_top_albums', get_top_albums, name='get_top_albums')
]