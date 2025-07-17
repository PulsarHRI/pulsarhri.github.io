# Connection and Address Management
The `PulsarActuator` class provides methods to establish and terminate communication with an actuator, verify its availability, and configure its CAN address.
## Connecting to the Actuator
To initiate communication with an actuator, use the `connect()` method.
* Description: Sends a PING message to the actuator and waits for a PONG response within the specified timeout period.

* Parameters: timeout (float, optional): Maximum time to wait for a response, in seconds. Default is 1.0.
* Returns: True if the actuator responds within the timeout window, False otherwise.
* Usage Example:
```bash
if actuator.connect():
    print("Actuator connected successfully.")
else:
    print("Failed to connect to actuator.")
```

## Disconnecting from the Actuator
To safely terminate communication, use the `disconnect()` method:

* Description: Sends a STOP command to the actuator to halt any ongoing operations and ensure a safe disconnection.
* Usage Example: 
```bash
actuator.disconnect()
```

## Pinging the Actuator
To check if a specific CAN address is active and responsive, use the send_ping() method.
* Description: Sends a PING message and waits for a PONG response.

* Parameters: timeout (float, optional): Time to wait for a response, in seconds. Default is 1.0.
Returns:
True if a response is received within the timeout, False otherwise.

Usage Example:
```bash
if actuator.send_ping():
    print("Actuator is responsive.")
else:
    print("No response from actuator.")
```

## Changing the Actuator's CAN Address
By default, actuators may start with a randomly assigned CAN address. To integrate the actuator into a known network configuration, you can assign it a specific address using:
```bash
changeAddress(new_address)
```
* Parameters: new_address (int): The new CAN address to assign. Must be within the valid range:
```bash
0x10 ≤ new_address ≤ 0x3FFE
```
* Usage Example: 
```bash
actuator.changeAddress(0x20)
```

!!! important 
    Make sure to assign a unique CAN address to each actuator to avoid communication conflicts on the network.
