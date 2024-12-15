from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'time', 'doctor_name')
    list_filter = ('date', 'doctor_name')
    search_fields = ('patient__name', 'doctor_name')
    # internal_admin_notes can be edited here by admin
    fields = ('patient', 'date', 'time', 'doctor_name', 'internal_admin_notes')