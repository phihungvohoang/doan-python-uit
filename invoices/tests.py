from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal

from properties.models import Property
from rooms.models import Room
from tenants.models import Tenant
from contracts.models import Contract
from invoices.models import UtilityReading, Invoice

User = get_user_model()


class InvoiceAPITest(TestCase):
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
            status="OCCUPIED"
        )

        self.tenant = Tenant.objects.create(
            full_name="Nguyễn Văn A",
            phone="0909000000",
            identity_number="123456789"
        )

        self.contract = Contract.objects.create(
            room=self.room,
            tenant=self.tenant,
            start_date="2026-05-01",
            end_date="2027-05-01",
            deposit=2500000,
            monthly_price=2500000,
            status="ACTIVE"
        )

    def test_generate_invoice_success(self):
        UtilityReading.objects.create(
            contract=self.contract,
            month=5,
            year=2026,
            old_electric=100,
            new_electric=150,
            old_water=20,
            new_water=25,
            electric_price=3500,
            water_price=15000
        )

        data = {
            "contract_id": self.contract.id,
            "month": 5,
            "year": 2026,
            "service_fee": 100000,
            "due_date": "2026-05-31"
        }

        response = self.client.post("/api/invoices/generate/", data)

        print("\n===== KẾT QUẢ TEST TẠO HÓA ĐƠN =====")
        print("Status code:", response.status_code)
        print("Dữ liệu trả về:", response.data)
        print("Tên người thuê:", response.data.get("tenant_name"))
        print("Số phòng:", response.data.get("room_number"))
        print("Tiền phòng:", response.data.get("room_fee"))
        print("Tiền điện:", response.data.get("electric_fee"))
        print("Tiền nước:", response.data.get("water_fee"))
        print("Phí dịch vụ:", response.data.get("service_fee"))
        print("Tổng tiền:", response.data.get("total_amount"))
        print("====================================\n")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Decimal(response.data["total_amount"]),
            Decimal("2850000.00")
        )

    def test_mark_invoice_paid_success(self):
        invoice = Invoice.objects.create(
            contract=self.contract,
            month=5,
            year=2026,
            room_fee=2500000,
            electric_fee=175000,
            water_fee=75000,
            service_fee=100000,
            total_amount=2850000,
            due_date="2026-05-31",
            status="UNPAID"
        )

        response = self.client.patch(f"/api/invoices/{invoice.id}/mark-paid/")

        invoice.refresh_from_db()

        print("\n===== KẾT QUẢ TEST THANH TOÁN HÓA ĐƠN =====")
        print("Status code:", response.status_code)
        print("Dữ liệu trả về:", response.data)
        print("Trạng thái hóa đơn sau thanh toán:", invoice.status)
        print("==========================================\n")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(invoice.status, "PAID")