import logging
from dataclasses import dataclass
from enum import Enum
from math import nan
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

@dataclass(slots=True)
class VirtualActuatorLog:
    """
    Per-step simulator telemetry log owned by ``PulsarActuatorVirtual``.

    Populated by ``PulsarActuatorVirtual.step()`` after every simulation tick.
    The internal DTwin backend has no knowledge of this structure.
    """
    enable: list[float] = ...
    temp_winding: list[float] = ...
    T_fb: list[float] = ...
    T_ref: list[float] = ...
    id_fb: list[float] = ...
    id_ref: list[float] = ...
    iq_fb: list[float] = ...
    iq_ref: list[float] = ...
    pos_fb: list[float] = ...
    pos_ref: list[float] = ...
    spd_fb: list[float] = ...
    spd_ref: list[float] = ...
    vd_ref: list[float] = ...
    vq_ref: list[float] = ...
    m_Te: list[float] = ...
    m_Tl: list[float] = ...
    m_acc: list[float] = ...
    m_eff_elec: list[float] = ...
    m_eff_mec: list[float] = ...
    m_i_dc: list[float] = ...
    m_ia: list[float] = ...
    m_ib: list[float] = ...
    m_ic: list[float] = ...
    m_id: list[float] = ...
    m_iq: list[float] = ...
    m_pos1: list[float] = ...
    m_pos2: list[float] = ...
    m_pwr_dc: list[float] = ...
    m_pwr_elec: list[float] = ...
    m_pwr_mec: list[float] = ...
    m_spd1: list[float] = ...
    m_spd2: list[float] = ...
    m_va: list[float] = ...
    m_vb: list[float] = ...
    m_vc: list[float] = ...
    m_vd: list[float] = ...
    m_vq: list[float] = ...
    meas_turn: list[int] = ...
    meas_turn2: list[int] = ...
    meas_T: list[float] = ...
    meas_e_pos: list[float] = ...
    meas_pos: list[float] = ...
    meas_pos2: list[float] = ...
    meas_spd: list[float] = ...
    meas_spd2: list[float] = ...
    inp_ref: list[float] = ...
    inp_load: list[float] = ...
    inp_t_adc: list[float] = ...
    inp_ref_ff_torque: list[float] = ...
    inp_ref_impedance_spd: list[float] = ...
    inp_ref_impedance_acel: list[float] = ...
    inp_control_type: list[int] = ...
    inp_enable: list[bool] = ...
    inp_reset_pos: list[bool] = ...
    debug_T_fb_max: list[bool] = ...
    debug_T_ref_max: list[bool] = ...
    debug_i_max: list[bool] = ...
    debug_pos_fb_max: list[bool] = ...
    debug_pos_fb_min: list[bool] = ...
    debug_pos_ref_max: list[bool] = ...
    debug_pos_ref_min: list[bool] = ...
    debug_spd_fb_max: list[bool] = ...
    debug_spd_ref_max: list[bool] = ...
    debug_spd_ref_min: list[bool] = ...
    time: list[float] = ...
    TIME_STEP: float = ...
    time_start: float = ...

