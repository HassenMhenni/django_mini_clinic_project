from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'verified_by_admin')
    list_filter = ('verified_by_admin',)
    search_fields = ('name',)
