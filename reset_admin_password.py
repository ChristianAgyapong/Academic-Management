import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Get the admin user
    admin = User.objects.get(username='admin')
    
    # Reset the password to admin123
    admin.set_password('admin123')
    admin.save()
    
    print("Admin password reset successfully!")
    print("Username: admin")
    print("Password: admin123")
    
    # Test authentication
    from django.contrib.auth import authenticate
    auth_result = authenticate(username='admin', password='admin123')
    print(f"Authentication test: {auth_result is not None}")
    
    if auth_result:
        print("✅ Admin login should now work!")
    else:
        print("❌ Authentication still failing")
        
except User.DoesNotExist:
    print("Admin user not found. Creating new admin user...")
    
    # Create admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@cta.com',
        password='admin123'
    )
    print("✅ Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    
except Exception as e:
    print(f"Error: {e}")