from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from properties.models import Property
from rooms.models import Room

User = get_user_model()


class RoomAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="123456",
            role="OWNER"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.property = Property.objects.create(
            owner=self.user,
            name="Nhà trọ A",
            address="TP.HCM",
            total_floors=3
        )

    def test_create_room_success(self):
        data = {
            "property": self.property.id,
            "room_number": "P101",
            "area": 20,
            "price": 2500000,
            "max_people": 2,
            "status": "AVAILABLE"
        }

        response = self.client.post("/api/rooms/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["room_number"], "P101")

    def test_list_rooms_success(self):
        Room.objects.create(
            property=self.property,
            room_number="P102",
            area=25,
            price=3000000,
            max_people=3,
            status="AVAILABLE"
        )

        response = self.client.get("/api/rooms/")

        self.assertEqual(response.status_code, 200)