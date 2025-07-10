# Controlling One Device

This notebook demonstrates how to connect to a Pulsar actuator using the pcp_api library and PCP_over_USB, configure feedback settings, and control one actuator in speed mode.

The full example is at the [bottom of the page](#full-example).

## Import necessary modules

```py
from pcp_api import PCP_over_USB, PulsarActuator
from pprint import pprint
from time import sleep
```
## Instantiate the adapter

Pulsar devices understand the PCP protocol, which can be communicated over USB or CAN. The devices has a built-in USB interface, so you can connect directly to the actuator via USB. Alternatively, you can use a CAN adapter to connect to the actuator over a CAN bus. This can adapter is connected to the host computer via USB, so in both cases, you will use the `PCP_over_USB` class to create the adapter.

```py
port = "COM1"  # you need to specify the port of the device or the CAN adapter
# port = PCP_over_USB.get_port()  # there is also an auto-detect system that will find the first available port
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
```

## Instantiate the actuator

You can instantiate as many actuators as you want with the same adapter. In this example we are going to control only one actuator, connected directly via USB. If you are using a CAN adapter, you need to specify the PCP address of the actuator. The PCP address is a unique identifier for each actuator on the CAN bus. You can find this address with the  [CLI scan command](../../cli.md#scan-for-devices). If you are connecting directly via USB, you can use `0` as the address.

```py
ACTUATOR_ADDRESS = 0  # 0 for direct USB connection, or use the actuator address if using CAN adapter
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)
actuator.connect()
print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")
```

## Configure feedback

first define in the top a function to handle the feedback from the actuator. This function will be called whenever new feedback is received from the actuator.

```py
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
```

Set up the feedback configuration and control mode:

* High-frequency feedback for data like speed, position, torque, ...
* Low-frequency feedback for data like bus voltage, temperatures....

```py title="Configure feedback and control settings"
actuator.setHighFreqFeedbackItems([
    PulsarActuator.PCP_Items.SPEED_FB,
    PulsarActuator.PCP_Items.POSITION_FB,
    PulsarActuator.PCP_Items.TORQUE_FB,
    # You can add more items as needed
])
actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)

# Low-frequency feedback includes bus voltage and motor temperature.
actuator.setLowFreqFeedbackItems([
    PulsarActuator.PCP_Items.VBUS,
    PulsarActuator.PCP_Items.TEMP_MOTOR,
])
actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

actuator.set_feedback_callback(actuator_feedback)
```

## Configure control settings


```py title="Configure control settings"
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1.0)  # rad/s
    actuator.start()
    # The actuator is started and feedback is monitored in a loop.
    # The loop will keep running until interrupted (e.g., by pressing `Stop` in the notebook).
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered
```


## Shutdown
Ensure the actuator is properly disconnected and the adapter is closed when the program is interrupted (e.g., via Ctrl+C or notebook stop if running from a Jupyter notebook).

```py title="Shutdown"
try:
    # Put the configuration and control code here
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()  # will also stop the actuator
    sleep(0.1)
    adapter.close()
```

## Full Example

```py title="Full Example"
from pcp_api import PCP_over_USB, PulsarActuator
from pprint import pprint
from time import sleep


ACTUATOR_ADDRESS = 0  # 0 to indicate direct USB connection, or use the PCP address if using CAN adapter


def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")


port = PCP_over_USB.get_port()  # auto-detect
# port = "COM1"
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")
try:
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)
    # feedback_callback can be set to None to disable it
    # and read the feedback manually with actuator.get_feedback()

    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1.0)  # rad/s because mode is SPEED

    # params = actuator.get_parameters([
    #     PulsarActuator.PCP_Parameters.FIRMWARE_VERSION,
    #     PulsarActuator.PCP_Parameters.MODE,
    #     PulsarActuator.PCP_Parameters.SETPOINT,
    # ])
    params = actuator.get_parameters_all()
    pprint(params)
    actuator.start()
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()  # also stops the actuator
    sleep(0.1)
    adapter.close()
```
