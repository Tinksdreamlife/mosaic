from django import forms
from .models import UserProfile
from .models import Comment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'country_born', 'countries_lived', 'current_country']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']