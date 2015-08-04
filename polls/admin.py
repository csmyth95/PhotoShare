from django.contrib import admin
from polls.models import UserProfile, Category, Image

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Image)


