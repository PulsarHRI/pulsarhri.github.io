# Advanced Features

This notebook demonstrates advanced configuration and control of a Pulsar actuator using the pcp_api library. It builds upon the basic example, which covers:

* Connecting to the actuator
* Setting feedback items and rates
* Running in speed mode with a fixed setpoint

In this advanced tutorial, you will learn how to:

* 🔄 Reset the encoder to define a custom zero position
* 🆔 Change the actuator's PCP address dynamically
* ⚙️ Tune performance profiles (torque and speed)
* 🎛️ Set custom control parameters (e.g., stiffness and damping)
* 💾 Optionally save configuration to persistent memory

These features are useful for fine-tuning actuator behavior, multi-actuator setups, and persistent deployment scenarios.

## Import Required Modules
We begin by importing the necessary modules to interact with the actuator, manage the CAN interface, and handle timing and output formatting.
```py title="Import Required Modules" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```

## Detect and Connect to the CAN Adapter
This section automatically detects the USB port where the CAN adapter is connected and initializes the adapter for communication.
```py title="Detect and Connect to the CAN Adapter" 
# Automatically detect the CAN port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")

# Initialize the adapter
adapter = CANoverUSB(port)
```
## Initialize the Actuator
We create an instance of the actuator using address 0 and attempt to establish a connection. If the connection fails, the program exits gracefully.
```py title="Initialize the Actuator" 
# Create actuator instance with ID 0
actuator = PulsarActuator(adapter, 0)

# Attempt to connect
if not actuator.connect():
    print("Could not connect to the actuator")
    adapter.close()
    raise SystemExit("Exiting due to connection failure.")
print("Connected to the actuator")
```
## Define the control parameters
Here we define the performance profiles and control parameters:

* Torque performance is set to BALANCED for fast torque response.
* Speed performance is also set to BALANCED for quick speed adjustments.
* Control parameters like damping and stiffness are set to custom values to fine-tune the actuator's dynamic behavior.

```py title="Define the control parameters"
K_DAMPING = 7.7
K_STIFFNESS = 8.8 
```
## Apply Advanced Configuration
This block performs several advanced configuration steps:

* Resets the encoder to define a new zero position.
* Changes the actuator's address (optional).
* Applies performance profiles for torque and speed.
* Sets custom control parameters.
* Optionally saves the configuration to persistent memory.

```py title="Apply Advanced Configuration"
try:
    # Reset encoder to define zero position
    actuator.reset_encoder_position()

    # Change the actuator's address (optional)
    actuator.changeAddress(0x15)

    # Set performance modes
    actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
    actuator.set_speed_performance(PulsarActuator.SpeedPerformance.AGGRESSIVE)

    # Set control parameters
    actuator.set_parameters({
        PulsarActuator.PCP_Parameters.K_DAMPING: K_DAMPING ,
        PulsarActuator.PCP_Parameters.K_STIFFNESS: K_STIFFNESS,
    })

    # Optional: Save configuration to persistent memory
    actuator.save_config()

except KeyboardInterrupt:
    print("Interrupted by user.")
    
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
    print("Disconnected and cleaned up.")
```
## Run and Verify That the Motor Control Behaves as Required
This section reinitializes the actuator and sets it up for real-time feedback monitoring. It demonstrates how to verify that the actuator behaves as expected after applying the advanced configuration.

```py title="Run and Verify That the Motor Control Behaves as Required"
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")
        
ACTUATOR_ADDRESS = 0
       
port = CANoverUSB.get_port()  # auto-detect
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
else:
    print(f"Connected to the actuator {actuator.address}")

try:
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)

    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1)  # rad/s
    # Retrieve and Display Actuator Parameters
    params = actuator.get_parameters_all()
    pprint(params)
    
    # Start the actuator and monitor feedback

    # The loop will keep running until interrupted (e.g., by pressing `Stop` in the notebook).
    actuator.start()
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered

## Shutdown

#Disconnect the actuator and close the adapter when the program is interrupted.

except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
```

## Full code

The Jupyter notebook can be downloaded [here](03-R-changing-parameters.ipynb).

```py title="Full code" linenums="1"
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep

# Automatically detect the CAN port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")

# Initialize the adapter
adapter = CANoverUSB(port)

# Create actuator instance with ID 0
actuator = PulsarActuator(adapter, 0)

# Attempt to connect
if not actuator.connect():
    print("Could not connect to the actuator")
    adapter.close()
    raise SystemExit("Exiting due to connection failure.")
print("Connected to the actuator")

K_DAMPING = 7.7
K_STIFFNESS = 8.8 

try:
    # Reset encoder to define zero position
    actuator.reset_encoder_position()

    # Change the actuator's address (optional)
    actuator.changeAddress(0x15)

    # Set performance modes
    actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
    actuator.set_speed_performance(PulsarActuator.SpeedPerformance.AGGRESSIVE)

    # Set control parameters
    actuator.set_parameters({
        PulsarActuator.PCP_Parameters.K_DAMPING: K_DAMPING ,
        PulsarActuator.PCP_Parameters.K_STIFFNESS: K_STIFFNESS,
    })

    # Optional: Save configuration to persistent memory
    actuator.save_config()

except KeyboardInterrupt:
    print("Interrupted by user.")
    
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
    print("Disconnected and cleaned up.")

def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")
        
ACTUATOR_ADDRESS = 0
       
port = CANoverUSB.get_port()  # auto-detect
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
else:
    print(f"Connected to the actuator {actuator.address}")

try:
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)

    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1)  # rad/s
    # Retrieve and Display Actuator Parameters
    params = actuator.get_parameters_all()
    pprint(params)
    
    # Start the actuator and monitor feedback

    # The loop will keep running until interrupted (e.g., by pressing `Stop` in the notebook).
    actuator.start()
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered

## Shutdown

#Disconnect the actuator and close the adapter when the program is interrupted.

except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
```