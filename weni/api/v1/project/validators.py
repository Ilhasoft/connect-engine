from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import PermissionDenied


class CanContributeInOrganizationValidator(object):
    def __call__(self, value):
        user_authorization = value.get_user_authorization(self.request.user)
        if not user_authorization.can_contribute:
            raise PermissionDenied(_("You can't contribute in this organization"))

    def set_context(self, serializer):
        self.request = serializer.context.get("request")
