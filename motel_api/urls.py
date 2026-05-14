from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from properties.views import PropertyViewSet
from rooms.views import RoomViewSet
from tenants.views import TenantViewSet
from contracts.views import ContractViewSet
from invoices.views import InvoiceViewSet, UtilityReadingViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()

router.register("properties", PropertyViewSet, basename="properties")
router.register("rooms", RoomViewSet, basename="rooms")
router.register("tenants", TenantViewSet, basename="tenants")
router.register("contracts", ContractViewSet, basename="contracts")
router.register("invoices", InvoiceViewSet, basename="invoices")
router.register("utility-readings", UtilityReadingViewSet, basename="utility-readings")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),

    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),

    path(
    "api/schema/",
    SpectacularAPIView.as_view(),
    name="schema"
),

path(
    "api/docs/",
    SpectacularSwaggerView.as_view(url_name="schema"),
    name="swagger-ui"
),
]