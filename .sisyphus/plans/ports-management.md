# Plan: Repository Port Management (PORTS.md + tooling)

## TL;DR
> Summary: Add a single source-of-truth for developer ports (human PORTS.md + machine ports.json + ports.schema.json), a Python-based validator and env-generator (scripts/ports_validate.py, scripts/ports_generate_env.py), TDD-first tests, and a CI validator job that blocks PRs that introduce port conflicts.
> Deliverables:
- PORTS.md (human-friendly) in repo root
- ports.json (machine sidecar) in repo root
- ports.schema.json (JSON Schema v1.0)
- scripts/ports_validate.py (validator using jsonschema)
- scripts/ports_generate_env.py (generator that writes .env.local with fallback logic)
- tests/ports/test_validator.py and tests/ports/test_generator.py (pytest)
- CI snippet to add to .github/workflows/ci.yml
> Effort: Short → Medium (one developer, 2–4 hours to implement, tests and CI integration)
> Parallel: YES - validator tests and generator tasks can be worked concurrently.
> Critical Path: ports.json + ports.schema.json → validator + unit tests → CI job → generator + generator tests

## Context
### Original Request
Create a parent-folder .md file to standardize port assignments for the 10 Vue.js projects on the host and provide a helper for projects to read port assignments; add TDD-first validator + generator tooling and CI enforcement.

### Interview Summary / Metis Review
- Metis recommended: both a human PORTS.md and a machine-readable ports.json. Use JSON for sidecar and Python for scripts to match repository (scripts/process_manager.py exists).
- Metis recommended enforcement via CI, owner model (team-level), fallback rules, and a generator that writes .env.local with a DO NOT COMMIT header.

### Assumptions (decisions made by this plan)
- Scope: development-only (dev servers, local runs). Production/CI/staging ports are OUT of scope unless explicitly requested later.
- Enforcement: CI will BLOCK PRs that add port collisions or invalid entries (default enforcement enabled in ports.json entries unless explicitly disabled per-entry).
- Ownership: Team-level ownership with placeholder emails. Implementer must replace with real owner/team handles at commit time.
- Toolchain: Vite-based Vue projects only (repo evidence: vite used). If other toolchains are present, the validator will treat them as extensions.
- Platform support: Python scripts will be cross-platform (macOS/Linux/Windows) using the Python standard library for port checks.

## Work Objectives
### Core Objective
Provide a deterministic, TDD-verified system for assigning and validating development ports across repository projects and to provide an automated local .env.local generator with fallback behavior.

### Deliverables (exact file paths)
- PORTS.md (repo root) — human-readable table and process
- ports.json (repo root) — machine sidecar JSON (schema_version + services)
- ports.schema.json (repo root) — JSON Schema
- scripts/ports_validate.py — CLI validator
- scripts/ports_generate_env.py — CLI generator
- tests/ports/test_validator.py — pytest tests for validator
- tests/ports/test_generator.py — pytest tests for generator
- CI: .github/workflows/ci.yml — add job step 'ports-validator' (YAML snippet included in this plan)

### Definition of Done (verifiable commands)
- ports.json exists and validates against ports.schema.json
  Command: python3 -m scripts.ports_validate --file ./ports.json
  Expected stdout: OK: no port conflicts found
  Exit code: 0
- Validator unit tests pass
  Command: pytest tests/ports/test_validator.py -q
  Expected: all tests pass
- Generator deterministic output
  Command: python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local
  Expected file content (exact):
  # GENERATED FROM ports.json - DO NOT COMMIT
  VITE_PORT=5173

## Verification Strategy
- TDD-first: write unit tests for validator and generator before implementation. Tests will be run by pytest.
- Validator uses jsonschema (python jsonschema) plus repo scan for port occurrences (regex patterns). Tests use temporary directories.
- CI: add a ports-validator job that runs validator across ports.json and scanned configs and fails on any conflict.

## Execution Strategy
Work will be split into three waves to maximize parallel work and early verification.

Wave 1 (foundation, parallelizable)
- Create ports.schema.json and example ports.json with frontend (5173) and backend (8000) entries.
- Create PORTS.md human-readable with table and contributor guidance.
- Add tests skeleton files (tests/ports/test_validator.py, tests/ports/test_generator.py) with TDD-first failing tests.

Wave 2 (implementation)
- Implement scripts/ports_validate.py (jsonschema validation, duplicate detection, repo scan) to satisfy tests.
- Implement scripts/ports_generate_env.py (generator + fallback logic) to satisfy tests.
- Add unit tests for fallback behavior (simulate port in-use via ephemeral server socket in test).

Wave 3 (CI + docs)
- Add CI job step to run python3 -m scripts.ports_validate --file ./ports.json and pytest tests/ports -q
- Update CONTRIBUTING.md with ports editing procedure and CODEOWNERS suggestion.

### Dependency Matrix (high level)
- ports.schema.json → ports.json → validator → CI
- ports.json → generator → per-project .env.local

