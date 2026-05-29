import logging
from enum import Enum
from math import nan
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
from .pulsar_actuator_real import PulsarActuatorReal, PulsarActuatorScannerReal

class PulsarActuator(PulsarActuatorReal):
    """Deprecated compatibility name for PulsarActuatorReal."""

    def __init__(self, adapter_handler, address: int, logger = None): ...

class PulsarActuatorScanner(PulsarActuatorScannerReal):
    """Deprecated compatibility name for PulsarActuatorScannerReal."""

    def __init__(self, adapter_handler, logger = None): ...

__all__ = ['PulsarActuator', 'PulsarActuatorScanner']
