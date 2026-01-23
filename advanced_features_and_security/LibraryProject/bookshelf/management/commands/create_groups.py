from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Creates default groups with permissions'

    def handle(self, *args, **kwargs):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all permissions for Book model
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Create groups and assign permissions
        groups_permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }
        
        for group_name, perm_codenames in groups_permissions.items():
            # Create or get the group
            group, created = Group.objects.get_or_create(name=group_name)
            
            # Clear existing permissions (if any)
            group.permissions.clear()
            
            # Add new permissions
            for codename in perm_codenames:
                try:
                    # Find the permission by codename
                    perm = permissions.get(codename=codename)
                    group.permissions.add(perm)
                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Added permission {codename} to group {group_name}'
                    ))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'⚠ Permission {codename} not found for Book model'
                    ))
            
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'✅ Created new group: {group_name}'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'🔄 Updated existing group: {group_name}'
                ))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All groups created successfully!'))
