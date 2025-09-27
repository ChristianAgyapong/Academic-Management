from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, UserRole


class Command(BaseCommand):
    help = 'Create profiles for users who don\'t have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            type=str,
            default='student',
            help='Default role for users without profiles (admin, teacher, student)',
        )

    def handle(self, *args, **options):
        default_role = options['role'].lower()
        
        # Validate role
        valid_roles = [choice[0] for choice in UserRole.choices]
        if default_role not in valid_roles:
            self.stdout.write(
                self.style.ERROR(f'Invalid role. Choose from: {", ".join(valid_roles)}')
            )
            return

        # Find users without profiles
        users_without_profiles = User.objects.filter(profile__isnull=True)
        
        created_count = 0
        for user in users_without_profiles:
            # Determine role based on user attributes
            role = default_role
            if user.is_superuser:
                role = UserRole.ADMIN
            
            Profile.objects.create(user=user, role=role)
            created_count += 1
            self.stdout.write(f'Created profile for user: {user.username} (role: {role})')

        if created_count == 0:
            self.stdout.write(
                self.style.SUCCESS('All users already have profiles.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} profiles.')
            )