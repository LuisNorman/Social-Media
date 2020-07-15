from django.shortcuts import render
from django.urls import reverse_lazy # When someone is logged in or logged out where they should go
from django.views.generic import CreateView
from . import forms # needed for logging in or sing up

# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login') #Once someone signs in - if successful, reverse them back to the login page. reverse_lazy so it sends them back after submit
    template_name = 'accounts/signup.html'
