import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

try:
    # Check if admin user exists
    admin = User.objects.filter(username='admin').first()
    print(f"Admin user exists: {admin is not None}")
    
    if admin:
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Is superuser: {admin.is_superuser}")
        print(f"Is staff: {admin.is_staff}")
        print(f"Is active: {admin.is_active}")
        print(f"Last login: {admin.last_login}")
        print(f"Date joined: {admin.date_joined}")
        
        # Test authentication
        auth_result = authenticate(username='admin', password='admin123')
        print(f"Authentication with 'admin123': {auth_result is not None}")
        
        # Check if user has a password set
        print(f"Has usable password: {admin.has_usable_password()}")
        
    else:
        print("Admin user does not exist!")
        print("Creating admin user now...")
        
        # Create admin user
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@sams.com',
            password='admin123'
        )
        print("Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        
except Exception as e:
    print(f"Error: {e}")