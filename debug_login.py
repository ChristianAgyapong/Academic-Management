#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import Profile, Student, Teacher

# Check demo users
print("=== DEMO USERS CHECK ===")
try:
    student_user = User.objects.get(username='student001')
    print(f"Student user exists: {student_user.username}")
    
    student_profile = student_user.profile
    print(f"Student profile exists: Role = {student_profile.role}")
    
    student_obj = Student.objects.get(profile=student_profile)
    print(f"Student object exists: ID = {student_obj.student_id}")
    
    # Test authentication
    auth_user = authenticate(username='student001', password='student123')
    print(f"Authentication successful: {auth_user is not None}")
    
except Exception as e:
    print(f"Error with student001: {e}")

print("\n=== TEACHER CHECK ===")
try:
    teacher_user = User.objects.get(username='teacher001')
    print(f"Teacher user exists: {teacher_user.username}")
    
    teacher_profile = teacher_user.profile
    print(f"Teacher profile exists: Role = {teacher_profile.role}")
    
    teacher_obj = Teacher.objects.get(profile=teacher_profile)
    print(f"Teacher object exists: ID = {teacher_obj.employee_id}")
    
except Exception as e:
    print(f"Error with teacher001: {e}")

print("\n=== ALL USERS ===")
for user in User.objects.all():
    try:
        profile = user.profile
        print(f"User: {user.username}, Role: {profile.role}")
    except:
        print(f"User: {user.username}, No profile!")