# AGENTS.md

## Collaboration Rules

- Think before coding: clarify goal, current state, impact, plan, validation, and rollback.
- Use the smallest change that satisfies the current task.
- Read relevant files before editing and follow existing architecture/style.
- Do not modify unrelated modules or perform opportunistic refactors.
- Do not touch data, permissions, APIs, deployment, dependencies, protected branches, or destructive operations without explicit confirmation.
- Do not claim validation passed unless it was actually run.

## Workflow

- Use a short task card before code changes.
- Continue implementation, testing, and fixing in the current thread when the task is clear.
- Create PRD / TECH_SPEC / PHASE_PLAN / VALIDATION / HANDOFF only when they help execution, verification, handoff, or long-term maintenance.
- Keep `docs/codex/CURRENT_STATE.md` updated for long-running project context.
- Use Handoff only when work must move to another thread/person.

## Result

After changes, report what changed, files touched, validation run, unverified risks, and next steps.
