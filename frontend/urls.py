from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('home', views.home, name='home'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('update_data', views.update_data, name='update_data'),
    path('contact', views.contact_page, name='contact'),
    path('settings', views.settings_page, name='settings'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('top_ten', views.show_top_ten, name='top_ten'),
    path('user_history', views.show_user_history, name='user_history'),
    path('top_artist', views.show_top_artist, name='top_artist'),
    path('top_albums', views.show_top_albums, name='top_albums')
]
