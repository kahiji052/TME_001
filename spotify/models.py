from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SpotifyToken(models.Model):
    session = models.CharField(max_length=50, unique=True)
    spotify_username = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=300)
    access_token = models.CharField(max_length=300)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)