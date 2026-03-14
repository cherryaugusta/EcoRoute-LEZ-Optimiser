from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


class CorrelationIdMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        header_name = getattr(settings, "CORRELATION_HEADER", "X-Correlation-ID")
        inbound = request.headers.get(header_name, "")
        cid = self._normalise(inbound) or str(uuid.uuid4())

        correlation_id_var.set(cid)
        request.correlation_id = cid  # type: ignore[attr-defined]

        response = self.get_response(request)
        response[header_name] = cid
        return response

    @staticmethod
    def _normalise(value: str) -> str:
        v = (value or "").strip()
        if not v:
            return ""
        try:
            return str(uuid.UUID(v))
        except ValueError:
            return ""
