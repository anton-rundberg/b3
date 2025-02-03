from .settings import *  # NOQA

TEST = True
DEBUG = False

DATABASES["default"]["OPTIONS"]["sslmode"] = "disable"  # noqa: F405

# Always use OTPAdminConfig in tests to keep env same as prod (OTPAdminConfiig has different permission checks)
if "django.contrib.admin" in INSTALLED_APPS:  # noqa: F405
    INSTALLED_APPS.remove("django.contrib.admin")  # noqa: F405
if "b3.apps.OTPAdminConfig" not in INSTALLED_APPS:  # noqa: F405
    INSTALLED_APPS.append("b3.apps.OTPAdminConfig")  # noqa: F405


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
}

CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = "memory://"
CELERY_BACKEND = "memory"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",  # to prevent API throttling
    }
}
