from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect 
from django.contrib import messages
from requests import Request, post
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from .util import *
from . import etl_script, top_ten_script, full_user_history, top_ten_artists, top_ten_albums

# Create your views here.
def IsAuthenticated(request):
    # print('USER = ', request.user.username)
    is_authenticated = is_spotify_authenticated(session_id=request.session.session_key)
    test = {'status': is_authenticated}
    if (test['status'] == False):
        return redirect('spotify:get_auth')
    return redirect('frontend:home')

class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-library-read user-top-read user-read-recently-played'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return redirect(url)

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    etl_script.test(request.user.username, access_token)

    # top_ten = top_ten_script.get_user_top_ten(request.user.username)
    
    # user_history = full_user_history.get_full_user_history(request.user.username)
    
    update_or_create_user_tokens(session_id=request.session.session_key, access_token=access_token, token_type=token_type, expires_in=expires_in, refresh_token=refresh_token)
    
    return redirect('frontend:home') 

def current_user(request):
    session = request.session.session_key
    endpoint = ""
    response = execute_spotify_api_request(session, endpoint)
    messages.add_message(request, messages.INFO, response['id'], extra_tags='current_user')
    return redirect('frontend:settings')

def get_top_ten(request):
    top_ten = top_ten_script.get_user_top_ten(request.user.username)
    request.session['top_ten'] = top_ten
    return redirect('frontend:top_ten')

def get_user_history(request):
    user_history = full_user_history.get_full_user_history(request.user.username)
    request.session['user_history'] = user_history
    return redirect('frontend:user_history')

def get_top_artists(request):
    top_artists = top_ten_artists.get_user_top_artists(request.user.username)
    request.session['top_artists'] = top_artists
    return redirect('frontend:top_artist')

def get_top_albums(request):
    top_albums = top_ten_albums.get_user_top_albums(request.user.username)
    request.session['top_albums'] = top_albums
    return redirect('frontend:top_albums')