from enum import Enum
import logging
from typing import Any, Callable, Dict, List, Optional, Union
from math import nan


class PulsarActuator:
    """
    Main class for controlling Pulsar actuators via PCP (Pulsar Control Protocol).

    This class provides high-level methods to control actuator modes, setpoints,
    feedback configuration, and parameter management.
    """

    class Mode(Enum):
        """Control modes available for the Pulsar actuator."""
        TORQUE = 0x05
        SPEED = 0x06
        POSITION = 0x07
        IMPEDANCE = 0x08
        # These modes are only for testing purposes
        FVI = 0x02
        OPEN_LOOP = 0x03
        DVI = 0x04         # Field oriented voltage injection

    class Rates(Enum):
        """Feedback update rates for high/low frequency data streams."""
        DISABLED = 0       # Feedback disabled
        RATE_2KHZ = 5      # 2kHz update rate (2000 Hz)
        RATE_1KHZ = 10
        RATE_500HZ = 20
        RATE_200HZ = 50
        RATE_100HZ = 100
        RATE_50HZ = 200
        RATE_20HZ = 500
        RATE_10HZ = 1_000
        RATE_5HZ = 2_000
        RATE_2HZ = 5_000
        RATE_1HZ = 10_000

    class TorquePerformance(Enum):
        """Performance settings for torque control mode."""
        AGGRESSIVE = 1     # Fast, responsive torque control
        BALANCED = 2       # Balanced torque control
        SOFT = 3          # Smooth, gentle torque control

    class SpeedPerformance(Enum):
        """Performance settings for speed control mode."""
        AGGRESSIVE = 1     # Fast, responsive speed control
        BALANCED = 2       # Balanced speed control
        SOFT = 3          # Smooth, gentle speed control
        CUSTOM = 4        # Custom speed control parameters

    class PCP_Parameters(Enum):
        """Available parameters that can be read/written on the actuator."""
        K_DAMPING = 0x01              # Damping coefficient (Nm·s/rad) for the virtual damper behavior (Impedance Control)
        K_STIFFNESS = 0x02            # Stiffness coefficient (Nm/rad) for the virtual spring behavior (Impedance Control)
        TORQUE_FF = 0x03              # Feedforward Torque Value (Nm)
        LIM_TORQUE = 0x04             # Upper and lower bounds for how much torque can be applied in the positive and negative directions. (Nm)
        LIM_POSITION_MAX = 0x05       # Max. Position Limit (rad)
        LIM_POSITION_MIN = 0x06       # Min. Position Limit (rad)
        LIM_SPEED_MAX = 0x07          # Max. Speed Limit (rad/s)
        LIM_SPEED_MIN = 0x08          # Min. Speed Limit (rad/s)
        PROFILE_POSITION_MAX = 0x09   # Max. Positive Speed (rad/s) in Position control configuration
        PROFILE_POSITION_MIN = 0x0A   # Min. Negative Speed (rad/s) in Position control configuration
        PROFILE_SPEED_MAX = 0x0B      # Max. Acceleration (rad/s^2) in Speed control configuration
        PROFILE_SPEED_MIN = 0x0C      # Max. Deceleration (rad/s^2) in Speed control configuration
        KP_SPEED = 0x0D               # Kp speed control constant P value
        KI_SPEED = 0x0E               # Ki speed control constant I value
        KP_POSITION = 0x0F            # Kp position control constant P value
        MODE = 0x30                   # Operation Mode (read-only, must be set via CHANGE_MODE)
        SETPOINT = 0x31               # Setpoint, Position (rad), Speed (rad/s), Torque (Nm)
        TORQUE_PERFORMANCE = 0x40     # Torque performance setting
        SPEED_PERFORMANCE = 0x41      # Speed performance setting
        PROFILE_SPEED_MAX_RAD_S = 0x42    # Maximum profile speed in rad/s
        PROFILE_TORQUE_MAX_NM = 0x43      # Maximum profile torque in Nm
        FF_GAIN = 0x45                # Feedforward gain for friction/inertia compensation (0-1, where 1 means full compensation)
        PCP_PARAM_SPEED_CUTOFF = 0x46  # Speed cutoff frequency of the speed IIR filter
        PCP_PARAM_CURRENT_CUTOFF = 0x47  # Current cutoff frequency of the dq current IIR filter
        INVERT_FLAG = 0x44            # Invert direction of motion (boolean flag, 0 or 1)
        FIRMWARE_VERSION = 0x80       # Firmware version (read-only)
        PCP_ADDRESS = 0x81            # device PCP address
        SERIAL_NUMBER = 0x82          # Device serial number (read-only)
        DEVICE_MODEL = 0x83           # Device model identifier (read-only)
        CONTROL_VERSION = 0x84        # Control software version (read-only)
        CAN_HIGH_SPEED = 0x85         # CAN high speed mode enabled/disabled

    class PCP_Items(Enum):
        """Feedback items available for monitoring actuator state."""
        ENCODER_INT = 0x41            # Internal encoder position
        ENCODER_INT_RAW = 0x42        # Raw internal encoder counts
        ENCODER_EXT = 0x43            # External encoder position
        ENCODER_EXT_RAW = 0x44        # Raw external encoder counts
        SPEED_FB = 0x45               # Speed feedback
        IA = 0x46                     # Phase A current
        IB = 0x47                     # Phase B current
        IC = 0x48                     # Phase C current
        TORQUE_SENS = 0x49            # Torque sensor reading
        TORQUE_SENS_RAW = 0x4A        # Raw torque sensor reading
        POSITION_REF = 0x4B           # Position reference/command
        POSITION_FB = 0x4C            # Position feedback
        POSITION_FB_INTERNAL = 0x73   # Position feedback (Internal encoder)
        SPEED_REF = 0x4D              # Speed reference/command
        ID_REF = 0x4F                 # D-axis current reference
        ID_FB = 0x50                  # D-axis current feedback
        IQ_REF = 0x51                 # Q-axis current reference
        IQ_FB = 0x52                  # Q-axis current feedback
        VD_REF = 0x53                 # D-axis voltage reference
        VQ_REF = 0x54                 # Q-axis voltage reference
        TORQUE_REF = 0x55             # Torque reference/command
        TORQUE_FB = 0x56              # Torque feedback
        REFERENCE_A_VOLTAGE = 0x57    # Reference phase A voltage
        REFERENCE_B_VOLTAGE = 0x58    # Reference phase B voltage
        REFERENCE_C_VOLTAGE = 0x59    # Reference phase C voltage
        BUS_POWER = 0x5A              # Bus power
        BUS_CURRENT = 0x5B            # Bus current
        THREE_PHASE_POWER = 0x5C      # Three-phase power
        MECHANICAL_POWER = 0x5D       # Mechanical power
        INVERTER_EFFICIENCY = 0x5E    # Inverter efficiency
        MOTOR_EFFICIENCY = 0x5F       # Motor efficiency
        ERRORS_ENCODER_INT = 0x60     # Internal encoder error flags
        ERRORS_ENCODER_EXT = 0x61     # External encoder error flags
        ERRORS_OVERRUN = 0x62         # Control loop overrun errors
        VBUS = 0x70                   # Bus voltage
        TEMP_PCB = 0x71               # PCB temperature
        TEMP_MOTOR = 0x72             # Motor temperature

    def __init__(self, adapter_handler: Any, address: int, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize a PulsarActuator instance.

        Args:
            adapter_handler: Communication adapter for PCP protocol
            address: PCP network address of the actuator (0x0001-0x3FFE)
            logger: Optional logger for debugging messages
        """
        ...

    def connect(self, timeout: float = 1.0) -> bool:
        """
        Establish connection to the actuator.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connection successful, False otherwise
        """
        ...

    def set_feedback_callback(self, callback: Callable[[int, dict], None]) -> None:
        """
        Set callback function to receive feedback data.

        Args:
            callback: Function to call when feedback data is received
        """
        ...

    def set_error_callback(self, callback: Callable[[int, dict], None]) -> None:
        """
        Set the callback function for errors.

        Args:
            callback (Callable[[int, dict], None]): Function called with the
                actuator address and an error dictionary.
        """
        ...

    def disconnect(self) -> None:
        """Disconnect from the actuator and clean up resources."""
        ...

    def get_feedback(self) -> Dict[Any, Any]:
        """
        Get the latest feedback data.

        Returns:
            Dictionary containing latest feedback values
        """
        ...

    def send_ping(self, timeout: float = 1.0) -> bool:
        """
        Send ping to verify actuator connectivity.

        Args:
            timeout: Response timeout in seconds

        Returns:
            True if ping successful, False otherwise
        """
        ...

    def change_address(self, new_address: int) -> None:
        """
        Change the PCP address of the actuator.

        Args:
            new_address: New PCP address (0x10 - 0x3FFE)
        """
        ...

    def start(self) -> None:
        """Enable the actuator control system."""
        ...

    def stop(self) -> None:
        """Disable the actuator control system."""
        ...

    def change_mode(self, mode: 'PulsarActuator.Mode') -> None:
        """
        Change the actuator control mode.

        Args:
            mode (PulsarActuator.Mode): The mode to be set.  (TORQUE, SPEED, POSITION, ...)
        """
        ...

    def get_mode(self) -> 'PulsarActuator.Mode':
        """
        Returns the current control mode of the actuator.

        Returns:
            PulsarActuator.Mode: The current mode.
        """
        ...

    def change_setpoint(self, setpoint: float) -> None:
        """
        Changes the setpoint of the actuator (for the current control mode).

        Args:
            setpoint (float): The setpoint to be set.
        """
        ...

    def change_torque_setpoint(self, setpoint: float, id_Kp: float = nan, id_Ki: float = nan, iq_Kp: float = nan, iq_Ki: float = nan) -> None:
        """
        Changes the setpoint and additional parameters for torque control.

        Args:
            setpoint (float): setpoint in Nm.
            id_Kp (float, optional): The proportional gain for the d-axis current controller.
            id_Ki (float, optional): The integral gain for the d-axis current controller.
            iq_Ki (float, optional): The integral gain for the q-axis current controller.
            iq_Kp (float, optional): The proportional gain for the q-axis current controller.
        """
        ...

    def change_speed_setpoint(self, setpoint: float, FF_gain: float = nan, spd_Ki: float = nan, spd_Kp: float = nan, ref_ff_torque: float = nan) -> None:
        """
        Changes the setpoint and additional parameters for speed control.

        Args:
            setpoint (float): setpoint in rad/s.
            FF_gain (float, optional): The feedforward gain to control friction and inertia compensation. (In general should be 0 or 1)
            spd_Ki (float, optional): The integral gain for the speed controller.
            spd_Kp (float, optional): The proportional gain for the speed controller.
            ref_ff_torque (float, optional): The reference feedforward torque in Nm.
        """
        ...

    def change_position_setpoint(self, setpoint: float, FF_gain: float = nan, spd_Ki: float = nan, spd_Kp: float = nan, pos_Kp: float = nan, ref_ff_torque: float = nan) -> None:
        """
        Changes the setpoint and additional parameters for position control.

        Args:
            setpoint (float): setpoint in rad.
            FF_gain (float, optional): The feedforward gain to control friction and inertia compensation. (In general should be 0 or 1)
            spd_Ki (float, optional): The integral gain for the speed controller.
            spd_Kp (float, optional): The proportional gain for the speed controller.
            pos_Kp (float, optional): The proportional gain for the position controller.
            ref_ff_torque (float, optional): The reference feedforward torque in Nm.
        """
        ...

    def change_impedance_setpoint(self, setpoint: float, FF_gain: float = nan, K_stiff: float = nan, K_damp: float = nan, J_imp: float = nan, ref_ff_torque: float = nan, ref_impedance_spd: float = nan, ref_impedance_acel: float = nan) -> None:
        """
        Changes the setpoint and additional parameters for impedance control.

        Args:
            setpoint (float): setpoint in rad.
            FF_gain (float, optional): The feedforward gain to control friction and inertia compensation. (In general should be 0 or 1)
            K_stiff (float, optional): The stiffness parameter for impedance control.
            K_damp (float, optional): The damping parameter for impedance control.
            J_imp (float, optional): The inertia parameter for impedance control.
            ref_ff_torque (float, optional): The reference feedforward torque in Nm.
            ref_impedance_spd (float, optional): The reference impedance speed in rad/s.
            ref_impedance_acel (float, optional): The reference impedance acceleration in rad/s^2.
        """
        ...

    def save_config(self) -> None:
        """Save current configuration to non-volatile memory."""
        ...

    def blink(self) -> None:
        """
        Blinks the actuator's LED. Useful for identifying the device.
        """
        ...

    def set_feedback_items(self, items: List['PulsarActuator.PCP_Items']) -> None:
        """
        Configure which items to include in high frequency feedback stream.

        Args:
            items: List of PCP_Items to monitor at high frequency
        """
        ...

    def set_feedback_rate(self, rate: Union['PulsarActuator.Rates', int]) -> None:
        """
        Set the update rate for high frequency feedback.

        Args:
            rate: Either a PulsarActuator.Rates enum value, or an integer representing
                  the desired feedback rate in Hz. The divider is rounded to the nearest
                  integer, so the actual rate may differ slightly from the requested rate.
                  To disable feedback, use Rates.DISABLED or pass 0.
        """
        ...

    def get_items_blocking(self, items: List['PulsarActuator.PCP_Items'], timeout: float = 1.0) -> Dict['PulsarActuator.PCP_Items', float]:
        """
        Requests specific feedback items and waits for their response.

        Args:
            items (list): The list of PulsarActuator.PCP_Items to be requested.
            timeout (float): The maximum time to wait for the response, in seconds. Default is 1.0 second.

        Returns:
            dict: A dictionary with the requested items and their values.
        """
        ...

    def set_home_position(self) -> None:
        """Sets the current position as the home position (zero reference)."""
        ...

    def set_parameters(self, parameters: Dict['PulsarActuator.PCP_Parameters', float]) -> None:
        """
        Set multiple actuator parameters.

        Args:
            parameters (Dict[PulsarActuator.PCP_Parameters, float]): Mapping of
                parameters to the values to write.
        """
        ...

    def get_parameters(self, parameters: List['PulsarActuator.PCP_Parameters'], timeout: float = 1.0) -> Dict['PulsarActuator.PCP_Parameters', float]:
        """
        Read multiple actuator parameters.

        Args:
            parameters (List[PulsarActuator.PCP_Parameters]): Parameters to
                request from the actuator.
            timeout (float): Response timeout in seconds.

        Returns:
            Dict[PulsarActuator.PCP_Parameters, float]: Current values for the
                requested parameters.
        """
        ...

    def get_parameters_all(self) -> Dict['PulsarActuator.PCP_Parameters', float]:
        """
        Read all available actuator parameters.

        Returns:
            Dictionary containing all parameter values
        """
        ...

    def set_can_high_speed(self, high_speed: bool) -> None:
        """
        Enable or disable CAN high speed mode.

        Args:
            high_speed (bool): True to enable high speed mode, False to disable.
        """
        ...

    def set_torque_performance(self, performance: 'PulsarActuator.TorquePerformance') -> None:
        """
        Set torque control performance level.

        Args:
            performance: Desired performance setting (AGGRESSIVE, BALANCED, or SOFT)
        """
        ...

    def set_speed_performance(self, performance: 'PulsarActuator.SpeedPerformance') -> None:
        """
        Set speed control performance level.

        Args:
            performance: Desired performance setting (AGGRESSIVE, BALANCED, SOFT, or CUSTOM)
        """
        ...

    @property
    def address(self) -> int:
        """
        Returns the actuator's CAN address (read-only).

        Returns:
            int: The CAN address of the actuator.
        """
        ...

    @property
    def model(self) -> str:
        """
        Returns the actuator's model name (read-only).

        Returns:
            str: The model name of the actuator.
        """
        ...

    @property
    def firmware_version(self) -> str:
        """
        Returns the actuator's firmware version (read-only).

        Returns:
            str: The firmware version of the actuator.
        """
        ...


class PulsarActuatorScanner(PulsarActuator):
    """
    Scanner class for discovering Pulsar actuators on the PCP network.

    Inherits from PulsarActuator but uses broadcast address for scanning operations.
    """

    def __init__(self, adapter_handler: Any, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize a PulsarActuatorScanner instance.

        Args:
            adapter_handler: Communication adapter for PCP protocol
            logger: Optional logger for debugging messages
        """
        ...

    def scan(self, begin: int = 0x10, end: int = 0x3FFE) -> List[int]:
        """
        Scan for actuators within the specified address range.

        Args:
            begin: Starting address for scan (default: 0x10)
            end: Ending address for scan (default: 0x3FFE)

        Returns:
            List of discovered actuator addresses
        """
        ...
