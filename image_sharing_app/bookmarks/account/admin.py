from django.contrib import admin

# Register your models here.
from .models import Profile

@admin.register(Profile)
class PeofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
