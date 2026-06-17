import logging
from enum import Enum
from math import nan
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

class PcpOverUsb:
    def __init__(self, port: Optional[str] = None, connect_on_init: bool = True, logger: Optional[logging.Logger] = None) -> None: ...

    def close(self) -> None: ...

    def set_callback(self, address: int, callback: Callable) -> None:
        """Register a callback for a transport address."""
        ...

    def setCallback(self, address: int, callback: Callable) -> None: ...

    def remove_callback(self, address: int) -> None:
        """Remove a callback for a specific address"""
        ...

    def removeCallback(self, address: int) -> None: ...

    def connect(self, port: Optional[str] = None) -> bool: ...

    def disconnect(self) -> None: ...

    @property
    def is_connected(self) -> bool: ...

    @staticmethod
    def check_pcp_id_range(can_id: int) -> bool:
        """Check if the address fits the 14-bit PCP address field."""
        ...

    @staticmethod
    def check_pcp_payload_size(payload) -> bool: ...

    def send_PCP(self, address: int, data: list, priority: bool = True, can_high_speed: bool = False) -> bool: ...

    def enter_bootloader(self) -> None:
        """To put the CAN adapter itself into bootloader mode """
        ...

    @staticmethod
    def get_ports() -> list[str]: ...

    @staticmethod
    def get_port() -> str:
        """Autodiscover the serial port for PCP over USB."""
        ...

class PCP_over_USB(PcpOverUsb):
    """Deprecated compatibility name for PcpOverUsb."""

    def __init__(self, port: Optional[str] = None, connect_on_init: bool = True, logger: Optional[logging.Logger] = None) -> None: ...
