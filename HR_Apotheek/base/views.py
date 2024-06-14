from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Medicine, Collection
from .forms import MedicineForm, CollectionForm, ProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'base/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create a profile for the new user
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'base/profile.html', {'form': form})

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'base/medicine_list.html', {'medicines': medicines})

@login_required
def collection_list(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'base/collection_list.html', {'collections': collections})
