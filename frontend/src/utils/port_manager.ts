"""
Port Manager

Port availability check and single instance management for Vue.js development.
"""

import socket
import logging

logger = logging.getLogger(__name__)


class PortManager:
    """Manage port availability and prevent conflicts"""

    def __init__(self):
        self.checked_ports = set()

    def is_port_available(self, port: int) -> bool:
        """
        Check if port is available.

        Args:
            port: Port number to check

        Returns:
            True if port is available, False otherwise
        """
        if port in self.checked_ports:
            return True  # Already checked and available

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                self.checked_ports.add(port)
                return True
            except OSError:
                return False

    def find_available_port(self, start_port: int = 5173, max_attempts: int = 100) -> int:
        """
        Find an available port starting from start_port.

        Args:
            start_port: Port to start checking from
            max_attempts: Maximum ports to check

        Returns:
            First available port found
        """
        for port in range(start_port, start_port + max_attempts):
            if self.is_port_available(port):
                logger.info(f"Port {port} is available")
                return port

        raise RuntimeError(f"No available ports found in range {start_port}-{start_port + max_attempts}")

    def check_existing_process(self, port: int) -> bool:
        """
        Check if there's an existing process running on the port.

        Args:
            port: Port number to check

        Returns:
            True if process exists on port, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                return result == 0  # Connection successful means process exists
        except Exception:
            return False

    def get_recommended_port(self, preferred_port: int = 5173) -> int:
        """
        Get a recommended port, checking for conflicts first.

        Args:
            preferred_port: Preferred port number

        Returns:
            Available port to use
        """
        if self.is_port_available(preferred_port):
            logger.info(f"Preferred port {preferred_port} is available")
            return preferred_port

        existing_process = self.check_existing_process(preferred_port)
        if existing_process:
            logger.warning(f"Existing process found on port {preferred_port}")
            logger.info("Finding alternative port...")
            return self.find_available_port(preferred_port + 1)

        # Port not available but no process running - another app using it
        logger.warning(f"Port {preferred_port} is in use, finding alternative...")
        return self.find_available_port(preferred_port + 1)
