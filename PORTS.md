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
