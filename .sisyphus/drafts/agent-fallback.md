# Draft: Agent Fallback Policy

## Requirements (confirmed)
- "제한이 걸리면 자동으로 바꿔 agent" — 사용자가 요청한 동작을 그대로 기록합니다.

## Technical Decisions (proposed)
- Default fallback agent: When '시시프스' limits are hit, trigger a fallback chain: Prometheus first, escalate to Atlas if needed.
- Scope: Global fallback (applies when Sisyphus quota/block is detected). Per-error-type mapping remains an advanced option.

## Research Findings
- 프로젝트 루트 및 README 확인 완료. .sisyphus/plans 디렉토리는 현재 없음(읽기 시 파일 없음 응답).
- 코드베이스는 backend(src)와 frontend 디렉토리가 분리되어 있으며, 다양한 에이전트(AGENTS.md) 정의가 존재함.

## Open Questions
1. Retry policy: Do you want immediate switch (current default) or Prometheus retry N times before escalating to Atlas? (recommended: immediate)
2. Exceptions: Should long-running background tasks be exempted from fallback switching?

## Scope Boundaries
INCLUDE: 계획 문서화 — 에이전트 자동 전환 정책 설계 (작업 계획으로 변환 가능).
EXCLUDE: 런타임 코드/설정 변경, 에이전트 구현 또는 권한 수정.

## Operational Behavior
- Trigger: On detection of Sisyphus limits (quotas, model blocking, rate limiting) the fallback chain starts.
- Chain order: Sisyphus → Prometheus → Atlas.
- Retry: Default is immediate switch (no retries). If retry behavior is desired, update Open Question #1.
- Logging: Transition events should be logged to .sisyphus/logs/agent-fallback.log (implementation task required).
