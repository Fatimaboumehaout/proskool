from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'specialization', 'status', 'hire_date']
    list_filter = ['status', 'gender', 'department', 'hire_date']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('employee_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'email', 'address')
        }),
        ('Informations professionnelles', {
            'fields': ('hire_date', 'specialization', 'department', 'status', 'salary')
        }),
        ('Système', {
            'fields': ('user',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Nom complet'
