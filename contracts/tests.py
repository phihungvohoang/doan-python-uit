from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from properties.models import Property
from rooms.models import Room
from tenants.models import Tenant

User = get_user_model()


class ContractAPITest(TestCase):
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
            address="TP.HCM"
        )

        self.room = Room.objects.create(
            property=self.property,
            room_number="P101",
            area=20,
            price=2500000,
            max_people=2,
            status="AVAILABLE"
        )

        self.tenant = Tenant.objects.create(
            full_name="Nguyễn Văn A",
            phone="0909000000",
            identity_number="123456789"
        )

    def test_create_contract_success_and_room_occupied(self):
        data = {
            "room": self.room.id,
            "tenant": self.tenant.id,
            "start_date": "2026-05-01",
            "end_date": "2027-05-01",
            "deposit": 2500000,
            "monthly_price": 2500000,
            "status": "ACTIVE"
        }

        response = self.client.post("/api/contracts/", data)

        self.assertEqual(response.status_code, 201)

        self.room.refresh_from_db()
        self.assertEqual(self.room.status, "OCCUPIED")