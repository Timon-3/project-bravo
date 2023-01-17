from django.db import models
from datetime import timezone

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    description = models.CharField(max_length=2000)



"""
# can be deleted if we decide to use the Django's built-it authentication system
    class Users(models.Model):
    user_ID = models.CharField(verbose_name="User's ID", max_length=50, help_text="User's ID")
    psw = models.CharField(verbose_name="Password", max_length=100, help_text="Password")
    email = models.CharField(verbose_name="E-mail", max_length=100, help_text="E-mail")
    first_name = models.CharField(verbose_name="Password", max_length=100, help_text="Password")
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(max_length=20, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(verbose_name="Creation date", default=timezone.now, help_text="The user was created at that time") """
