from rest_framework.viewsets import ModelViewSet
from .models import Property
from .serializers import PropertySerializer
from accounts.permissions import IsStaffOrOwner


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsStaffOrOwner]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)