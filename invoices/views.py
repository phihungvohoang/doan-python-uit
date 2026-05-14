from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Invoice, UtilityReading
from .serializers import InvoiceSerializer, UtilityReadingSerializer
from contracts.models import Contract
from accounts.permissions import IsStaffOrOwner


class UtilityReadingViewSet(ModelViewSet):
    queryset = UtilityReading.objects.all()
    serializer_class = UtilityReadingSerializer
    permission_classes = [IsStaffOrOwner]

    filterset_fields = ["contract", "month", "year"]


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsStaffOrOwner]

    filterset_fields = ["status", "month", "year", "contract"]

    def perform_create(self, serializer):
        room_fee = serializer.validated_data["room_fee"]
        electric_fee = serializer.validated_data.get("electric_fee", 0)
        water_fee = serializer.validated_data.get("water_fee", 0)
        service_fee = serializer.validated_data.get("service_fee", 0)

        total = room_fee + electric_fee + water_fee + service_fee
        serializer.save(total_amount=total)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate_invoice(self, request):
        contract_id = request.data.get("contract_id")
        month = request.data.get("month")
        year = request.data.get("year")
        service_fee = request.data.get("service_fee", 0)
        due_date = request.data.get("due_date")

        if not contract_id or not month or not year or not due_date:
            return Response(
                {"message": "Thiếu contract_id, month, year hoặc due_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        contract = Contract.objects.get(
            id=contract_id,
            status=Contract.Status.ACTIVE
        )

        if Invoice.objects.filter(
            contract=contract,
            month=month,
            year=year
        ).exists():
            return Response(
                {"message": "Hóa đơn tháng này đã tồn tại."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reading = UtilityReading.objects.get(
            contract=contract,
            month=month,
            year=year
        )

        room_fee = contract.monthly_price
        electric_fee = reading.electric_fee()
        water_fee = reading.water_fee()
        total = room_fee + electric_fee + water_fee + int(service_fee)

        invoice = Invoice.objects.create(
            contract=contract,
            month=month,
            year=year,
            room_fee=room_fee,
            electric_fee=electric_fee,
            water_fee=water_fee,
            service_fee=service_fee,
            total_amount=total,
            due_date=due_date,
        )

        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["patch"], url_path="mark-paid")
    def mark_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.status = Invoice.Status.PAID
        invoice.save()

        return Response({"message": "Đã thanh toán hóa đơn."})