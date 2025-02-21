from django.core.management.base import BaseCommand
from Userapp.models import Right, Role

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        rights = [
            "Create User", "Edit User", "Delete User",
            "Create Role", "Edit Role", "Delete Role",
            "Create Right", "Edit Right", "Delete Right"
        ]
        for right_name in rights:
            Right.objects.get_or_create(name=right_name)

        roles = {
            "Super Admin": Right.objects.all(),
            "Admin": Right.objects.exclude(name="Delete User"),
            "Operators": Right.objects.filter(name__in=["Create Right", "Edit Right"]),
            "Technicians": Right.objects.none(),
        }

        for role_name, rights in roles.items():
            role, created = Role.objects.get_or_create(name=role_name)
            role.rights.set(rights)
            role.save()
