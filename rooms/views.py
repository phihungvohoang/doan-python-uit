from rest_framework.viewsets import ModelViewSet
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filterset_fields = ["status", "property"]
    search_fields = ["room_number"]
    ordering_fields = ["price", "area"]