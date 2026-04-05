# PR Description: Add Port Management System (PORTS.md + Tooling)

## Summary

This PR adds a comprehensive port management system to avoid port conflicts across multiple projects on the same host. It provides:

- **PORTS.md**: Human-readable port registry documentation
- **ports.json**: Machine-readable port registry with schema validation
- **ports.schema.json**: JSON Schema for validation
- **scripts/ports_validate.py**: CLI validator to check for conflicts
- **scripts/ports_generate_env.py**: CLI generator to create local .env files with fallback support
- **Unit tests**: TDD-style tests for validator and generator

## Changes

### New Files
- `PORTS.md` - Human-readable port registry documentation
- `ports.json` - Machine-readable port registry (frontend: 5173, backend: 8000)
- `ports.schema.json` - JSON Schema for ports.json validation
- `scripts/ports_validate.py` - Validator CLI with schema validation, duplicate detection, and optional repo scanning
- `scripts/ports_generate_env.py` - Generator CLI with primary, fallback, and ephemeral port support
- `tests/ports/test_validator.py` - Unit tests for validator (13 tests)
- `tests/ports/test_generator.py` - Unit tests for generator (12 tests)
- `.sisyphus/plans/ports-management.md` - Operational plan document

## Testing

### Unit Tests
```bash
python3 -m pytest tests/ports/ -v
```

All 25 tests pass (13 for validator, 12 for generator).

### Validator Usage
```bash
# Validate ports.json against schema
python3 -m scripts.ports_validate --file ./ports.json

# Validate and scan repo for port conflicts
python3 -m scripts.ports_validate --file ./ports.json --scan-repo
```

### Generator Usage
```bash
# Generate .env.local for frontend (uses primary port 5173)
python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local

# Generate with fallback support (if 5173 in use, tries 5174, 5175)
python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local --allow-fallback
```

## Behavior

### Conflict Detection
- Schema validation ensures required fields and valid data types
- Port range validation (1-65535)
- Duplicate detection across active and reserved services
- Retired services are excluded from duplicate checks

### Port Assignment
- Primary port: Assigned port in ports.json
- Fallbacks: Ordered list of alternative ports
- Ephemeral: Auto-selected from configured range (default 30000-31999) when all else unavailable

### Generated Files
- Generated .env.local files include header: `# GENERATED FROM ports.json - DO NOT COMMIT`
- Files are created with restrictive permissions (0o600 on Unix)
- Should be gitignored (not committed)

## Review Checklist

- [ ] ports.json schema is valid
- [ ] ports.json contains correct entries for frontend (5173) and backend (8000)
- [ ] PORTS.md accurately reflects ports.json content
- [ ] Unit tests pass: `python3 -m pytest tests/ports/ -v`
- [ ] Validator works: `python3 -m scripts.ports_validate --file ./ports.json`
- [ ] Generator works: `python3 scripts/ports_generate_env.py --id frontend --out /tmp/.env.local`
- [ ] Owner team contacts are updated from placeholders (frontend@example.com, backend@example.com)
- [ ] CI workflow includes validator step (to be added in follow-up PR or separate change)

## Breaking Changes

None. This is a new feature that does not affect existing functionality.

## Documentation

See:
- `PORTS.md` for port registry and usage instructions
- `.sisyphus/plans/ports-management.md` for detailed operational plan

## Notes

- Placeholders for owner emails should be updated before merge
- CI integration step will be added in a follow-up PR
- Currently covers development ports only (production ports out of scope)