## TODOs (detailed tasks)
- [ ] 1. Create ports.schema.json (file content in References below)

  What to do: Add JSON Schema file exactly as provided in References. Place at repo root as ports.schema.json.
  Must NOT do: Allow unknown top-level keys without schema bump.

  Recommended Agent Profile:
  - Category: writing — Reason: precise spec document creation
  - Skills: [`python`, `jsonschema`] — for schema design and validator integration

  Parallelization: Can be done in Wave 1, doesn't block other tasks.

  References:
  - ports.schema.json: See 'References: ports.schema.json' section below.

  Acceptance Criteria:
  - File exists at ./ports.schema.json
  - python -c "import json, jsonschema, sys; jsonschema.Draft7Validator.check_schema(json.load(open('ports.schema.json')))" returns no exception

  QA Scenarios:
  Scenario: Schema parse
    Tool: Bash/Python
    Steps:
      1. python3 -c "import json, jsonschema; jsonschema.Draft7Validator.check_schema(json.load(open('ports.schema.json')))"
    Expected: exit code 0, no stdout
    Evidence: CI log contains no schema errors

- [ ] 2. Create ports.json (example content provided)

  What to do: Create ports.json in repo root with entries for 'frontend' (5173) and 'backend' (8000) matching schema.
  Must NOT do: Commit any sensitive values or generated .env.local files.

  Parallelization: Wave 1.

  Acceptance Criteria:
  - python3 -m scripts.ports_validate --file ./ports.json prints OK: no port conflicts found and exit 0 (after validator implemented)

  QA Scenarios:
  Scenario: ports.json validation (after validator exists)
    Tool: python3
    Steps:
      1. python3 -m scripts.ports_validate --file ./ports.json
    Expected: stdout EXACT: OK: no port conflicts found\n
- [ ] 3. Add PORTS.md (human-readable) at repo root with table and process (content in References)

  What to do: Add a clear editable table and instructions explaining how to add/update entries, PR process, and how to use scripts/ports_generate_env.py.

  Acceptance Criteria:
  - File exists at ./PORTS.md
  - README references PORTS.md (add a link in README.md if not existing)

- [ ] 4. Add failing unit tests (TDD) for validator and generator (tests/ports/test_validator.py, tests/ports/test_generator.py)

  What to do: Create tests that assert duplicate detection, invalid-port detection, successful validation, generator deterministic output, and fallback logic when primary port is in use.

  Acceptance Criteria:
  - Running pytest initially shows failing tests (TDD red), then after implementation they pass.

