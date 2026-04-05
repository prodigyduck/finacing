#!/usr/bin/env python3
"""
Ports validator - validates ports.json against schema and checks for conflicts.

Usage:
    python3 -m scripts.ports_validate --file ./ports.json [--scan-repo]
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema file."""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: schema file not found: {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in schema file: {e}")
        sys.exit(1)


def load_ports(ports_path: Path) -> dict:
    """Load ports.json file."""
    try:
        with open(ports_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: ports file not found: {ports_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in ports file: {e}")
        sys.exit(1)


def validate_schema(data: dict, schema: dict) -> List[str]:
    """Validate ports.json against schema using simple validation."""
    errors = []

    # Check required top-level keys
    if 'schema_version' not in data:
        errors.append("ERROR: missing required field: schema_version")
    if 'services' not in data:
        errors.append("ERROR: missing required field: services")

    # Validate services
    if 'services' in data:
        services = data['services']
        if not isinstance(services, list):
            errors.append("ERROR: services must be an array")
        else:
            for idx, service in enumerate(services):
                if not isinstance(service, dict):
                    errors.append(f"ERROR: service at index {idx} must be an object")
                    continue

                # Required fields
                required_fields = ['id', 'name', 'path', 'port', 'env_var', 'owner', 'status']
                for field in required_fields:
                    if field not in service:
                        errors.append(f"ERROR: service at index {idx} missing required field: {field}")

                # Port range
                if 'port' in service:
                    port = service['port']
                    if not isinstance(port, int) or port < 1 or port > 65535:
                        errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} invalid port: {port} (must be 1-65535)")

                # Fallbacks
                if 'fallbacks' in service:
                    fallbacks = service['fallbacks']
                    if not isinstance(fallbacks, list):
                        errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} fallbacks must be an array")
                    else:
                        for f_idx, fallback in enumerate(fallbacks):
                            if not isinstance(fallback, int) or fallback < 1 or fallback > 65535:
                                errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} invalid fallback at index {f_idx}: {fallback}")

                # Status enum
                if 'status' in service:
                    status = service['status']
                    if status not in ['active', 'reserved', 'retired']:
                        errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} invalid status: {status} (must be active, reserved, or retired)")

                # Owner
                if 'owner' in service:
                    owner = service['owner']
                    if not isinstance(owner, dict):
                        errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} owner must be an object")
                    else:
                        if 'team' not in owner:
                            errors.append(f"ERROR: service {service.get('id', f'index-{idx}')} owner missing required field: team")

    return errors


def check_duplicates(data: dict) -> List[str]:
    """Check for duplicate ports across active services."""
    errors = []
    port_map: Dict[int, List[str]] = {}

    if 'services' not in data:
        return errors

    for service in data['services']:
        if service.get('status') == 'retired':
            continue

        service_id = service.get('id', 'unknown')
        port = service.get('port')

        if port is not None:
            if port not in port_map:
                port_map[port] = []
            port_map[port].append(service_id)

        # Check fallbacks too
        for fallback in service.get('fallbacks', []):
            if fallback not in port_map:
                port_map[fallback] = []
            port_map[fallback].append(f"{service_id} (fallback)")

    # Report duplicates
    for port, services in port_map.items():
        if len(services) > 1:
            errors.append(f"ERROR: port {port} conflict: {' vs '.join(services)}")

    return errors


def scan_repo_for_ports(repo_root: Path, data: dict) -> List[str]:
    """Scan repository for hardcoded ports and report mismatches."""
    errors = []

    if 'services' not in data:
        return errors

    # Build map of expected ports by path
    expected_ports: Dict[str, Tuple[int, str]] = {}
    for service in data['services']:
        service_path = service.get('path')
        port = service.get('port')
        env_var = service.get('env_var')
        if service_path and port is not None:
            expected_ports[service_path] = (port, env_var)

    # Files to scan
    files_to_scan = []
    for pattern in ['package.json', '**/vite.config*.js', '**/vite.config*.ts', 'docker-compose*.yml', '.env*']:
        files_to_scan.extend(repo_root.rglob(pattern))

    # Port patterns
    port_patterns = [
        r'--port\s+(\d+)',
        r'VITE_PORT=(\d+)',
        r'PORT=(\d+)',
        r'port:\s*(\d+)',
        r'"port":\s*(\d+)',
    ]

    combined_pattern = re.compile('|'.join(port_patterns), re.IGNORECASE)

    for file_path in files_to_scan:
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            matches = combined_pattern.finditer(content)
            for match in matches:
                found_port = int(match.group(1))

                # Find which service this file belongs to
                relative_path = str(file_path.relative_to(repo_root))
                service_path = None
                for sp in expected_ports:
                    if relative_path.startswith(sp):
                        service_path = sp
                        break

                if service_path:
                    expected_port, env_var = expected_ports[service_path]
                    if found_port != expected_port:
                        errors.append(
                            f"ERROR: {relative_path} declares port {found_port} but registry lists {expected_port} for service path {service_path}"
                        )
        except Exception:
            # Skip files that can't be read (e.g., binary files)
            pass

    return errors


def main():
    parser = argparse.ArgumentParser(description='Validate ports.json')
    parser.add_argument('--file', type=str, default='./ports.json', help='Path to ports.json')
    parser.add_argument('--scan-repo', action='store_true', help='Scan repository for port conflicts')
    args = parser.parse_args()

    # Determine paths
    repo_root = Path(__file__).parent.parent
    ports_path = Path(args.file)
    if not ports_path.exists():
        ports_path = repo_root / args.file
    schema_path = repo_root / 'ports.schema.json'

    if not ports_path.exists():
        ports_path = repo_root / args.file

    # Load files
    schema = load_schema(schema_path)
    ports = load_ports(ports_path)

    # Validate
    all_errors = []

    # Schema validation
    schema_errors = validate_schema(ports, schema)
    all_errors.extend(schema_errors)

    # Duplicate check
    dup_errors = check_duplicates(ports)
    all_errors.extend(dup_errors)

    # Repo scan
    if args.scan_repo:
        scan_errors = scan_repo_for_ports(repo_root, ports)
        all_errors.extend(scan_errors)

    # Report results
    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(2)
    else:
        print("OK: no port conflicts found")
        sys.exit(0)


if __name__ == '__main__':
    main()
