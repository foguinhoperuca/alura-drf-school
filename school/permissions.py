from rest_framework.permissions import DjangoModelPermissions


class StrictDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
