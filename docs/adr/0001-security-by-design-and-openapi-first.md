# ADR 0001: Security-by-Design + OpenAPI-First Contracts

## Status
Accepted

## Context
A London ClimateTech / logistics portfolio project must demonstrate:
- secure defaults from day zero
- contract-driven API design
- typed clients with minimal drift risk
- governance artifacts for AI usage patterns

## Decision
- Django REST Framework + drf-spectacular for OpenAPI generation.
- Correlation-ID middleware enforcing UUID-only inbound IDs.
- Secret scanning via pre-commit hooks (detect-secrets + gitleaks) plus deterministic mock scanning.
- Dependency scanning via pip-audit and safety.
- Angular strict mode with typed interfaces mirroring API serializers.

## Consequences
- Slightly more boilerplate initially, significantly reduced integration and audit risk.
- Stronger change control: schema changes are explicit and detectable.
