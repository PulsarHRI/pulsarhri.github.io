# Initialization and Constructor
To create an instance of the `PulsarActuator` class, you must provide a CAN bus handler (commonly referred to as an adapter) and the actuator’s CAN address. Optionally, you may also supply a custom logger for debugging and monitoring purposes.
## Python Usage
```bash
PulsarActuator(canbus_handler, address: int, logger=None)
```

## Parameters
* canbus_handler (object):An object responsible for managing communication over the CAN bus. This handler must implement the method:
```bash
setCallback(address, callback_fn)
```
This method is used to register a callback function that processes incoming CAN messages for the specified actuator address.
* address(int):
The unique CAN address assigned to the actuator. This address is used to identify and communicate with the specific device on the CAN network.
* logger(Logger,optional):
A Python Logger instance used for logging internal events, warnings, and errors. If not provided, the class defaults to using Python’s root logger.
