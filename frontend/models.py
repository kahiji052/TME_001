from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class date_login(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.DateTimeField(null=True)
    def __str__(self):
        return self.user.username

class Plays(models.Model):
    username = models.CharField(max_length=100)
    song_title = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    played_at = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return self.username