#!/usr/bin/env python
"""
Convert existing users to teachers for attendance demo.
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile, Teacher

def convert_user_to_teacher(username):
    """Convert an existing user to a teacher."""
    try:
        user = User.objects.get(username=username)
        
        # Check if user already has a profile
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.role = 'teacher'
            profile.save()
        else:
            profile = Profile.objects.create(user=user, role='teacher')
        
        # Create or get teacher profile
        teacher, created = Teacher.objects.get_or_create(
            profile=profile,
            defaults={
                'employee_id': f'T{user.id}',
                'department': 'Faculty',
                'qualification': 'PhD',
                'experience_years': 5,
                'join_date': date(2024, 1, 15)
            }
        )
        
        if created:
            print(f"✅ Converted {username} to teacher")
        else:
            print(f"✅ {username} is already a teacher")
            
        return teacher
        
    except User.DoesNotExist:
        print(f"❌ User {username} not found")
        return None

if __name__ == '__main__':
    print("🔧 Converting existing users to teachers...")
    
    # Convert ms.antwi to teacher
    teacher = convert_user_to_teacher('ms.antwi')
    
    if teacher:
        print(f"✅ Successfully set up teacher: {teacher.profile.user.username}")
        print(f"   Employee ID: {teacher.employee_id}")
        print(f"   Department: {teacher.department}")
    
    print("\n🎉 Setup complete! You can now test the attendance system with teacher account 'ms.antwi'")