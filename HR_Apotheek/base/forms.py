from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Medicine, Collection, Profile

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer', 'cures', 'side_effects']

class CollectionForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y')
    )
    collected_approved_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=True,
        label='Approved By'
    )

    class Meta:
        model = Collection
        fields = ['medicine', 'user', 'date', 'collected', 'collected_approved', 'collected_approved_by']

    # class Meta:
    #     model = Collection
    #     fields = ['medicine', 'user', 'date', 'collected', 'collected_approved', 'collected_approved_by']

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y')
    )
    class Meta:
        model = Profile
        fields = ['bio_text', 'city', 'date_of_birth']

class CustomUserCreationForm(UserCreationForm):  # extend build in UserCreationForm with city, bio and birthdate
    city = forms.CharField(max_length=100, required=True)
    bio_text = forms.CharField(widget=forms.Textarea, required=True)
    date_of_birth = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y'),
        required=True
    )
    # date_of_birth = forms.DateField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'city', 'bio_text', 'date_of_birth')

class YesNoForm(forms.Form):
    RESPONSE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    response = forms.ChoiceField(choices=RESPONSE_CHOICES, widget=forms.RadioSelect)
