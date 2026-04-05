# Draft: Agent fallback — Next steps

## Requirements (confirmed)
- Implement operational fallback chain Sisyphus → Prometheus → Atlas, immediate-switch on quota/rate-limit
- Expose Prometheus metrics on /metrics/ and instrument fallback/circuit events
- TDD-first approach with deterministic integration tests (no external network)
- CI workflow runs lint, unit, integration, and metrics-smoke checks
- Create parent-level port-management document to avoid port collisions between 10 Vue projects

## Summary of current state
- Core orchestrator, error types, retry hook, metrics, tests, and CI workflow were implemented locally on branch `feature/agent-fallback-ci-tests`.
- Integration tests and local app startup validated: /health OK, /metrics/ exposes agent metrics.
- Remaining work centers on: creating canonical PORTS.md, wiring real agent adapters, pushing PR and running CI on remote, and production hardening (uvicorn/lifespan).

## Open Questions (require user decision)
- [DECISION 1] Push branch to remote and open PR now? (I need the remote repo URL or permission to push.)
- [DECISION 2] Should I immediately update the 10 Vue projects to read PORTS.md (push changes) or provide a helper script + instructions and leave code changes to each project owner? Options: (A) auto-apply small env loader in each project, (B) provide PORTS.md + helper script only. Default: B.
- [DECISION 3] Run a Momus high-accuracy review of the plan before pushing? Default: skip (faster), but available if you want a rigorous QA loop.

## Next-step candidates (short)
1. Create parent-folder PORTS.md (canonical ports map + rules + example per-project .env snippet) — low risk, one file.
2. Replace simulated agent_adapters in app.state with a repository-factory that instantiates agent-specific adapters (Sisyphus, Prometheus, Atlas) — medium risk, requires wiring and tests.
3. Push branch `feature/agent-fallback-ci-tests` to remote and open PR — requires remote/push permission; triggers CI.
4. Harden uvicorn/ASGI lifespan and startup pattern for production (avoid uvicorn.run(...) compatibility issues) — recommended before production deploy.
5. Apply PORTS.md usage to Vue projects: either (A) inject small loader to read parent PORTS.md or (B) generate per-project .env files and commit — needs policy choice.
6. Run Momus high-accuracy review of .sisyphus/plans/agent-fallback-operational.md and the implementation (expensive but raises confidence).

## Dependencies & blockers
- Pushing branch and running CI requires remote repo access.
- Replacing adapters requires tests to be extended to cover new wiring; CI should run before merge.
- Modifying Vue projects requires coordination with their owners or permission to commit across multiple repos if they are separate.

## Proposed default next action (recommended)
1. Create PORTS.md in the repo root and add an example .env snippet for the Vue projects. (Low effort, immediate value.)
2. After PORTS.md is created, implement the repository-factory for agent adapters in code (local), add unit tests for wiring, and run the full local test suite.
3. When ready, push branch and open PR; optionally run Momus review before merging if you want extra rigor.

## Draft actions to take now (I can perform if you approve)
- Create PORTS.md with canonical mapping and examples. (Estimated 15–30 minutes.)
- Implement repository-factory to replace simulated adapters and add corresponding unit tests. (Estimated 2–4 hours.)
- Prepare a PR description and checklist for reviewers (CI steps, test matrix, manual verification notes). (Estimated 20–40 minutes.)

## Assumptions
- You will grant push permission or provide the remote repo URL when you want me to push.
- Vue projects can reference a shared parent file or be given generated .env files; pick one.

## Open tasks assigned to user
- Provide remote repo URL or push permission to run the push-and-PR step.
- Decide whether Vue projects should be auto-updated or given a helper script (see Decision 2).

## Files I'll update if you approve
- PARENT_FOLDER/PORTS.md (new)
- src/application/services/agent_orchestrator.py (if further wiring needed)
- tests/unit/* (additional unit tests for adapter factory)

---

Update created: .sisyphus/drafts/agent-fallback-next-steps.md
