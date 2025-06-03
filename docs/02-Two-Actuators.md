# 02. Controlling Two Targets

This notebook demonstrates how to control multiple Pulsar actuators using the CANoverUSB interface. We will walk through the steps of connecting to the USB-CAN adapter, initializing two actuators, configuring their feedback settings, assigning different speed setpoints, and running them simultaneously.

## Import necessary modules

```py title="" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```
## Define Constants and Feedback Function
We define the CSP (CANopen Slave Protocol) addresses for the two actuators. These addresses are used to uniquely identify each actuator on the CAN bus.

```py title="" 
# Example CSP addresses for two actuators
CSP_ADDRESSES = [0x10, 0x11]
```
## Define a feedback callback function
This function is called automatically whenever feedback is received from any actuator. It extracts the position feedback (in radians) and prints it along with the actuator's address.

```py title="" 
def actuator_feedback(address: int, feedback: dict):
    position = feedback.get(PulsarActuator.PCP_Items.POSITION_FB, None)
    print(f"Actuator 0x{address:X} position: {position:.2f} rad/s")
```
## Connect to USB-CAN Adapter
We auto-detect the USB port to which the CAN adapter is connected and create an instance of the adapter. This step is essential to establish communication with the actuators.

```py title=""
# Auto-detect the port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
```
## Initialize and Configure Actuators
For each actuator address, we:

* Create a PulsarActuator instance.
* Attempt to connect to the actuator.
* Configure high-frequency feedback to report position at 10 Hz.
* Disable low-frequency feedback.
* Set the actuator to SPEED mode.
* Register the feedback callback function.

Each successfully initialized actuator is added to a list for later control.

```py title=""
actuators = []

for address in CSP_ADDRESSES:
    actuator = PulsarActuator(adapter, address)
    if not actuator.connect():
        print(f"Could not connect to the actuator {actuator.address}")
        adapter.close()
        raise SystemExit(1)

    print(f"Connected to the actuator {actuator.address}")

    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.POSITION_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.set_feedback_callback(actuator_feedback)

    actuators.append(actuator)
```
## Set Setpoints and Start Actuators
We assign different speed setpoints to each actuator and start them. This allows both actuators to run simultaneously at different speeds.

```py title=""
# Set different speeds for each actuator
actuators[0].change_setpoint(0.2)
actuators[1].change_setpoint(0.3)

# Start all actuators
for actuator in actuators:
    actuator.start()
```
## Run and Cleanup
We let the actuators run briefly to allow feedback to be printed. When the program is interrupted (e.g., via Ctrl+C), we ensure all actuators are properly disconnected and the adapter is closed.

```py title=""
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