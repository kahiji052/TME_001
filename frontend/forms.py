from django import forms
from django.contrib.auth.forms import User
from . import models

class login_form(forms.Form):
    username = forms.CharField(
        label='',
        widget = forms.TextInput(attrs = {'placeholder': 'Nombre de usuario', 'class': 'input_data'})
    )

    password = forms.CharField(
        label = '',
        widget = forms.PasswordInput(attrs = {'placeholder': 'Contraseña', 'class': 'input_data'})
    )
    

class create_form(forms.Form):
    create_username = forms.CharField(
        label='',
        widget = forms.TextInput(attrs = {'placeholder': 'Nombre de usuario', 'class': 'input_data'})
    )

    create_email = forms.EmailField(
        label = '',
        widget = forms.EmailInput(attrs = {'placeholder': 'Correo electrónico', 'class': 'input_data'})
    )

    create_password = forms.CharField(
        label = '',
        widget = forms.PasswordInput(attrs = {'placeholder': 'Contraseña', 'class': 'input_data'})
    )

    repassword = forms.CharField(
        label = '',
        widget = forms.PasswordInput(attrs = {'placeholder': 'Confirmar contraseña', 'class': 'input_data'})
    )

    def clean_create_username(self):
        create_username = self.cleaned_data['create_username']
        check_username = User.objects.filter(username=create_username)

        if check_username:
            raise forms.ValidationError('Usuario inválido.') 
        return create_username

    def clean_create_email(self):
        create_email = self.cleaned_data['create_email']
        check_email = User.objects.filter(email=create_email)

        if check_email:
            raise forms.ValidationError('Este correo ya está registrado.') 
        return create_email

    def clean_repassword(self):
        create_password = self.cleaned_data["create_password"]
        repassword = self.cleaned_data["repassword"]

        if create_password != repassword:
            raise forms.ValidationError('Las contraseñas no coinciden.') 
        return repassword 

class forgot_form(forms.Form):
    send_email = forms.EmailField(
        label = '',
        widget = forms.EmailInput(attrs = {'placeholder': 'Correo electrónico', 'class': 'input_data'}),
        error_messages={'invalid': 'Email inválido.'}
    )
