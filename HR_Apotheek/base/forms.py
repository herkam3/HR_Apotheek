from django import forms
from django.contrib.auth.models import User
from .models import Medicine, Collection, Profile

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer', 'cures', 'side_effects']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['medicine', 'user', 'date', 'collected', 'collected_approved', 'collected_approved_by']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio_text', 'city', 'date_of_birth']

class YesNoForm(forms.Form):
    RESPONSE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    response = forms.ChoiceField(choices=RESPONSE_CHOICES, widget=forms.RadioSelect)
