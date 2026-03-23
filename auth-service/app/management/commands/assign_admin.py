from django.core.management.base import BaseCommand
from app.models import User, Role, UserRole

class Command(BaseCommand):
    help = 'Assign admin role to first user'

    def handle(self, *args, **options):
        try:
            # Get first user
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('No users found'))
                return

            # Get or create admin role
            admin_role, _ = Role.objects.get_or_create(name='admin')
            
            # Check if user already has admin role
            if UserRole.objects.filter(user=user, role=admin_role).exists():
                self.stdout.write(self.style.SUCCESS(f'User {user.username} already has admin role'))
                return
            
            # Assign admin role
            UserRole.objects.create(user=user, role=admin_role)
            self.stdout.write(self.style.SUCCESS(f'Assigned admin role to user {user.username}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))