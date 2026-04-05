#!/usr/bin/env python3
"""
Ports .env generator - generates .env.local files from ports.json with fallback support.

Usage:
    python3 scripts/ports_generate_env.py --id frontend --out ./frontend/.env.local [--allow-fallback] [--ephemeral-range 30000-31999]
"""

import argparse
import json
import sys
import socket
from pathlib import Path
from typing import Optional, Tuple


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


def find_service(ports: dict, service_id: Optional[str] = None, service_path: Optional[str] = None) -> Optional[dict]:
    """Find service by ID or path."""
    if 'services' not in ports:
        return None

    for service in ports['services']:
        if service_id and service.get('id') == service_id:
            return service
        if service_path and service.get('path') == service_path:
            return service

    return None


def is_port_available(port: int, host: str = '0.0.0.0') -> bool:
    """Check if a port is available for binding."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
    except OSError:
        return False


def find_available_port(
    primary_port: int,
    fallbacks: list[int],
    allow_fallback: bool,
    ephemeral_range: Tuple[int, int],
    host: str = '0.0.0.0'
) -> Tuple[int, str]:
    """Find an available port, using fallbacks or ephemeral range if needed."""
    # Try primary port
    if is_port_available(primary_port, host):
        return primary_port, 'primary'

    if not allow_fallback:
        print(f"ERROR: primary port {primary_port} is in use and --allow-fallback not provided")
        sys.exit(4)

    # Try fallbacks
    for fallback in fallbacks:
        if is_port_available(fallback, host):
            print(f"INFO: primary port {primary_port} in use, using fallback {fallback}")
            return fallback, 'fallback'

    # Try ephemeral range
    ephemeral_start, ephemeral_end = ephemeral_range
    for port in range(ephemeral_start, ephemeral_end + 1):
        if is_port_available(port, host):
            print(f"INFO: primary port {primary_port} and fallbacks in use, using ephemeral port {port}")
            return port, 'ephemeral'

    print(f"ERROR: no available ports found (primary: {primary_port}, fallbacks: {fallbacks}, ephemeral: {ephemeral_start}-{ephemeral_end})")
    sys.exit(4)


def write_env_file(output_path: Path, env_var: str, port: int):
    """Write .env.local file with generated content."""
    try:
        # Create parent directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(output_path, 'w') as f:
            f.write("# GENERATED FROM ports.json - DO NOT COMMIT\n")
            f.write(f"{env_var}={port}\n")

        # Set restrictive permissions on Unix-like systems
        try:
            output_path.chmod(0o600)
        except (OSError, AttributeError):
            pass

        print(f"Wrote {output_path} with {env_var}={port}")
    except OSError as e:
        print(f"ERROR: failed to write {output_path}: {e}")
        sys.exit(1)


def parse_ephemeral_range(range_str: str) -> Tuple[int, int]:
    """Parse ephemeral range string like '30000-31999'."""
    try:
        parts = range_str.split('-')
        if len(parts) != 2:
            raise ValueError()
        start = int(parts[0])
        end = int(parts[1])
        if start < 1024 or end > 65535 or start > end:
            raise ValueError()
        return start, end
    except ValueError:
        print(f"ERROR: invalid ephemeral range '{range_str}', must be like '30000-31999' (ports 1024-65535)")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Generate .env.local files from ports.json')
    parser.add_argument('--id', type=str, help='Service ID to look up')
    parser.add_argument('--path', type=str, help='Service path to look up')
    parser.add_argument('--out', type=str, required=True, help='Output .env.local file path')
    parser.add_argument('--allow-fallback', action='store_true', help='Allow using fallback ports if primary in use')
    parser.add_argument('--ephemeral-range', type=str, default='30000-31999',
                        help='Ephemeral port range (default: 30000-31999)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to check port availability (default: 0.0.0.0)')
    args = parser.parse_args()

    # Validate args
    if not args.id and not args.path:
        print("ERROR: must specify either --id or --path")
        sys.exit(3)

    # Determine paths
    repo_root = Path(__file__).parent.parent
    ports_path = repo_root / 'ports.json'
    output_path = Path(args.out)

    # Load ports
    ports = load_ports(ports_path)

    # Find service
    service = find_service(ports, service_id=args.id, service_path=args.path)
    if not service:
        print(f"ERROR: service not found (id={args.id}, path={args.path})")
        sys.exit(3)

    # Get service details
    primary_port = service.get('port')
    env_var = service.get('env_var')
    fallbacks = service.get('fallbacks', [])

    if primary_port is None:
        print(f"ERROR: service {service.get('id')} missing 'port' field")
        sys.exit(3)

    if not env_var:
        print(f"ERROR: service {service.get('id')} missing 'env_var' field")
        sys.exit(3)

    # Find available port
    ephemeral_range = parse_ephemeral_range(args.ephemeral_range)
    port, source = find_available_port(
        primary_port,
        fallbacks,
        args.allow_fallback,
        ephemeral_range,
        args.host
    )

    # Write output
    write_env_file(output_path, env_var, port)
    print(f"Port source: {source}")


if __name__ == '__main__':
    main()
