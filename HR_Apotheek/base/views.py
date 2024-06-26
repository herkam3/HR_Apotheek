from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Profile, Medicine, Collection
from .forms import MedicineForm, CollectionForm, ProfileForm, YesNoForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    return render(request, 'base/index.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            city = form.cleaned_data.get('city')
            bio_text = form.cleaned_data.get('bio_text')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            Profile.objects.create(user=user, city=city, bio_text=bio_text, date_of_birth=date_of_birth)
            login(request, user)
            return redirect('register_succes')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def register_success(request):
    return render(request, 'base/register_success.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')  # or 'login' depending on your URL names
    

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
    if request.method == 'POST':
        form = YesNoForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            if response == 'yes':
                collection.collected = True
                collection.save()
                return redirect('collection_list')
            else:
                messages.info(request, "Approvel canceled.")
            return redirect('admin_view_collections')
        
    # collection.collected = True
    # collection.save()
    # return redirect('collection_list')


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'base/edit_profile.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_approve_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    if request.method == 'POST':
        form = YesNoForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            if response == 'yes':
                collection.collected_approved = True
                collection.collected_approved_by = request.user
                collection.save()
            else:
                messages.info(request, "Approvel canceled.")
            return redirect('admin_view_collections')
        
    else:
        form = YesNoForm()
    return render(request, 'admin/prompt.html', {'form': form, 'action': 'approve'})
    
    # collection.collected_approved = True
    # collection.collected_approved_by = request.user
    # collection.save()
    # return redirect('admin_view_collections')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_delete_prescription(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    if request.method == 'POST':
        form = YesNoForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            if response == 'yes':
                collection.delete()
                messages.success(request, "Prescription deleted successfully.")
            else:
                messages.info(request, "Deletion canceled.")
            return redirect('admin_view_collections')
    else:
        form = YesNoForm()
    return render(request, 'admin/prompt.html', {'form': form, 'action': 'delete'})
    
    # collection = get_object_or_404(Collection, id=collection_id)
    # collection.delete()
    # return redirect('admin_view_collections')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_view_collections(request):
    collections = Collection.objects.all()
    return render(request, 'admin/collection_list.html', {'collections': collections})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_create_prescription(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            medicine = form.cleaned_data['medicine']
            user = form.cleaned_data['user']
            date = form.cleaned_data['date']
            
            # Ensure a user cannot receive multiple prescriptions for the same medicine on the same day
            if Collection.objects.filter(user=user, medicine=medicine, date=date).exists():
                return HttpResponse("A user cannot receive multiple prescriptions for the same medicine on the same day.", status=400)
            
            form.save()
            return redirect('admin_view_collections')
    else:
        form = CollectionForm()
    return render(request, 'admin/create_prescription.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_create_prescription_from_medicine(request, medicine_id):
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
@user_passes_test(lambda u: u.is_staff)
def admin_manage_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'admin/medicine_list.html', {'medicines': medicines})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = MedicineForm()
    return render(request, 'admin/add_medicine.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'admin/edit_medicine.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = YesNoForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            if response == 'yes':
                medicine.delete()
                messages.success(request, "Medicine deleted successfully.")
            else:
                messages.info(request, "Deletion canceled.")
            return redirect('admin_dashboard')
            
    else:
        form = YesNoForm()
    return render(request, 'admin/prompt.html', {'form': form, 'action': 'delete'})
            
    
    # medicine.delete()
    # return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Get or create the profile for the user, providing default values for non-nullable fields
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'bio_text': '',
            'city': '',
            'date_of_birth': '2000-01-01'  # or another default date
        }
    )
    collections = Collection.objects.filter(user=user)
    return render(request, 'admin/user_profile.html', {'profile': profile, 'collections': collections})

@login_required
def user_dashboard(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'base/user_dashboard.html', {'collections': collections})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    users = User.objects.all()
    collections = Collection.objects.all()
    medicines = Medicine.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'users': users, 'collections': collections, 'medicines': medicines})  

@login_required
@user_passes_test(lambda u: u.is_staff)
def prompt_delete(request):
    if request.method == 'POST':
        form = YesNoForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            if response == 'yes':
                messages.success(request, "You selected Yes!")
            else:
                messages.info(request, "You selected No.")
            return redirect('admin_dashboard')  # Adjust the redirect target as needed
    else:
        form = YesNoForm()  