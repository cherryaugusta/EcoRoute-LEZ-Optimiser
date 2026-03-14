from django.contrib import admin

from core.models import RouteAuditRecord


@admin.register(RouteAuditRecord)
class RouteAuditRecordAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "origin",
        "destination",
        "fleet_type",
        "goal",
        "emissions_kg_co2e",
    )
    search_fields = ("origin", "destination", "compliance_explanation")
    list_filter = ("fleet_type", "goal", "created_at")
