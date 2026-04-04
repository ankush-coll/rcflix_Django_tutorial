from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EmailOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otphash=models.CharField(max_length=128)
    created_at=models.DateTimeField(auto_now_add=True)
    attempts=models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100, blank=True)

class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.movie_name}"