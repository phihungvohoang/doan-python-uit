from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class TenantAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="123456",
            role="OWNER"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_tenant_success(self):
        data = {
            "full_name": "Nguyễn Văn B",
            "phone": "0123456789",
            "identity_number": "1111111111",
            "date_of_birth": "2000-01-01",
            "address": "TP.HCM"
        }

        response = self.client.post("/api/tenants/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["full_name"], "Nguyễn Văn B")