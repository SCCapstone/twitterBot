from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    def __str__(self):
        return self.email

class Profile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(default='https://i.ibb.co/jGJMs0d/profile.png', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'