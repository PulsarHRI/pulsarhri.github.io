import logging
from enum import Enum
from math import nan
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

MAX_FEEDBACK_RATE_ALLOWED_HZ: Any

class PulsarActuatorReal:
    MODELS_NAMES: Any

    class Mode(Enum):
        """Control modes available for Pulsar actuator implementations."""
        FVI = 0x02  # Field voltage injection test mode
        OPEN_LOOP = 0x03  # Open-loop test mode
        DVI = 0x04  # Field oriented voltage injection test mode
        TORQUE = 0x05
        SPEED = 0x06
        POSITION = 0x07
        IMPEDANCE = 0x08

    class Rates(Enum):
        """Feedback update rates for high/low frequency data streams."""
        DISABLED = 0  # Feedback disabled
        RATE_2KHZ = 10  # 2 kHz update rate
        RATE_1KHZ = 20  # 1 kHz update rate
        RATE_500HZ = 40  # 500 Hz update rate
        RATE_200HZ = 100  # 200 Hz update rate
        RATE_100HZ = 200  # 100 Hz update rate
        RATE_50HZ = 400  # 50 Hz update rate
        RATE_20HZ = 1_000  # 20 Hz update rate
        RATE_10HZ = 2_000  # 10 Hz update rate
        RATE_5HZ = 4_000  # 5 Hz update rate
        RATE_2HZ = 10_000  # 2 Hz update rate
        RATE_1HZ = 20_000  # 1 Hz update rate

    class TorquePerformance(Enum):
        """Performance presets for torque control mode."""
        AGGRESSIVE = 1  # Fast, responsive torque control
        BALANCED = 2  # Balanced torque control
        SOFT = 3  # Smooth, gentle torque control

    class SpeedPerformance(Enum):
        """Performance presets for speed control mode."""
        AGGRESSIVE = 1  # Fast, responsive speed control
        BALANCED = 2  # Balanced speed control
        SOFT = 3  # Smooth, gentle speed control
        CUSTOM = 4  # Custom speed control parameters

    class PCP_Parameters(Enum):
        """Parameters that can be read or written through the actuator API."""
        K_DAMPING = 0x01  # Damping coefficient (Nm*s/rad) for impedance control
        K_STIFFNESS = 0x02  # Stiffness coefficient (Nm/rad) for impedance control
        TORQUE_FF = 0x03  # Feed-forward torque value (Nm)
        LIM_TORQUE = 0x04  # Symmetric torque limit in positive/negative directions (Nm)
        LIM_POSITION_MAX = 0x05  # Maximum position limit (rad)
        LIM_POSITION_MIN = 0x06  # Minimum position limit (rad)
        LIM_SPEED_MAX = 0x07  # Maximum speed limit (rad/s)
        LIM_SPEED_MIN = 0x08  # Minimum speed limit (rad/s)
        PROFILE_POSITION_MAX = 0x09  # Maximum positive speed in position-control profile (rad/s)
        PROFILE_POSITION_MIN = 0x0A  # Maximum negative speed in position-control profile (rad/s)
        PROFILE_SPEED_MAX = 0x0B  # Maximum acceleration in speed-control profile (rad/s^2)
        PROFILE_SPEED_MIN = 0x0C  # Maximum deceleration in speed-control profile (rad/s^2)
        KP_SPEED = 0x0D  # Speed-loop proportional gain
        KI_SPEED = 0x0E  # Speed-loop integral gain
        KP_POSITION = 0x0F  # Position-loop proportional gain
        MODE = 0x30  # Operation mode; read-only, set with CHANGE_MODE
        SETPOINT = 0x31  # Current setpoint: position (rad), speed (rad/s), or torque (Nm)
        TORQUE_PERFORMANCE = 0x40  # Torque performance preset
        SPEED_PERFORMANCE = 0x41  # Speed performance preset
        PROFILE_SPEED_MAX_RAD_S = 0x42  # Maximum profile speed (rad/s)
        PROFILE_TORQUE_MAX_NM = 0x43  # Maximum profile torque (Nm)
        INVERT_FLAG = 0x44  # Invert direction of motion (boolean flag, 0 or 1)
        FF_GAIN = 0x45  # Feed-forward gain for friction/inertia compensation
        PCP_PARAM_SPEED_CUTOFF = 0x46  # Speed IIR filter cutoff frequency
        PCP_PARAM_CURRENT_CUTOFF = 0x47  # DQ-current IIR filter cutoff frequency
        FIRMWARE_VERSION = 0x80  # Real actuator firmware version (read-only)
        PCP_ADDRESS = 0x81  # Device PCP address
        SERIAL_NUMBER = 0x82  # Device serial number (read-only)
        DEVICE_MODEL = 0x83  # Device model identifier (read-only)
        CONTROL_VERSION = 0x84  # Control software version (read-only)
        CAN_HIGH_SPEED = 0x85  # CAN high-speed mode enabled/disabled

    class PCP_Items(Enum):
        """Feedback items available for monitoring actuator state."""
        ENCODER_INT = 0x41  # Internal encoder position
        ENCODER_INT_RAW = 0x42  # Raw internal encoder counts
        ENCODER_EXT = 0x43  # External encoder position
        ENCODER_EXT_RAW = 0x44  # Raw external encoder counts
        SPEED_FB = 0x45  # Speed feedback
        IA = 0x46  # Phase A current
        IB = 0x47  # Phase B current
        IC = 0x48  # Phase C current
        TORQUE_SENS = 0x49  # Torque sensor reading
        TORQUE_SENS_RAW = 0x4A  # Raw torque sensor reading
        POSITION_REF = 0x4B  # Position reference/command
        POSITION_FB = 0x4C  # Position feedback
        POSITION_FB_INTERNAL = 0x73  # Position feedback from internal encoder
        SPEED_REF = 0x4D  # Speed reference/command
        ID_REF = 0x4F  # D-axis current reference
        ID_FB = 0x50  # D-axis current feedback
        IQ_REF = 0x51  # Q-axis current reference
        IQ_FB = 0x52  # Q-axis current feedback
        VD_REF = 0x53  # D-axis voltage reference
        VQ_REF = 0x54  # Q-axis voltage reference
        TORQUE_REF = 0x55  # Torque reference/command
        TORQUE_FB = 0x56  # Torque feedback
        REFERENCE_A_VOLTAGE = 0x57  # Reference phase A voltage
        REFERENCE_B_VOLTAGE = 0x58  # Reference phase B voltage
        REFERENCE_C_VOLTAGE = 0x59  # Reference phase C voltage
        BUS_POWER = 0x5A  # DC bus power
        BUS_CURRENT = 0x5B  # DC bus current
        THREE_PHASE_POWER = 0x5C  # Three-phase electrical power
        MECHANICAL_POWER = 0x5D  # Mechanical output power
        INVERTER_EFFICIENCY = 0x5E  # Inverter efficiency
        MOTOR_EFFICIENCY = 0x5F  # Motor efficiency
        ERRORS_ENCODER_INT = 0x60  # Internal encoder error flags
        ERRORS_ENCODER_EXT = 0x61  # External encoder error flags
        ERRORS_OVERRUN = 0x62  # Control-loop overrun error flags
        VBUS = 0x70  # DC bus voltage
        TEMP_PCB = 0x71  # PCB temperature
        TEMP_MOTOR = 0x72  # Motor temperature
        DEBUG_SIGNAL_BOOL = 0x90  # Debug boolean signal
        DEBUG_SIGNAL01 = 0x91  # Debug signal 1
        DEBUG_SIGNAL02 = 0x92  # Debug signal 2
        DEBUG_SIGNAL03 = 0x93  # Debug signal 3
        DEBUG_SIGNAL04 = 0x94  # Debug signal 4
        DEBUG_SIGNAL05 = 0x95  # Debug signal 5
        DEBUG_SIGNAL06 = 0x96  # Debug signal 6
        DEBUG_SIGNAL07 = 0x97  # Debug signal 7
        DEBUG_SIGNAL08 = 0x98  # Debug signal 8
        DEBUG_SIGNAL09 = 0x99  # Debug signal 9
        DEBUG_SIGNAL10 = 0x9A  # Debug signal 10

    def __init__(self, adapter_handler: Any, address: int, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize a real actuator bound to a PCP adapter and address.

        Args:
            adapter_handler: Transport adapter used to send and receive PCP messages.
            address: PCP actuator address.
            logger: Optional logger used for diagnostics.
        """
        ...

    @property
    def connected(self) -> bool:
        """Return whether the actuator is connected."""
        ...

    @property
    def implementation_version(self) -> str:
        """Return the physical actuator firmware version."""
        ...

    def set_feedback_callback(self, callback: Callable[[int, dict], None]) -> None:
        """
        Set the callback invoked when feedback data is received.

        Args:
            callback: Callable receiving the actuator address and feedback data.
        """
        ...

    def set_error_callback(self, callback: Callable[[int, dict], None]) -> None:
        """
        Set the callback invoked when actuator errors are received.

        Args:
            callback: Callable receiving the actuator address and error data.
        """
        ...

    def set_low_freq_feedback_callback(self, callback: Callable[[Any], None]) -> None:
        """Deprecated compatibility shim for the removed low-frequency callback."""
        ...

    def get_feedback(self) -> Dict[Any, Any]:
        """
        Return the latest feedback values.

        Returns:
            The current feedback dictionary.
        """
        ...

    @staticmethod
    def is_valid_actuator_address(address: int) -> bool:
        """Return whether ``address`` is a valid actuator network address."""
        ...

    def stop(self) -> None:
        """Disable actuator control."""
        ...

    def connect(self, timeout: float = 1.0) -> bool:
        """
        Connect to the actuator by sending a ping request.

        Args:
            timeout: Maximum time to wait for a pong response, in seconds.

        Returns:
            ``True`` when the actuator responds before the timeout expires.
        """
        ...

    def disconnect(self) -> None:
        """Stop the actuator, unregister its callback, and mark it disconnected."""
        ...

    def send_ping(self, timeout: float = 1.0) -> bool:
        """
        Send a ping message and wait for a pong response.

        Args:
            timeout: Maximum time to wait for a pong response, in seconds.

        Returns:
            ``True`` if a pong response is received before the timeout expires.
        """
        ...

    def change_address(self, new_address: int) -> None:
        """
        Write a new PCP address to the actuator.

        Args:
            new_address: New actuator address in the valid actuator range.
        """
        ...

    def start(self) -> None:
        """Enable actuator control."""
        ...

    def change_mode(self, mode: 'PulsarActuatorReal.Mode') -> None:
        """
        Change the actuator control mode.

        Args:
            mode: Control mode to activate.
        """
        ...

    def get_mode(self) -> 'PulsarActuatorReal.Mode':
        """
        Return the current actuator control mode.

        Returns:
            The cached control mode, or a mode read from the actuator.
        """
        ...

    def change_setpoint(self, setpoint: float) -> None:
        """
        Change the setpoint for the current control mode.

        Args:
            setpoint: Setpoint value for the active mode.
        """
        ...

    def change_torque_setpoint(self, setpoint: float, id_Kp: float = nan, id_Ki: float = nan, iq_Kp: float = nan, iq_Ki: float = nan) -> None:
        """
        Switch to torque mode and send a torque setpoint.

        Args:
            setpoint: Torque reference, in Nm.
            id_Kp: Optional d-axis current proportional gain.
            id_Ki: Optional d-axis current integral gain.
            iq_Kp: Optional q-axis current proportional gain.
            iq_Ki: Optional q-axis current integral gain.
        """
        ...

    def change_speed_setpoint(self, setpoint: float, FF_gain: float = nan, spd_Ki: float = nan, spd_Kp: float = nan, ref_ff_torque: float = nan) -> None:
        """
        Switch to speed mode and send a speed setpoint.

        Args:
            setpoint: Speed reference, in rad/s.
            FF_gain: Optional feed-forward gain.
            spd_Ki: Optional speed-loop integral gain.
            spd_Kp: Optional speed-loop proportional gain.
            ref_ff_torque: Optional feed-forward torque reference, in Nm.
        """
        ...

    def change_position_setpoint(self, setpoint: float, FF_gain: float = nan, spd_Ki: float = nan, spd_Kp: float = nan, pos_Kp: float = nan, ref_ff_torque: float = nan) -> None:
        """
        Switch to position mode and send a position setpoint.

        Args:
            setpoint: Position reference, in radians.
            FF_gain: Optional feed-forward gain.
            spd_Ki: Optional speed-loop integral gain.
            spd_Kp: Optional speed-loop proportional gain.
            pos_Kp: Optional position-loop proportional gain.
            ref_ff_torque: Optional feed-forward torque reference, in Nm.
        """
        ...

    def change_impedance_setpoint(self, setpoint: float, FF_gain: float = nan, K_stiff: float = nan, K_damp: float = nan, J_imp: float = nan, ref_ff_torque: float = nan, ref_impedance_spd: float = nan, ref_impedance_acel: float = nan) -> None:
        """
        Switch to impedance mode and send an impedance setpoint.

        Args:
            setpoint: Position reference, in radians.
            FF_gain: Optional feed-forward gain.
            K_stiff: Optional impedance stiffness.
            K_damp: Optional impedance damping.
            J_imp: Optional impedance inertia.
            ref_ff_torque: Optional feed-forward torque reference, in Nm.
            ref_impedance_spd: Optional impedance speed reference, in rad/s.
            ref_impedance_acel: Optional impedance acceleration reference.
        """
        ...

    def internal_change_speed_setpoint(self, setpoint: float, spd_b0: float = nan, spd_wc: float = nan, spd_wo: float = nan) -> None:
        """Send an internal speed-controller setpoint packet."""
        ...

    def internal_change_position_setpoint(self, setpoint: float, pos_Ki: float = nan, pos_Kd: float = nan, pos_b0: float = nan, pos_wc: float = nan, pos_wo: float = nan, spd_b0: float = nan, spd_wc: float = nan, spd_wo: float = nan) -> None:
        """Send an internal position-controller setpoint packet."""
        ...

    def set_home_position(self) -> None:
        """Set the current actuator position as the zero reference."""
        ...

    def set_feedback_items(self, items: List['PulsarActuatorReal.PCP_Items']) -> None:
        """
        Configure the high-frequency feedback item stream.

        Args:
            items: Feedback items to include in telemetry packets.
        """
        ...

    def set_feedback_rate(self, rate: Union['PulsarActuatorReal.Rates', int]) -> None:
        """
        Configure the high-frequency feedback rate.

        Args:
            rate: A ``Rates`` divider enum or an integer target rate in Hz. The
                divider is rounded to the nearest integer. Use ``Rates.DISABLED``
                or ``0`` to disable feedback.
        """
        ...

    def get_items_blocking(self, items: List['PulsarActuatorReal.PCP_Items'], timeout: float = 1.0) -> Dict['PulsarActuatorReal.PCP_Items', float]:
        """
        Request specific feedback items and wait for their response.

        Args:
            items: Feedback items to request. Requests are capped at the protocol
                batch limit.
            timeout: Maximum time to wait for a response, in seconds.

        Returns:
            Mapping from requested feedback items to received values. Returns an
            empty mapping on timeout.
        """
        ...

    def set_parameters(self, parameters: Dict['PulsarActuatorReal.PCP_Parameters', float]) -> None:
        """
        Write actuator parameters.

        Args:
            parameters: Mapping from parameter enum to the float value to write.
        """
        ...

    def get_parameters(self, parameters: List['PulsarActuatorReal.PCP_Parameters'], timeout: float = 1.0) -> Dict['PulsarActuatorReal.PCP_Parameters', float]:
        """
        Read actuator parameters.

        Args:
            parameters: Parameters to request. Long requests are split across
                protocol-sized batches.
            timeout: Maximum time to wait for each response, in seconds.

        Returns:
            Mapping from parameter enum to the most recently received value.
        """
        ...

    def get_parameters_all(self) -> Dict['PulsarActuatorReal.PCP_Parameters', float]:
        """
        Read all known actuator parameters.

        Returns:
            Mapping from parameter enum to current value.
        """
        ...

    def set_can_high_speed(self, high_speed: bool) -> None:
        """Enable or disable CAN BRS/high-speed operation for this actuator."""
        ...

    def set_torque_performance(self, performance: 'PulsarActuatorReal.TorquePerformance') -> None:
        """
        Set the actuator torque-control performance preset.

        Args:
            performance: Torque performance preset to apply.
        """
        ...

    def set_speed_performance(self, performance: 'PulsarActuatorReal.SpeedPerformance') -> None:
        """
        Set the actuator speed-control performance preset.

        Args:
            performance: Speed performance preset to apply.
        """
        ...

    def save_config(self) -> None:
        """Persist the current actuator configuration to non-volatile memory."""
        ...

    def restore_factory_parameters(self, settle_time: float = 1.0) -> None:
        """
        Restore user-writable actuator parameters to firmware factory defaults.

        Args:
            settle_time: Seconds to wait after sending the restore command before
                returning. The actuator may briefly stop answering pings while it
                applies the restored configuration.

        This clears the saved configuration values used for parameters such as
        gains, limits, profile settings, CAN speed, and direction inversion. It
        does not erase factory electrical-machine calibration data.
        """
        ...

    def blink(self) -> None:
        """Blink the actuator LED for physical identification."""
        ...

    def enter_bootloader(self) -> None:
        """Request that the actuator enters bootloader mode."""
        ...

    def changeAddress(self, new_address: int) -> None: ...

    def setFeedbackItems(self, items: List['PulsarActuatorReal.PCP_Items']) -> None: ...

    def setFeedbackRate(self, rate: Union['PulsarActuatorReal.Rates', int]) -> None: ...

    def set_high_freq_feedback_items(self, items: List['PulsarActuatorReal.PCP_Items']) -> None: ...

    def setHighFreqFeedbackItems(self, items: List['PulsarActuatorReal.PCP_Items']) -> None: ...

    def set_high_freq_feedback_rate(self, rate: 'PulsarActuatorReal.Rates') -> None: ...

    def setHighFreqFeedbackRate(self, rate: 'PulsarActuatorReal.Rates') -> None: ...

    def set_low_freq_feedback_items(self, items: List['PulsarActuatorReal.PCP_Items']) -> None: ...

    def setLowFreqFeedbackItems(self, items: List['PulsarActuatorReal.PCP_Items']) -> None: ...

    def set_low_freq_feedback_rate(self, rate: 'PulsarActuatorReal.Rates') -> None: ...

    def setLowFreqFeedbackRate(self, rate: 'PulsarActuatorReal.Rates') -> None: ...

    def getItemsBlocking(self, items: List['PulsarActuatorReal.PCP_Items'], timeout: float = 1.0) -> Dict['PulsarActuatorReal.PCP_Items', float]: ...

    def reset_encoder_position(self) -> None: ...

class PulsarActuatorScannerReal(PulsarActuatorReal):
    """Discover real actuators through a connected CAN adapter."""

    def __init__(self, adapter_handler: Any, logger: Optional[logging.Logger] = None) -> None:
        """Initialize a scanner using an adapter-local address."""
        ...

    def scan(self, begin: int = 1, end: int = ...) -> List[int]:
        """
        Scan an address range for responding actuator devices.

        Args:
            begin: First address to probe.
            end: Last address to probe.

        Returns:
            Addresses that responded to ping.
        """
        ...

    @property
    def is_connected(self) -> bool:
        """Return whether the scanner is connected to a valid CAN adapter."""
        ...

__all__ = ['PulsarActuatorReal', 'PulsarActuatorScannerReal']
