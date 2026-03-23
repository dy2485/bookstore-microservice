# Generated manually for default roles

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


def create_default_roles(apps, schema_editor):
    """Create default roles for the system"""
    Role = apps.get_model('app', 'Role')

    # Create default roles with permissions
    roles_data = [
        {
            'name': 'user',
            'permissions': {
                'can_read_own_profile': True,
                'can_update_own_profile': True,
                'can_change_password': True,
            }
        },
        {
            'name': 'staff',
            'permissions': {
                'can_read_own_profile': True,
                'can_update_own_profile': True,
                'can_change_password': True,
                'can_manage_books': True,
                'can_manage_orders': True,
                'can_view_reports': True,
            }
        },
        {
            'name': 'manager',
            'permissions': {
                'can_read_own_profile': True,
                'can_update_own_profile': True,
                'can_change_password': True,
                'can_manage_books': True,
                'can_manage_orders': True,
                'can_manage_staff': True,
                'can_view_reports': True,
                'can_manage_inventory': True,
            }
        },
        {
            'name': 'admin',
            'permissions': {
                'can_read_own_profile': True,
                'can_update_own_profile': True,
                'can_change_password': True,
                'can_manage_books': True,
                'can_manage_orders': True,
                'can_manage_staff': True,
                'can_manage_users': True,
                'can_assign_roles': True,
                'can_view_reports': True,
                'can_manage_inventory': True,
                'can_system_admin': True,
            }
        }
    ]

    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            name=role_data['name'],
            defaults={'permissions': role_data['permissions']}
        )
        if created:
            print(f"Created role: {role.name}")


def reverse_create_default_roles(apps, schema_editor):
    """Reverse migration - remove default roles"""
    Role = apps.get_model('app', 'Role')
    Role.objects.filter(name__in=['user', 'staff', 'manager', 'admin']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),  # Adjust this based on your actual initial migration
    ]

    operations = [
        migrations.RunPython(
            create_default_roles,
            reverse_code=reverse_create_default_roles
        ),
    ]