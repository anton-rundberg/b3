"""b3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("task-list/", include("task_lists.urls", namespace="task_list")),
    path("users/", include("users.urls", namespace="users")),
    path("versions/", include("versions.urls", namespace="versions")),
]

# OpenAPI docs
if os.getenv("ENV") in ("LOCAL", "DEV"):
    urlpatterns.extend(
        [
            path(
                "docs/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger",
            ),
            path(
                "docs/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc",
            ),
            path("docs/openapi/", SpectacularAPIView.as_view(), name="schema"),
        ]
    )

# Debug toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Media files for local dev
if os.getenv("ENV") == "LOCAL":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
