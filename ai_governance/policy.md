# AI Governance Policy (Portfolio Demonstration)

## Scope
This repository includes an AI governance folder to demonstrate enterprise patterns for managing prompt use, evaluation artifacts, and disclosure boundaries. The application is not required to call an LLM to operate.

## Non-negotiables
- No production secrets in prompts, examples, or evaluation logs.
- No personal data processing without an explicit DPIA-style review.
- Human-in-the-loop (HITL) required for any compliance-relevant narrative output (e.g., “why this route is compliant”).

## Prompt catalog controls
- Every prompt must have:
  - owner, purpose, data classification, allowed inputs, disallowed inputs
  - known failure modes
  - evaluation criteria and test fixtures
- Prompts must be versioned. Deprecations must be recorded.

## Evaluation controls
- Evaluations must be reproducible:
  - fixed test fixtures
  - deterministic scoring rules where feasible
- Store evaluation outcomes as JSON. Avoid raw user content.

## Disclosure controls
- Any AI-assisted output must:
  - state limitations
  - include uncertainty language where applicable
  - provide traceability to inputs and rules used
  - prohibit fabricated citations and unverifiable claims
