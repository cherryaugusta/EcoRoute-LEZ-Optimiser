from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any

import redis
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import RouteAuditRecord
from core.serializers import RouteAuditRecordSerializer


@dataclass(frozen=True)
class DependencyStatus:
    ok: bool
    detail: str


class HealthCheckView(APIView):
    authentication_classes: list[Any] = []
    permission_classes: list[Any] = []

    def get(self, request: Request) -> Response:
        db = self._check_db()
        rd = self._check_redis()

        all_ok = db.ok and rd.ok
        payload = {
            "status": "ok" if all_ok else "degraded",
            "correlation_id": getattr(request, "correlation_id", None),
            "database": asdict(db),
            "redis": asdict(rd),
        }
        return Response(
            payload,
            status=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    @staticmethod
    def _check_db() -> DependencyStatus:
        try:
            conn = connections["default"]
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()
            return DependencyStatus(ok=True, detail="reachable")
        except OperationalError as exc:
            return DependencyStatus(ok=False, detail=f"unreachable: {exc.__class__.__name__}")

    @staticmethod
    def _check_redis() -> DependencyStatus:
        try:
            client = redis.Redis.from_url(
                settings.REDIS_URL,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            pong = client.ping()
            return DependencyStatus(ok=bool(pong), detail="reachable" if pong else "no-pong")
        except Exception as exc:  # noqa: BLE001
            return DependencyStatus(ok=False, detail=f"unreachable: {exc.__class__.__name__}")


class RouteAuditRecordCreateView(CreateAPIView):
    queryset = RouteAuditRecord.objects.all()
    serializer_class = RouteAuditRecordSerializer


class RouteAuditRecordListView(ListAPIView):
    queryset = RouteAuditRecord.objects.order_by("-created_at")
    serializer_class = RouteAuditRecordSerializer


class ExampleDeterministicAuditComputeView(APIView):
    authentication_classes: list[Any] = []
    permission_classes: list[Any] = []

    def post(self, request: Request) -> Response:
        body = request.data or {}
        origin = str(body.get("origin", "London Bridge"))
        destination = str(body.get("destination", "Heathrow T5"))
        fleet_type = str(body.get("fleet_type", "ev"))
        goal = str(body.get("goal", "greenest"))

        restricted = ["ULEZ", "LEZ"]
        explanation = (
            f"Selected a route designed to avoid restricted polygons tagged {restricted}. "
            "No restricted-zone edge traversals were included in the path search result."
        )

        distance_km = Decimal("27.40")
        duration_s = 3400
        cost_pence = 980
        emissions = Decimal("1.240") if fleet_type == "ev" else Decimal("6.800")

        payload = {
            "origin": origin,
            "destination": destination,
            "fleet_type": fleet_type,
            "goal": goal,
            "restricted_zones_avoided": restricted,
            "compliance_explanation": explanation,
            "estimated_cost_pence": cost_pence,
            "estimated_distance_km": str(distance_km),
            "estimated_duration_seconds": duration_s,
            "emissions_kg_co2e": str(emissions),
            "emissions_breakdown": {"traction": float(emissions), "upstream": 0.0},
        }
        return Response(payload, status=status.HTTP_200_OK)
