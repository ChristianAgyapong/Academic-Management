from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Student, Teacher

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 1
    min_num = 1
    max_num = 1

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        # Save related objects (Profile) after the User is saved
        super().save_related(request, form, formsets, change)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'registration_number', 'admission_date', 'is_active']
    list_filter = ['is_active', 'admission_date']
    search_fields = ['student_id', 'registration_number', 'profile__user__first_name', 'profile__user__last_name']
    
    def get_full_name(self, obj):
        return obj.profile.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'department', 'experience_years', 'join_date', 'is_active']
    list_filter = ['is_active', 'department', 'join_date']
    search_fields = ['employee_id', 'department', 'profile__user__first_name', 'profile__user__last_name']
    
    def get_full_name(self, obj):
        return obj.profile.user.get_full_name()
    get_full_name.short_description = 'Full Name'
