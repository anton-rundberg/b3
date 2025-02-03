from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path(
        "reset-password-confirm/<uuid:user_id>/",
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path("csrf/", views.CSRFAPIView.as_view(), name="csrf"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
