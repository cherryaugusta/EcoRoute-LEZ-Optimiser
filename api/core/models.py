from __future__ import annotations

import uuid
from django.db import models


class RouteAuditRecord(models.Model):
    class FleetType(models.TextChoices):
        DIESEL = "diesel", "Diesel"
        HYBRID = "hybrid", "Hybrid"
        EV = "ev", "EV"

    class OptimisationGoal(models.TextChoices):
        FASTEST = "fastest", "Fastest"
        CHEAPEST = "cheapest", "Cheapest"
        GREENEST = "greenest", "Greenest"
        BALANCED = "balanced", "Balanced"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    origin = models.CharField(max_length=256)
    destination = models.CharField(max_length=256)

    fleet_type = models.CharField(max_length=16, choices=FleetType.choices)
    goal = models.CharField(max_length=16, choices=OptimisationGoal.choices)

    restricted_zones_avoided = models.JSONField(default=list)
    compliance_explanation = models.TextField()

    estimated_cost_pence = models.PositiveIntegerField()
    estimated_distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_duration_seconds = models.PositiveIntegerField()

    emissions_kg_co2e = models.DecimalField(max_digits=10, decimal_places=3)
    emissions_breakdown = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f"{self.origin} -> {self.destination} ({self.fleet_type}, {self.goal})"
