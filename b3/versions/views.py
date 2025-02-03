from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from . import models, serializers


class VersionsView(generics.RetrieveAPIView):
    serializer_class = serializers.VersionSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get_object(self):
        try:
            return models.Version.objects.latest("created_at")
        except models.Version.DoesNotExist:
            raise Http404
