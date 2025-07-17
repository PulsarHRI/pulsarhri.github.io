# Log Data to CSV

This script is an example of how to log data from a PULSAR HRI actuator. It doesn't show live data, but instead logs it to a CSV file for later analysis.
The full example is at the [bottom of the page](#full-example).


## Common code

Most of the code is common to all examples, so we will not repeat it here. You can find the common code in the [first example](01-R-single-actuator.md).


## Select the items to log
You can put the items to log from the actuator, in a list. The items are defined in `PulsarActuator.PCP_Items`. You can choose from items like `POSITION_FB`, `TORQUE_SENS`, `SPEED_FB`, ... In this example, we will log the current in the three phases of the motor, which are `IA`, `IB`, and `IC`. 

```py
itemsToLog = [
        PulsarActuator.PCP_Items.IA,
        PulsarActuator.PCP_Items.IB,
        PulsarActuator.PCP_Items.IC,
        # add more items to log
    ]

```

## Preparing CSV Logging

This opens a CSV file for writing. The key thing is to order the items in the same way they are logged. As the items are defined in an enum, you can sort them by name to ensure a consistent order.

```py
file = open("log.csv", "w")
csv_writer = csv.writer(file, lineterminator='\n')
# add header
header = ["Timestamp"]
header.extend([item.name for item in sorted(itemsToLog, key=lambda x: x.name)])  # sorted by name for consistent order
csv_writer.writerow(header)
```


## Callback function for feedback

The callback function, instead of showing the feedback in real-time, like the other examples, it directly logs the data into a file, which allows for higher rates. The feedback data is a dictionary, where the keys are `PulsarActuator.PCP_Items` and the values are the corresponding values. Again, we sort the keys by name to ensure a consistent order in the CSV file.

```py
def actuator_feedback(address: int, feedback: dict):
    line = [time()]  # timestamp
    line.extend([feedback[k] for k in sorted(feedback.keys(), key=lambda x: x.name)])  # sorted by enum name for consistent order
    csv_writer.writerow(line)
```


## Configuration of the Feedback Rates

We are going to use only high-frequency feedback at 1kHz.

```py
actuator.setHighFreqFeedbackItems(itemsToLog)
actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_1KHZ)
actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)
```


## Start Actuator

Like in the other examples, we can choose the control mode, setpoint, other parameters (not shown here) and start the actuator. In this example, we are going the let it run for 3 seconds.

```py
actuator.change_mode(PulsarActuator.Mode.SPEED)
actuator.change_setpoint(1.0)
actuator.start()
actuator.set_feedback_callback(actuator_feedback)
sleep(3)  # actuator_feedback() should be triggered during this time
```


## Run and Cleanup 

Make sure to close the file, stop the actuator and  close the adapter at the end. 

```py
actuator.disconnect()  # also stops the actuator
adapter.close()
file.close()
```


## Example output

This code will generate a CSV file named `log.csv` with the logged data. The first column is the timestamp, and the subsequent columns are the values of the items you logged. The output will look like this:

| Timestamp | IA | IB | IC |
|-----------|----|----|----|
| 1642780800.123 | 0.15 | -0.08 | 0.12 |
| 1642780800.124 | 0.16 | -0.09 | 0.13 |
| 1642780800.125 | 0.17 | -0.10 | 0.14 |


## Full Example


```py title="Full code" linenums="1"
from pcp_api import  PCP_over_USB, PulsarActuator
from time import sleep, time
import csv


itemsToLog = [
        PulsarActuator.PCP_Items.IA,
        PulsarActuator.PCP_Items.IB,
        PulsarActuator.PCP_Items.IC,
        # add more items to log
    ]


port = PCP_over_USB.get_port()  # auto-detect
# port = "COM1"
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
actuator = PulsarActuator(adapter, 0)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")

actuator.setHighFreqFeedbackItems(itemsToLog)
actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_1KHZ)
actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)

file = open("log.csv", "w")
csv_writer = csv.writer(file, lineterminator='\n')

# add header
header = ["Timestamp"]
header.extend([item.name for item in sorted(itemsToLog, key=lambda x: x.name)])  # sorted by name for consistent order
csv_writer.writerow(header)


def actuator_feedback(address: int, feedback: dict):
    line = [time()]  # timestamp
    line.extend([feedback[k] for k in sorted(feedback.keys(), key=lambda x: x.name)])  # sorted by enum name for consistent order
    csv_writer.writerow(line)


actuator.change_mode(PulsarActuator.Mode.SPEED)
actuator.change_setpoint(1.0)
actuator.start()
actuator.set_feedback_callback(actuator_feedback)
try:
    sleep(3)  # actuator_feedback() should be triggered during this time
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()  # also stops the actuator
    sleep(0.1)
    adapter.close()
    file.close()
```