from django.urls import path

from core.views import (
    ExampleDeterministicAuditComputeView,
    HealthCheckView,
    RouteAuditRecordCreateView,
    RouteAuditRecordListView,
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("audit-records/", RouteAuditRecordListView.as_view(), name="audit-records-list"),
    path(
        "audit-records/create/",
        RouteAuditRecordCreateView.as_view(),
        name="audit-records-create",
    ),
    path("audit/compute/", ExampleDeterministicAuditComputeView.as_view(), name="audit-compute"),
]
