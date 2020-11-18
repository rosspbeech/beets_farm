from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This line links a userprofile to a user model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # The additional attributes we want to include that User does not have
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # This returns the users username, rather than the object location as it would if not overriden
    def __str__(self):
        return self.user.username



class Persona(models.Model):
    name = models.CharField(max_length=80, unique=True)
    about = models.TextField()
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Persona, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Beet(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    about = models.TextField(null=True)
    sound_file = models.FileField(upload_to="the_beets", blank=False)
    plays = models.IntegerField(default=0)

    def __str__(self):
        return self.name


