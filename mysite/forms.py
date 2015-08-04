from django import forms
from django.contrib.auth.models import User

from polls.models import Category, UserProfile, Image


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the album name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        # fields to include
        fields = ('name', 'views', 'likes')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the image.")
    image = forms.ImageField(
        label='Select an image!')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Image
        fields = ('title', 'image')


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ('picture',)


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

