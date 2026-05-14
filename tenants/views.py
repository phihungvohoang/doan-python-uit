from rest_framework.viewsets import ModelViewSet
from .models import Tenant
from .serializers import TenantSerializer
from accounts.permissions import IsStaffOrOwner


class TenantViewSet(ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsStaffOrOwner]

    search_fields = ["full_name", "phone", "identity_number"]