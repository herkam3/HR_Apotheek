from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import NameForm, DistanceForm
from .models import Time, Distance

def index(request):
    return render(request, 'base/index.html')