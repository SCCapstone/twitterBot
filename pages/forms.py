from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from datetime import timedelta, date

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required = False)
    retweet_threshold = forms.IntegerField(required = False)
    favorite_threshold = forms.IntegerField(required = False)
    date_threshold = forms.DateField (required = False)
    tweet_number = forms.IntegerField(required = False)

    def clean_search(self):
        data = self.cleaned_data.get('search')
        if data == '':
            raise forms.ValidationError('Enter a search term!')
        return data

    def clean_date_threshold(self):
        data = self.cleaned_data.get('date_threshold')
        if data == None:
            return data
        if data < date.today()-timedelta(days=7):
            raise forms.ValidationError('Enter a valid date! (no more than 7 days in the past)')
        if data > date.today():
            raise forms.ValidationError("Enter a valid date! (date can't be in the future)")
        return data

