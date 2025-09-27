from django.contrib import admin
from .models import AcademicYear, Semester, Course, Section, Enrollment, Material, Assignment

# Register your models here.

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_year', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'academic_year']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits', 'is_active']
    list_filter = ['department', 'is_active', 'credits']
    search_fields = ['code', 'name', 'department']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['course', 'section_number', 'teacher', 'semester', 'max_capacity', 'classroom']
    list_filter = ['semester', 'course__department']
    search_fields = ['course__code', 'course__name', 'teacher__profile__user__last_name']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'section', 'enrollment_date', 'status']
    list_filter = ['status', 'enrollment_date', 'section__semester']
    search_fields = ['student__profile__user__username', 'section__course__code']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'upload_date', 'is_visible']
    list_filter = ['upload_date', 'is_visible', 'section__course']
    search_fields = ['title', 'section__course__code']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'due_date', 'max_points', 'created_date']
    list_filter = ['due_date', 'created_date', 'section__course']
    search_fields = ['title', 'section__course__code']