- [ ] 5. Implement scripts/ports_validate.py

  What to do: Implement CLI with signature:
    python3 -m scripts.ports_validate --file ./ports.json [--scan-repo]

  Implementation details (decision-complete):
  - Use standard library argparse for CLI.
  - Use jsonschema.validate with ports.schema.json (Draft7 minimal) to validate schema.
  - Check duplicates: build map of assigned ports and test for duplicates across active services.
  - Repo scan: when --scan-repo, search for port literals in files matching patterns: package.json, **/vite.config*.js, docker-compose*.yml, .env*, src/**, using Python's glob + regex r"(?i)(?:--port\s+|VITE_PORT=|PORT=|port:\s*)?(\b[0-9]{2,5}\b)" with context.
  - If any error: print machine-parsable lines starting with ERROR: and exit code 2.
  - On success: print: OK: no port conflicts found and exit 0.

  Must NOT do: attempt to kill processes or create files.

  Acceptance Criteria (executable):
  - python3 -m scripts.ports_validate --file ./ports.json exits 0 and prints OK: no port conflicts found

  QA Scenarios (unit tests):
  - Duplicate detection test: create temp ports.json with duplicates; run validator module function; assert raises SystemExit with code 2 and error message contains "port X conflict".

- [ ] 6. Implement scripts/ports_generate_env.py

  What to do: Implement CLI with signature:
    python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local [--allow-fallback] [--ephemeral-range 30000-31999]

  Decision-complete implementation details:
  - Read ports.json. Lookup service by id OR by path (path exact match). If not found: exit code 3 and print ERROR: service not found.
  - Determine primary port from service['port'].
  - Check availability of port using cross-platform socket.bind(('0.0.0.0', port)) inside a try/except and close immediately when successful to detect availability.
  - If primary free: choose it. If in-use: iterate service['fallbacks'] (if present) in order and use first free fallback.
  - If none free and --allow-fallback not provided: exit with code 4 and message ERROR: no available ports for service X.
  - If none free and --allow-fallback provided: pick ephemeral free port in provided range (default 30000-31999) by binding to 0 and checking range; pick first free and use.
  - Write output file EXACT content:
    # GENERATED FROM ports.json - DO NOT COMMIT
    {env_var}={port}\n
  - Ensure file is created with 0o600 permissions where possible.

  Acceptance Criteria:
  - Running generator for frontend when primary free creates file with exact content above.
  - When primary is in use and fallback free, generator picks fallback and prints INFO message to stdout.

  QA Scenarios (functional tests):
  - Start temporary socket server to occupy port 5173 (in test), run generator, expect .env.local with VITE_PORT=5174 (given fallback list).

- [ ] 7. Add CI job snippet to .github/workflows/ci.yml

  What to do: Add job 'ports-validator' that runs on PRs touching ports.json, PORTS.md, package.json, docker-compose.yml, vite config files.

  Exact job YAML to add (example):
  ```yaml
  ports-validator:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install jsonschema pytest
      - name: Validate ports.json
        run: python3 -m scripts.ports_validate --file ./ports.json
  ```

  Acceptance Criteria:
  - When ports.json contains duplicates, CI job exits non-zero and displays ERROR lines.

- [ ] 8. Docs & CONTRIBUTING update

  What to do: Add a section in CONTRIBUTING.md that explains how to edit ports.json, run validator locally, generate .env.local and the expectation to add owner/team contact.

  Acceptance Criteria: CONTRIBUTING.md contains "Ports" section and references scripts and CI job name.

## Final Verification Wave (MANDATORY)
- [ ] F1. Plan Compliance Audit — Oracle/Momis: ensure plan tasks map to repository conventions and no missing references.
- [ ] F2. Code Quality Review — run linters on scripts and tests.
- [ ] F3. Real Manual QA — run generator and validator on a clean checkout and simulated in-use ports.
- [ ] F4. Scope Fidelity Check — ensure production port scopes were not accidentally included.

## Commit Strategy (exact messages)
1. chore(ports): add PORTS.md, ports.json, ports.schema.json
2. test(ports): add failing validator + generator tests (TDD)
3. feat(ports): implement scripts/ports_validate.py + tests
4. feat(ports): implement scripts/ports_generate_env.py + tests
5. ci(ports): add ports-validator job to CI
6. docs(ports): update CONTRIBUTING.md and README

## Success Criteria
- ports.json validated in CI on every PR touching ports files or port-assigning files
- No committed generated .env.local files in repo
- Developers can run `python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local` to get deterministic local env files

## References (file content you should commit exactly)

### ports.schema.json (commit this exact JSON)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Ports registry schema",
  "type": "object",
  "required": ["schema_version", "services"],
  "properties": {
    "schema_version": {"type": "string"},
    "services": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "path", "port", "env_var", "owner", "status"],
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "path": {"type": "string"},
          "port": {"type": "integer", "minimum": 1, "maximum": 65535},
          "fallbacks": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 65535}},
          "env_var": {"type": "string"},
          "protocol": {"type": "string"},
          "host": {"type": "string"},
          "owner": {"type": "object", "required": ["team"], "properties": {"team": {"type": "string"}, "contact": {"type": "string"}}},
          "status": {"type": "string", "enum": ["active", "reserved", "retired"]},
          "assigned_at": {"type": "string", "format": "date-time"},
          "notes": {"type": "string"}
        }
      }
    }
  }
}
```

### ports.json (example commit content)
```json
{
  "schema_version": "1.0",
  "services": [
    {
      "id": "frontend",
      "name": "Frontend (Vite)",
      "path": "frontend",
      "port": 5173,
      "fallbacks": [5174, 5175],
      "env_var": "VITE_PORT",
      "owner": {"team": "frontend", "contact": "frontend@example.com"},
      "status": "active",
      "notes": "Vite default dev port"
    },
    {
      "id": "backend",
      "name": "Backend (FastAPI)",
      "path": ".",
      "port": 8000,
      "env_var": "BACKEND_PORT",
      "owner": {"team": "backend", "contact": "backend@example.com"},
      "status": "active",
      "notes": "FastAPI dev server"
    }
  ]
}
```

### PORTS.md (exact content to commit)
```markdown
# PORTS — Development Port Registry

This repository uses a single source-of-truth for development port assignments.

Files:
- ports.json — machine-readable registry (required for CI)
- ports.schema.json — schema for ports.json
- PORTS.md — this human-readable reference (this file)

Registry format:
- id: short identifier used by scripts
- name: human name
- path: repo-relative path to the project
- port: primary assigned port
- fallbacks: ordered list of fallback ports
- env_var: environment variable used by the project
- owner: team + contact
- status: active | reserved | retired

Editing process:
1. Update ports.json and add explanation in PR description.
2. Ensure CI (ports-validator job) passes locally by running:
   python3 -m scripts.ports_validate --file ./ports.json
3. Add CODEOWNERS approval from the owning team if ownership changes.

Local usage:
- Generate a local .env file for a project:
  python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local

Do NOT commit generated .env.local files. They are ignored by .gitignore. The generated file will include a header: "# GENERATED FROM ports.json - DO NOT COMMIT"

Contact: repo maintainers or team owners listed in ports.json
```

## Open Questions & Decisions Recorded
- Scope: dev-only (assumption). If you want to cover Docker/CI/prod ports, reply and we will extend schema.
- Enforcement: CI blocks conflicting PRs (assumption). To relax to warnings, change validator exit codes and CI behavior.
- Ownership: team-level placeholders were used — replace with real team handles before merge.

## What I will do next after you approve this plan
1. Produce the three source files (ports.schema.json, ports.json example, PORTS.md) as committed content (I will create a plan/draft for reviewers). (I will not modify other files unless you instruct.).
2. Prepare failing unit tests for TDD and place them in tests/ports/.
3. Optionally run Momus high-accuracy review if you request before implementation.

---

Plan saved to: .sisyphus/plans/ports-management.md
