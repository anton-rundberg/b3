from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from . import models, permissions, serializers, tasks


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        login(self.request, user)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["email"]
        tasks.send_reset_password_email.si(user.pk).delay()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordConfirmView(generics.UpdateAPIView):
    serializer_class = serializers.ResetPasswordConfirmSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(models.User, pk=self.kwargs["user_id"])


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Removes the currently logged in user (requires field 'password')
    """

    serializer_class = serializers.UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        perms = super().get_permissions()
        if self.request.method not in (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "OPTIONS",
        ):
            perms.append(permissions.PasswordPermission())
        return perms

    def get_object(self):
        return self.request.user


class LoginThrottle(AnonRateThrottle):
    rate = "overriden/below"  # Needed but overriden by parse_rate()

    def parse_rate(self, rate):
        return 10, 60 * 15  # 10 requests per 15 minutes


class CSRFAPIView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        # See cookie-auth.md
        csrf_token = get_token(request)  # TODO: Needed if we run on same domain?
        return Response({"csrf_token": csrf_token})


@method_decorator(sensitive_post_parameters(), name="dispatch")
@method_decorator(csrf_protect, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (LoginThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(never_cache, name="dispatch")
class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
