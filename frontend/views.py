from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import json
import datetime as dt
from datetime import timedelta
from . import forms, models
from . import welcome_mail, reset_mail, contact_mail

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def login_page(request):
    context = {
        'login_form': forms.login_form(),
        'create_form': forms.create_form(),
        'forgot_form': forms.forgot_form()
    }
    
    if request.method == 'POST':
        if 'save_user' in request.POST:
            context['login_form'] = forms.login_form(request.POST)
            if context['login_form'].is_valid():
                username = request.POST['username']
                password =  request.POST['password']

                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('frontend:home')
                else:
                    messages.error(request, 'Usuario o contraseña inválida.')

        if 'save_account' in request.POST:
            context['create_form'] = forms.create_form(request.POST)
            if context['create_form'].is_valid():
                username = request.POST['create_username']
                email = request.POST['create_email']
                password = request.POST['create_password']
                account = User.objects.create_user(username, email, password)
                welcome_mail.send_mail(to_emails = [email])

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    models.date_login.objects.create (
                        user = account
                    )

                    login(request, user)
                    return redirect('frontend:home')

        if 'save_email' in request.POST:
            context['forgot_form'] = forms.forgot_form(request.POST)
            if context['forgot_form'].is_valid():
                email = request.POST['send_email']
                reset_mail.send_mail(to_emails = [email])

    return render(request, 'login/base.html', context)

def reset_password(request):
    return render(request, 'reset_password.html')

@login_required(login_url='frontend:login')
def home(request):
    # Hora actual
    current_time = timezone.now()

    date_login = models.date_login.objects.get(user__username=request.user.username)
    first_login  = date_login.first_login
    
    if first_login != None:
        # Suma de días (al día de actualización)
        date_update = first_login + timedelta(hours=24)
        check_update = (current_time.replace(tzinfo=None) < date_update.replace(tzinfo=None))
    else:
        date_update = None
        check_update = None

    context = {
        'current_time': current_time,
        'first_login': first_login,
        'date_update': date_update,
        'check_update': check_update,
    }
    return render(request, 'home.html', context)

@login_required(login_url='frontend:login')
def update_data(request):
    # Día de actualización
    date_login = models.date_login.objects.get(user__username=request.user.username)
    date_login.first_login = timezone.now()
    date_login.save()

    # Auth Spotify
    return redirect('spotify:is_authenticated') 

@login_required(login_url='frontend:login')
def show_top_ten(request):
    if 'top_ten' in request.session:
        top_ten = json.loads(request.session['top_ten'])
    else:
        top_ten = None
    
    context = {
        'top_ten': top_ten
    }
    return render(request, 'top_ten.html', context)

@login_required(login_url='frontend:login')
def show_user_history(request):
    if 'user_history' in request.session:
        user_history = json.loads(request.session['user_history'])
    else:
        user_history = None

    context = {
        'user_history': user_history
    }
    return render(request, 'history.html', context)

@login_required(login_url='frontend:login')
def show_top_artist(request):
    if 'top_artists' in request.session:
        top_artists = json.loads(request.session['top_artists'])
    else:
        top_artists = None

    context = {
        'top_artists': top_artists
    }
    return render(request, 'top_artist.html', context)

@login_required(login_url='frontend:login')
def show_top_albums(request):
    if 'top_albums' in request.session:
        top_albums = json.loads(request.session['top_albums'])
    else:
        top_albums = None

    context = {
        'top_albums': top_albums
    }
    return render(request, 'top_albums.html', context)

@login_required(login_url='frontend:login')
def logout_user(request):
    logout(request)
    return redirect('frontend:login')

@login_required(login_url='frontend:login')
def contact_page(request):
    if request.method == 'POST':
        if 'send_mail' in request.POST:
            email = request.POST['user_email']
            contact_mail.send_mail(to_emails=[email])

    return render(request, 'contact.html')

@login_required(login_url='frontend:login')
def settings_page(request):
    if request.method == 'POST':
        if 'save_username' in request.POST:
            new_username = request.POST['username']
            query = User.objects.filter(username=new_username)
            if query:
                messages.add_message(request, messages.ERROR, 'Usuario inválido.', extra_tags='error_username')
            else:
                user = User.objects.get(username=request.user.username)
                user.username = new_username
                user.save()
                return HttpResponseRedirect(reverse('frontend:settings'))
        if 'save_email' in request.POST:
            email = request.POST['email']
            query = User.objects.filter(email=email)
            if query:
                messages.add_message(request, messages.ERROR, 'Correo inválido.', extra_tags='error_email')
            else:
                user = User.objects.get(username=request.user.username)
                user.email = email
                user.save()
                return HttpResponseRedirect(reverse('frontend:settings'))
        if 'save_password' in request.POST:
            new_password = request.POST['new_password']
            password = request.POST['password']
            if new_password == password:
                user = User.objects.get(username=request.user.username)
                user.set_password(new_password)
                user.save()
            else:
                messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden.', extra_tags='error_password')
    return render(request, 'settings.html')