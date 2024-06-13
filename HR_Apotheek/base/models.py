from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    cures = models.TextField()
    side_effects = models.TextField()

    def __str__(self):
        return self.name

class Collection(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    collected = models.BooleanField(default=False)
    collected_approved = models.BooleanField(default=False)
    collected_approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_collections', null=True, blank=True)

    def __str__(self):
        return f"{self.medicine.name} collected by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio_text = models.TextField()
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username