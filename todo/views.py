from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signupuser(requests):
    return render(requests, 'signup.html', {'signup':UserCreationForm()})