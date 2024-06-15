from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Medicine, Collection
from .forms import MedicineForm, CollectionForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

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
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    user_collections = Collection.objects.filter(user=request.user, medicine=medicine)
    total_collections = Collection.objects.filter(medicine=medicine)
    return render(request, 'base/medicine_detail.html', {
        'medicine': medicine,
        'user_collections': user_collections,
        'total_collections': total_collections,
    })

@login_required
def collection_list(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'base/collection_list.html', {'collections': collections})

@login_required
def collection_mark_collected(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    collection.collected = True
    collection.save()
    return redirect('collection_list')

@login_required
def admin_approve_collection(request, collection_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    collection = get_object_or_404(Collection, id=collection_id)
    collection.collected_approved = True
    collection.collected_approved_by = request.user
    collection.save()
    return redirect('admin_view_collections')

@login_required
def admin_delete_prescription(request, collection_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    collection = get_object_or_404(Collection, id=collection_id)
    collection.delete()
    return redirect('admin_view_collections')

@login_required
def admin_view_collections(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    collections = Collection.objects.all()
    return render(request, 'admin/collection_list.html', {'collections': collections})

@login_required
def admin_create_prescription(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view_collections')
    else:
        form = CollectionForm()
    return render(request, 'admin/create_prescription.html', {'form': form})

@login_required
def admin_create_prescription_from_medicine(request, medicine_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_detail', medicine_id=medicine_id)
    else:
        form = CollectionForm(initial={'medicine': medicine})
    return render(request, 'admin/create_prescription.html', {'form': form, 'medicine': medicine})

@login_required
def admin_manage_medicines(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    medicines = Medicine.objects.all()
    return render(request, 'admin/medicine_list.html', {'medicines': medicines})

@login_required
def admin_add_medicine(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_medicines')
    else:
        form = MedicineForm()
    return render(request, 'admin/add_medicine.html', {'form': form})

@login_required
def admin_edit_medicine(request, medicine_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_medicines')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'admin/edit_medicine.html', {'form': form})

@login_required
def admin_view_user_profile(request, user_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user=user)
    collections = Collection.objects.filter(user=user)
    return render(request, 'admin/user_profile.html', {'profile': profile, 'collections': collections})
