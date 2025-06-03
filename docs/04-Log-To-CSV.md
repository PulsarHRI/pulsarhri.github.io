# 04. Log Data to CSV
This script is designed to connect to a Pulsar actuator using a CAN-over-USB adapter. It logs high-frequency sensor data and saves it to a CSV file for later analysis.

## Import Required Modules

```py title="" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from time import sleep, time
import csv
```
## Connect to the CAN Adapter

```py title="" 
# Automatically detect the CAN port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")

# Initialize the adapter
adapter = CANoverUSB(port)
```
# Initialize the Actuator
This creates an actuator object at address 0
```py title="" 
actuator = PulsarActuator(adapter, 0)
```
## Specify the Logging Variables
Specifies which sensor data to log (e.g., torque sensor, PCB temperature)

```py title=""
if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
print(f"Connected to the actuator {actuator.address}")
```
## Configuration of the Feedback Rates
* Sets up high-frequency feedback (1kHz) for selected items.
* Disables low-frequency feedback.

```py title=""
actuator.setHighFreqFeedbackItems(itemsToLog)
actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_1KHZ)
actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)
```
## Preaparig CSV Logging 
This opens a CSV file for writing

```py title=""
file = open("log.csv", "w")
csv_writer = csv.writer(file, lineterminator='\n')
```
Adding a header row with the timestamp and item names

```py title=""
# add header
header = [time()]  # timestamp
header.extend([item.name for item in sorted(itemsToLog, key=lambda x: x.name)])  # sorted by name for consistent order
csv_writer.writerow(header)
```
## Define Feedback Callback
This function is called whenever new feedback data is recieved

```py title=""
# add header
header = [time()]  # timestamp
header.extend([item.name for item in sorted(itemsToLog, key=lambda x: x.name)])  # sorted by name for consistent order
csv_writer.writerow(header)
```
## Start Actuator

```py title=""
actuator.change_mode(PulsarActuator.Mode.SPEED)
actuator.change_setpoint(1)
actuator.start()
actuator.set_feedback_callback(actuator_feedback)
```
## Run and Cleanup 
This runs for 3 seconds, then disconnects and closes everything

```py title=""
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
The CSV is updated for postprocessing