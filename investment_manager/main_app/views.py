from django.http import HttpResponse
from . import app_dash
# Create your views here.
from .app_engine import Portfolio
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
from .montecarlo_plotly import Graphs
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

app = app_dash.app

if app ==None:
    print("app is none existant")
else:
    print("app intact")

@login_required
def settings(request):
    text = "hello how are you my friend the web is working"

    context = {
        'text':text,
    }
    return render(request, "main_app/settings.html",context)

@login_required
def portfolio_building(request):

    context ={
        "app":app
    }
    return render(request, "main_app/creating_portfolio.html", context)

def portfolio_testing(request):


    data = "Here will come a plotly graph and other scripts"
    context = {
        "data": data
    }
    return render(request,"main_app/testingportfolio.html", context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'main_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('building')  # Redirect to your dashboard page
    else:
        form = AuthenticationForm()
    return render(request, 'main_app/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the home page or any other page after logout.

