from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication


class CSRFProtectMixin:
    # DRF disables CSRF protection when a user is not authenticated so if we want to do
    # non-safe requests (POST, PATCH, DELETE) for non-authenticated users, we need to
    # add CSRF protection manually.
    #
    # Adding this will break all auth methods which are not SessionAuthentication so if
    # you for some reason need the endpoint to also work logged in with another auth
    # method, you'll need to think your implementation through.
    #
    # See https://stackoverflow.com/questions/49275069/csrf-is-only-checked-when-authenticated-in-drf
    authentication_classes = (SessionAuthentication,)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
