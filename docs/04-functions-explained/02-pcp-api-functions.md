# Real hardware functions explained

## Communication 
### connect(timeout=1.0) - bool

!!! info
    Initiates communication with the actuator by sending a PING message and waiting for a PONG response.

Args: timeout (float, optional): Maximum time to wait for a response, in seconds. Default is 1.0.
Returns: True if the actuator responds within the timeout window, False otherwise.

### disconnect()
!!! info
    Safely terminates communication by sending a STOP command to halt any ongoing operations.

### send_ping(timeout=1.0) - bool
!!! info
    Sends a PING message and waits for a PONG response within a specified timeout.

Args: timeout (float, optional): The maximum time to wait for a pong response, in seconds. Default is 1.0 second.
Returns: True if a pong response is received within the timeout period, False otherwise.

### changeAddress(new_address)
!!! info
    Assigns a new CAN address to the actuator.

Args: new_address (int): The new CAN address to assign. Must be within the valid range 0x10 ≤ new_address ≤ 0x3FFE.

## Control

### start()
!!! info
    Starts the actuator's operation.

### stop()
!!! info
    Stops the actuator's current motion and operation.

### change_mode(mode: Mode)
!!! info
    Changes the mode of the actuator.

Args: mode (PulsarActuator.Mode): The mode to be set.

**Modes**:

* PulsarActuator.Mode.CALIBRATION
* PulsarActuator.Mode.FVI
* PulsarActuator.Mode.OPEN_LOOP
* PulsarActuator.Mode.DVI
* PulsarActuator.Mode.TORQUE
* PulsarActuator.Mode.SPEED
* PulsarActuator.Mode.POSITION
* PulsarActuator.Mode.IMPEDANCE

### change_setpoint(setpoint)
!!! info
    Changes the setpoint of the actuator.

Args: setpoint (float): The setpoint to be set. The units of all the setpoints are in international system units (rad, rad/s, Nm)

### set_torque_performance(performance: TorquePerformance)
!!! info
    Sets the torque performance.
Args: performance (PulsarActuator.TorquePerformance): The torque performance to be set.

[**Torque performance options**](00-functions-overview.md/#torque-control-loop-performance):

* PulsarActuator.TorquePerformance.AGRESSIVE
* PulsarActuator.TorquePerformance.BALANCED
* PulsarActuator.TorquePerformance.SOFT

### set_speed_performance(performance: SpeedPerformance)

!!! info
    Sets the speed performance.
Args: performance (PulsarActuator.SpeedPerformance): The speed performance to be set.

[**Speed performance options**](00-functions-overview.md/#predefined-performance-profiles):

* PulsarActuator.SpeedPerformance.AGRESSIVE
* PulsarActuator.SpeedPerformance.BALANCED
* PulsarActuator.SpeedPerformance.SOFT
* PulsarActuator.SpeedPerformance.CUSTOM To be able to set the values of KP_SPEED and KI_SPEED manually using [set_parameters](#set_parametersparameters) you should first set this speed performance option.

### reset_encoder_position()
!!! info
    Resets the encoder absolute position to 0. Do this before using the position based controls.

### save_config()
!!! info
    Saves the current configuration of the actuator in non-volatile memory.

### calibrate()
!!! info 
    Performs internal calibration routines to align the motor’s electrical position with the mechanical position of the encoder and get the ADCs offsets.
!!! warning
    DO NOT USE THIS UNLESS SPECIFIED BY PULSAR TEAM

## Logging

### set_feedback_callback(callback: callable) - None
!!! info
    Registers a function to be called whenever new feedback is received.

Args: callback (callable): The function to be executed with each feedback update.

### get_feedback() - dict
!!! info
    Returns the feedback dictionary containing real-time data from the actuator.
Returns: dict: The feedback dictionary.
### setHighFreqFeedbackItems(items: list)
!!! info
    Sets the items to be sent in the high-frequency feedback.

Args: items (list): The list of PulsarActuator.PCP_Items to be sent.

### setLowFreqFeedbackItems(items: list)
!!! info
    Sets the items to be sent in the low-frequency feedback.

Args: items (list): The list of PulsarActuator.PCP_Items to be sent.

### setHighFreqFeedbackRate(rate: Rates)
!!! info
    Sets the rate of the high-frequency feedback.

Args: rate (Rates): The rate in Hz.

### setLowFreqFeedbackRate(rate: Rates)
!!! info
    Sets the rate of the low-frequency feedback.

Args: rate (Rates): The rate in Hz.

**Rates**:

* PulsarActuator.Rates.DISABLED
* PulsarActuator.Rates.RATE_1KHZ
* PulsarActuator.Rates.RATE_100HZ
* PulsarActuator.Rates.RATE_50HZ
* PulsarActuator.Rates.RATE_10HZ
* PulsarActuator.Rates.RATE_5HZ
* PulsarActuator.Rates.RATE_2HZ
* PulsarActuator.Rates.RATE_1HZ

## Read and set parameters

### [set_parameters(parameters)](01-actuator-parameters-explained.md/#set_parametersparameters)

!!! info
    Set parameters.

### [get_parameters(parameters, timeout=1.0)](01-actuator-parameters-explained.md/#get_parametersparameters-timeout10)

!!! info
    Get parameters.

### [get_parameters_all()](01-actuator-parameters-explained.md/#get_parameters_all)

!!! info
    Get all parameters.

