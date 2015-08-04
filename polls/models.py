from django.db import models
from django.contrib.auth.models import User
from polls.thumbs import ImageWithThumbsField


class Category(models.Model):
    user = models.ForeignKey(User, related_name='Albums')
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    user = models.ForeignKey(User, related_name='Images')
    title = models.CharField(max_length=128)
    image = ImageWithThumbsField(upload_to='images/', sizes=((125, 125), (200, 200), (500, 500)))
    category = models.ForeignKey(Category)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # A required line - links a UserProfile to User.
    user = models.OneToOneField(User)
    friends = models.ManyToManyField('self')
    # The additional attributes we wish to include.
    picture = ImageWithThumbsField(upload_to='profile_images', blank=True, sizes=((125, 125), (200, 200)))

    def __unicode__(self):
        return self.user.username




