from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Contract
from .serializers import ContractSerializer
from rooms.models import Room


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def perform_create(self, serializer):
        contract = serializer.save()
        contract.room.status = Room.Status.OCCUPIED
        contract.room.save()

    @action(detail=True, methods=["patch"])
    def terminate(self, request, pk=None):
        contract = self.get_object()
        contract.status = Contract.Status.TERMINATED
        contract.save()

        contract.room.status = Room.Status.AVAILABLE
        contract.room.save()

        return Response({"message": "Đã kết thúc hợp đồng."})