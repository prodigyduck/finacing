#!/usr/bin/env python3
"""
Process Manager

Check for and kill existing processes on specified ports.
"""

import os
import psutil
import logging
import signal

logger = logging.getLogger(__name__)


def find_processes_on_port(port: int):
    """
    Find processes using the specified port.

    Args:
        port: Port number to check

    Returns:
        List of processes using the port
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr and conn.laddr.port == port:
                    processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes


def kill_processes_on_port(port: int, force: bool = False):
    """
    Kill processes using the specified port.

    Args:
        port: Port number to check
        force: Force kill without confirmation
    """
    processes = find_processes_on_port(port)

    if not processes:
        logger.info(f"No processes found on port {port}")
        return

    if not force:
        print(f"\nFound {len(processes)} process(es) using port {port}:")
        for proc in processes:
            print(f"  - PID: {proc.pid}, Name: {proc.name()}")

        response = input("\nKill these processes? (y/N): ").strip().lower()
        if response != 'y':
            logger.info("Cancelled by user")
            return

    for proc in processes:
        try:
            proc.terminate()
            logger.info(f"Terminated process: PID {proc.pid}, Name: {proc.name()}")
        except psutil.NoSuchProcess:
            logger.warning(f"Process {proc.pid} no longer exists")
        except psutil.AccessDenied:
            logger.error(f"Access denied to process {proc.pid}")


def check_and_cleanup_ports(ports: list[int]):
    """
    Check multiple ports and clean up processes.

    Args:
        ports: List of ports to check
    """
    for port in ports:
        processes = find_processes_on_port(port)
        if processes:
            logger.warning(f"Port {port} is in use by {len(processes)} process(es)")
            kill_processes_on_port(port, force=True)
        else:
            logger.info(f"Port {port} is available")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process Manager for Financing")
    parser.add_argument(
        "--check-port",
        type=int,
        help="Check specific port for processes"
    )
    parser.add_argument(
        "--kill-port",
        type=int,
        help="Kill processes on specific port"
    )
    parser.add_argument(
        "--cleanup-ports",
        nargs='+',
        type=int,
        help="Kill processes on specified ports",
        default=[5173, 8000]  # Default ports for frontend and backend
    )

    args = parser.parse_args()

    if args.kill_port:
        kill_processes_on_port(args.kill_port)

    elif args.check_port:
        processes = find_processes_on_port(args.check_port)
        if processes:
            print(f"\nProcesses on port {args.check_port}:")
            for proc in processes:
                print(f"  PID: {proc.pid}, Name: {proc.name()}")
        else:
            print(f"No processes found on port {args.check_port}")

    elif args.cleanup_ports:
        check_and_cleanup_ports(args.cleanup_ports)

    else:
        print("No action specified. Use --help for usage.")
