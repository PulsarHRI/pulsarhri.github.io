# Controlling Several Devices

This notebook demonstrates how to control multiple PULSAR HRI actuators. We will walk through the steps of connecting to the USB-CAN adapter, initializing two actuators, configuring their feedback settings, assigning different speed setpoints, and running them simultaneously.


## Import necessary modules

We import the necessary modules.

```py
from pcp_api import  PCP_over_USB, PulsarActuator
from time import sleep
```


## Define Constants and Feedback Function

We define the addresses for the two actuators. These addresses are used to uniquely identify each actuator on the CAN bus. You can discover the addresses of your actuators using the [CLI scan command](../cli.md#scan-for-devices)

```py
# Example PCP addresses for two actuators
ACTUATOR_ADDRESSES = [0x10, 0x11]
```


## Define a feedback callback function
This function is called automatically whenever feedback is received from any actuator. You can define individual functions for each actuator, or use a single function for all actuators. In this example, we are going to extract the position from the feedback dict, and prints it along with the actuator's address.

```py
def actuator_feedback(address: int, feedback: dict):
    position = feedback.get(PulsarActuator.PCP_Items.POSITION_FB, None)
    print(f"Actuator 0x{address:X} position: {position:.2f} rad/s")
```


## Connect to USB-CAN Adapter

We auto-detect the USB port to which the CAN adapter is connected and create an instance of the adapter. This step is essential to establish communication with the actuators.


```py
# Auto-detect CAN adapter port
port = PCP_over_USB.get_port()
# port = "COM1"
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
```


## Initialize Actuators and set common configuration

We create a loop to initialize each actuator using its address. Each actuator is connected, configured for high-frequency feedback, and set to SPEED mode. The feedback callback function is registered to handle incoming feedback from the actuators.


```py
actuators = []  # list to hold actuator instances

for address in ACTUATOR_ADDRESSES:
    # Create a PulsarActuator instance.
    actuator = PulsarActuator(adapter, address)

    # Attempt to connect to the actuator.
    if not actuator.connect():
        print(f"Could not connect to the actuator {actuator.address}")
        adapter.close()
        raise SystemExit(1)

    print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")

    # Configure high-frequency feedback to report position at 10 Hz.
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.POSITION_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)

    # Disable low-frequency feedback.
    actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)

    # Set the actuator to SPEED mode.
    actuator.change_mode(PulsarActuator.Mode.SPEED)

    # Register the feedback callback function.
    actuator.set_feedback_callback(actuator_feedback)

    actuators.append(actuator)
```


## Individual Actuator Configuration

We assign different configuration to each actuator.

```py
# Set different speeds for each actuator
actuators[0].change_setpoint(0.2)
actuators[1].change_setpoint(0.3)
```


## Run and Cleanup

We start all actuators and let them run briefly to allow feedback to be printed. When the program is interrupted (e.g., via Ctrl+C ), we ensure all actuators are properly disconnected and the adapter is closed.

```py
# Start all actuators
for actuator in actuators:
    actuator.start()

print("Actuators started. Press Ctrl+C to stop.")
try:
    sleep(0.1)  # Let feedback trigger
except KeyboardInterrupt:
    pass
finally:
    for actuator in actuators:
        actuator.disconnect()
    sleep(0.1)
    adapter.close()
```


## Full code
The Jupyter notebook can be downloaded [here](../assets/jnotebooks/several_actuators.ipynb).

```py title="Full code" linenums="1"
from pcp_api import  PCP_over_USB, PulsarActuator
from time import sleep

# Example PCP addresses for two actuators
ACTUATOR_ADDRESSES = [0x10, 0x11]

def actuator_feedback(address: int, feedback: dict):
    position = feedback.get(PulsarActuator.PCP_Items.POSITION_FB, None)
    print(f"Actuator 0x{address:X} position: {position:.2f} rad/s")

# Auto-detect CAN adapter port
port = PCP_over_USB.get_port()
# port = "COM1"
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)

actuators = []  # list to hold actuator instances

for address in ACTUATOR_ADDRESSES:
    # Create a PulsarActuator instance.
    actuator = PulsarActuator(adapter, address)

    # Attempt to connect to the actuator.
    if not actuator.connect():
        print(f"Could not connect to the actuator {actuator.address}")
        adapter.close()
        raise SystemExit(1)

    print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")

    # Configure high-frequency feedback to report position at 10 Hz.
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.POSITION_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)

    # Disable low-frequency feedback.
    actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)

    # Set the actuator to SPEED mode.
    actuator.change_mode(PulsarActuator.Mode.SPEED)

    # Register the feedback callback function.
    actuator.set_feedback_callback(actuator_feedback)

    actuators.append(actuator)

# Set different speeds for each actuator
actuators[0].change_setpoint(0.2)
actuators[1].change_setpoint(0.3)

# Start all actuators
for actuator in actuators:
    actuator.start()

print("Actuators started. Press Ctrl+C to stop.")
try:
    sleep(0.1)  # Let feedback trigger
except KeyboardInterrupt:
    pass
finally:
    for actuator in actuators:
        actuator.disconnect()
    sleep(0.1)
    adapter.close()
```