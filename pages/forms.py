from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from datetime import timedelta, datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class SearchForm(forms.Form):
    search = forms.CharField()
    retweet_threshold = forms.IntegerField(required = False)
    favorite_threshold = forms.IntegerField(required = False)
    date_threshold = forms.CharField(required = False)

    def clean_search(self):
        data = self.cleaned_data.get('search')
        if data == '':
            raise forms.ValidationError('Enter a search term!')
        return data

    def clean_retweet_threshold(self):
        data = self.cleaned_data.get('retweet_threshold')
        if data == None:
            return data
        if data < 0:
            raise forms.ValidationError('Enter positive number for favorite threshold!')
        return data

    def clean_favorite_threshold(self):
        data = self.cleaned_data.get('favorite_threshold')
        if data == None:
            return data
        if data < 0:
            raise forms.ValidationError('Enter positive number for favorite threshold!')
        return data

    def clean_date_threshold(self):
        data = self.cleaned_data.get('date_threshold')
        if data == '':
            return data
        data_datetime = datetime.strptime(data, '%m/%d/%Y %I:%M %p')
        if data_datetime < datetime.now()-timedelta(days=7):
            raise forms.ValidationError('Enter a valid date! (no more than 7 days in the past)')
        return data