class PulsarActuatorVirtual:
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

    def __init__(self, adapter_handler: Any | None = None, address: int | None = None, logger: logging.Logger | None = None) -> None:
        """
        Initialize a virtual actuator.

        Args:
            adapter_handler: Optional preconfigured DTwin actuator wrapper.
            address: Optional virtual PCP address.
            logger: Optional logger used for diagnostics.
        """
        ...

    @property
    def connected(self) -> bool:
        """Return whether the actuator is connected."""
        ...

    @property
    def implementation_version(self) -> str:
        """Return DTwin model/build metadata for the generic version hook."""
        ...

    def set_feedback_callback(self, callback: Callable[[int | None, dict[Any, Any]], None]) -> None:
        """Set the callback invoked when virtual feedback is emitted."""
        ...

    def set_error_callback(self, callback: Callable[[int | None, dict[Any, Any]], None]) -> None:
        """Set the callback invoked when virtual actuator errors are emitted."""
        ...

    def set_low_freq_feedback_callback(self, callback: Callable[[Any], None]) -> None:
        """Deprecated compatibility shim for the removed low-frequency callback."""
        ...

    def get_feedback(self) -> dict['PulsarActuatorVirtual.PCP_Items', float]:
        """Return the latest configured feedback snapshot."""
        ...

    @staticmethod
    def is_valid_actuator_address(address: int) -> bool:
        """Return whether ``address`` is a valid actuator network address."""
        ...

    def stop(self) -> None:
        """Disable virtual actuator control."""
        ...

    def get_model_version(self) -> str:
        """Return DTwin model/build metadata for this virtual actuator."""
        ...

    @staticmethod
    def discover_available_actuators(bindings_path: str | Path) -> list[str]:
        """
        Return virtual actuator models available under a bindings path.

        Args:
            bindings_path: Directory containing generated DTwin artifacts.

        Returns:
            Available actuator model names. Missing directories return an empty
            list.
        """
        ...

    def set_actuator(self, model_name: str, library_path: str | Path | None = None, bindings_root: str | Path | None = None) -> Any:
        """
        Configure the digital twin by model name.

        When ``library_path`` is provided, it is treated as an actuator-library
        YAML file. Without a YAML file, the method resolves generated DTwin
        artifacts directly from ``bindings_root`` or the repo assets folder.

        Args:
            model_name: Actuator model name to load.
            library_path: Optional actuator-library YAML path.
            bindings_root: Optional root used to discover generated artifacts.

        Returns:
            Configured DTwin actuator wrapper.
        """
        ...

    def set_actuator_from_paths(self, library_path: str | Path, bindings_path: str | Path) -> Any:
        """
        Configure the digital twin from explicit artifact paths.

        Args:
            library_path: Path to the generated DTwin shared library.
            bindings_path: Path to the generated Python bindings.

        Returns:
            Configured DTwin actuator wrapper.
        """
        ...

    def connect(self, timeout: float = 1.0) -> bool:
        """
        Connect to the configured virtual actuator.

        Args:
            timeout: Accepted for real API compatibility; unused by the virtual
                backend.

        Returns:
            ``True`` when a DTwin actuator wrapper is configured.
        """
        ...

    def disconnect(self) -> None:
        """Terminate the virtual actuator backend and mark it disconnected."""
        ...

    def send_ping(self, timeout: float = 1.0) -> bool:
        """
        Return whether the virtual actuator is configured and connected.

        Args:
            timeout: Accepted for real API compatibility; unused by the virtual
                backend.
        """
        ...

    def change_address(self, new_address: int) -> None:
        """
        Set the virtual PCP address.

        Args:
            new_address: New virtual actuator address in the valid actuator range.
        """
        ...

    def start(self) -> None:
        """Enable virtual actuator control."""
        ...

    def change_mode(self, mode: 'PulsarActuatorVirtual.Mode') -> None:
        """
        Change the virtual actuator control mode.

        Args:
            mode: Control mode to activate.
        """
        ...

    def get_mode(self) -> 'PulsarActuatorVirtual.Mode':
        """Return the current virtual actuator control mode."""
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
        Switch to torque mode and apply a torque setpoint.

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
        Switch to speed mode and apply a speed setpoint.

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
        Switch to position mode and apply a position setpoint.

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
        Switch to impedance mode and apply an impedance setpoint.

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

    def set_home_position(self) -> None:
        """Set the current virtual actuator position as the zero reference."""
        ...

    def set_feedback_items(self, items: list['PulsarActuatorVirtual.PCP_Items']) -> None:
        """
        Configure the feedback items emitted by simulation steps.

        Args:
            items: Feedback items to include in emitted snapshots.
        """
        ...

    def set_feedback_rate(self, rate: 'PulsarActuatorVirtual.Rates | int') -> None:
        """
        Configure feedback emission rate for simulation steps.

        Args:
            rate: A ``Rates`` divider enum or integer target rate in Hz. Use
                ``Rates.DISABLED`` or ``0`` to disable callback emission.
        """
        ...

    def get_items_blocking(self, items: list['PulsarActuatorVirtual.PCP_Items'], timeout: float = 1.0) -> dict['PulsarActuatorVirtual.PCP_Items', float]:
        """
        Return requested feedback values from the current simulator state.

        Args:
            items: Feedback items to read. Requests are capped at the protocol
                batch limit.
            timeout: Accepted for real API compatibility; unused by the virtual
                backend.

        Returns:
            Mapping from requested feedback items to current values.
        """
        ...

    def set_parameters(self, parameters: dict['PulsarActuatorVirtual.PCP_Parameters', float]) -> None:
        """
        Write virtual actuator parameters.

        Args:
            parameters: Mapping from parameter enum to the value to write.
        """
        ...

    def get_parameters(self, parameters: list['PulsarActuatorVirtual.PCP_Parameters'], timeout: float = 1.0) -> dict['PulsarActuatorVirtual.PCP_Parameters', float]:
        """
        Read virtual actuator parameters.

        Args:
            parameters: Parameters to read.
            timeout: Accepted for real API compatibility; unused by the virtual
                backend.

        Returns:
            Mapping from parameter enum to current value.
        """
        ...

    def get_parameters_all(self) -> dict['PulsarActuatorVirtual.PCP_Parameters', float]:
        """Read all known virtual actuator parameters."""
        ...

    def set_can_high_speed(self, enabled: bool) -> None:
        """Store CAN high-speed state for real API compatibility."""
        ...

    def set_torque_performance(self, performance: 'PulsarActuatorVirtual.TorquePerformance') -> None:
        """Set the virtual torque-control performance preset."""
        ...

    def set_speed_performance(self, performance: 'PulsarActuatorVirtual.SpeedPerformance') -> None:
        """Set the virtual speed-control performance preset."""
        ...

    def save_config(self) -> None:
        """Log that virtual actuators do not persist configuration."""
        ...

    def blink(self, timeout: float = 1.0) -> None:
        """Log that physical LED blinking is unavailable for virtual actuators."""
        ...

    def step(self, load: float | None = None, steps: int = 1) -> dict['PulsarActuatorVirtual.PCP_Items', float]:
        """
        Advance the simulation explicitly.

        This is the main virtual-only extension beyond the real actuator API.

        Args:
            load: Optional load torque to apply before stepping.
            steps: Number of simulation steps to run.

        Returns:
            Latest configured feedback snapshot after stepping.
        """
        ...

    def start_steps(self, step_number: int) -> None:
        """Advance the simulation by ``step_number`` steps."""
        ...

    def change_load(self, load: float) -> None:
        """Change the load torque applied to future simulation steps."""
        ...

    def get_sim_time(self, round_dec: int = 3) -> float:
        """
        Return the latest simulated time.

        Args:
            round_dec: Decimal places used to round the returned time.
        """
        ...

    def get_sim_time_step_s(self) -> float:
        """
        Return the DTwin simulation step time in seconds.

        The current DTwin artifacts use the wrapper's telemetry log timestep.
        If a future generated artifact exposes timestep metadata, the backend
        wrapper will return that value through the same public API.
        """
        ...

    def get_sim_rate_hz(self) -> float:
        """Return the DTwin simulation step rate in Hz."""
        ...

    def get_all_parameters(self) -> dict[str, dict]:
        """Return grouped DTwin controller, impedance, limit, and profile values."""
        ...

    def get_info(self) -> dict[str, float]:
        """Return the DTwin ``info`` state as plain Python values."""
        ...

    def get_motor_state(self) -> dict[str, float]:
        """Return the DTwin motor state as plain Python values."""
        ...

    def get_measurements(self) -> dict[str, float]:
        """Return the DTwin measurement state as plain Python values."""
        ...

    def get_debug_flags(self) -> dict[str, bool]:
        """Return DTwin debug flags as booleans."""
        ...

    def has_errors(self) -> bool:
        """Return whether any DTwin debug error flag is set."""
        ...
