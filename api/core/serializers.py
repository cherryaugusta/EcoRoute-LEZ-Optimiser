from __future__ import annotations

from rest_framework import serializers
from core.models import RouteAuditRecord


class RouteAuditRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAuditRecord
        fields = [
            "id",
            "created_at",
            "origin",
            "destination",
            "fleet_type",
            "goal",
            "restricted_zones_avoided",
            "compliance_explanation",
            "estimated_cost_pence",
            "estimated_distance_km",
            "estimated_duration_seconds",
            "emissions_kg_co2e",
            "emissions_breakdown",
        ]
        read_only_fields = ["id", "created_at"]
