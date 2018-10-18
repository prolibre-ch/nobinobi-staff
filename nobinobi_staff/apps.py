from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def load_group_and_permissions(sender, **kwargs):
    """Load an initial group and its permissions"""
    from django.contrib.auth.models import Group, Permission
    groupe_personnel = Group.objects.get_or_create(
        name='Personnel'
    )[0]
    permissions_names = [
        'can_read_list',
    ]
    permissions = [
        Permission.objects.get(codename=permission_name)
        for permission_name
        in permissions_names
    ]
    for permission in permissions:
        groupe_personnel.permissions.add(permission)


def load_fixtures_personal(sender, **kwargs):
    from django.core.management import call_command
    call_command("loaddata", "staff_qualification_{}".format(settings.LANGUAGE_CODE))
    call_command("loaddata", "staff_absence_type_{}".format(settings.LANGUAGE_CODE))


class NobinobiStaffConfig(AppConfig, object):
    name = 'nobinobi_staff'
    verbose_name = _("Staff")
    verbose_name_plural = _("Staffes")

    def ready(self):
        post_migrate.connect(load_fixtures_personal, sender=self)
        # post_migrate.connect(load_group_and_permissions, sender=self)
