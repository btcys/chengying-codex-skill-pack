# AGENTS.md

## Collaboration Rules

- Communicate requirements, scope, risks, validation, and rollback before coding.
- Use the smallest change that satisfies the current task.
- Do not modify unrelated modules.
- Do not touch data, permissions, APIs, deployment, or dependencies without explicit confirmation.

## Workflow

- Lean: use a lightweight work order with goal, non-goal, allowed changes, forbidden changes, validation, and rollback.
- Standard: use `docs/codex/` PRD, design, technical spec, phase plan, validation, and handoff documents.
- Enterprise: add architecture, security, privacy, release, review, and threading governance.
- PM Thread does not edit business code. Level 2 / Standard and Level 3 / Enterprise work must be dispatched to an Execution Thread or an existing execution thread; if thread tools are unavailable, output an Execution Thread task package and stop at `blocked_waiting_for_execution_thread`.
