# 02. Controlling Two Targets

This notebook demonstrates how to control Pulsar actuators using the CANoverUSB interface. We will go through the steps of connecting to the USB-CAN adapter, initializing the actuators, configuring them, and finally running them.

```py title="" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```
## Define Constants and Feedback Function
We define the CSP addresses for the actuators and a feedback function to handle actuator feedback.

```py title="" 
# Example CSP addresses for two actuators
CSP_ADDRESSES = [0x10, 0x11]
```
## Define a feedback callback function

This function will be called automatically when feedback is received from the actuator.

```py title="" 
def actuator_feedback(address: int, feedback: dict):
    position = feedback.get(PulsarActuator.PCP_Items.POSITION_FB, None)
    print(f"Actuator 0x{address:X} position: {position:.2f} rad/s")
```
## Connect to USB-CAN Adapter
We connect to the USB-CAN adapter. The port is auto-detected.

```py title=""
# Auto-detect the port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
```
## Initialize and Configure Actuators
We initialize the actuators, connect to them, and configure their feedback settings.

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
We set different speeds for each actuator and start them.

```py title=""
# Set different speeds for each actuator
actuators[0].change_setpoint(0.2)
actuators[1].change_setpoint(0.3)

# Start all actuators
for actuator in actuators:
    actuator.start()
```
## Run and Cleanup
We run the actuators for a short period and then clean up by disconnecting the actuators and closing the adapter.

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