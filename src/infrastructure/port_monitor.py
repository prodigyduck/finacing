"""
Port Monitor Service

Real-time port status monitoring and conflict detection.
"""

import psutil
import socket
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PortInfo:
    """Port status information"""

    def __init__(
        self,
        port: int,
        in_use: bool,
        process_name: Optional[str] = None,
        process_id: Optional[int] = None,
        last_checked: datetime = None,
    ):
        self.port = port
        self.in_use = in_use
        self.process_name = process_name
        self.process_id = process_id
        self.last_checked = last_checked

    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            "port": self.port,
            "in_use": self.in_use,
            "process_name": self.process_name,
            "process_id": self.process_id,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None,
        }


class PortMonitorService:
    """Monitor port usage across system"""

    # Common development ports
    MONITORED_PORTS = [5173, 5174, 5175, 8000, 8001, 3000, 3001]

    def __init__(self):
        self._port_cache: Dict[int, PortInfo] = {}

    def scan_port(self, port: int) -> PortInfo:
        """
        Scan a specific port and get detailed information.

        Args:
            port: Port number to scan

        Returns:
            PortInfo with port status
        """
        # Check if port is in use
        in_use = False
        process_name = None
        process_id = None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))

            if result == 0:
                # Connection successful - port is in use by another process
                in_use = True

                # Try to identify the process using this port
                process_name = self._find_process_using_port(port)
                if process_name:
                    process_id = self._get_process_id(process_name)

        except OSError:
            # Port not in use
            in_use = False

        port_info = PortInfo(
            port=port,
            in_use=in_use,
            process_name=process_name,
            process_id=process_id,
            last_checked=datetime.now()
        )

        # Update cache
        self._port_cache[port] = port_info

        return port_info

    def _find_process_using_port(self, port: int) -> Optional[str]:
        """
        Find process name that's using the port.

        Args:
            port: Port number

        Returns:
            Process name if found, None otherwise
        """
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port:
                try:
                    process = psutil.Process(conn.pid)
                    return process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        return None

    def _get_process_id(self, process_name: str) -> Optional[int]:
        """
        Get process ID from process name.

        Args:
            process_name: Process name

        Returns:
            Process ID if found, None otherwise
        """
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name() == process_name:
                return proc.pid
        return None

    def scan_all_ports(self) -> List[PortInfo]:
        """
        Scan all monitored ports.

        Returns:
            List of PortInfo for all monitored ports
        """
        port_infos = []

        for port in self.MONITORED_PORTS:
            port_info = self.scan_port(port)
            port_infos.append(port_info)

        return port_infos

    def kill_process_on_port(self, port: int) -> bool:
        """
        Kill process using specified port.

        Args:
            port: Port number

        Returns:
            True if process was killed, False otherwise
        """
        port_info = self._port_cache.get(port)

        if not port_info or not port_info.in_use:
            logger.warning(f"Port {port} is not in use, nothing to kill")
            return False

        if port_info.process_id:
            try:
                process = psutil.Process(port_info.process_id)
                process.terminate()
                logger.info(f"Killed process: PID {port_info.process_id}, Name: {port_info.process_name}")

                # Update cache
                self.scan_port(port)
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.error(f"Failed to kill process {port_info.process_id}: {e}")
                return False

        return False

    def get_port_summary(self) -> Dict:
        """
        Get summary of all monitored ports.

        Returns:
            Dictionary with port usage statistics
        """
        port_infos = self.scan_all_ports()

        total_ports = len(port_infos)
        in_use_count = sum(1 for p in port_infos if p.in_use)
        available_count = total_ports - in_use_count

        return {
            "total_ports": total_ports,
            "in_use_count": in_use_count,
            "available_count": available_count,
            "ports": [p.to_dict() for p in port_infos],
            "last_updated": datetime.now().isoformat(),
        }


port_monitor = PortMonitorService()
