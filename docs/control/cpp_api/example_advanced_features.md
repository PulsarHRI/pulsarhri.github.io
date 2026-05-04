# Advanced Actuator Configuration

This tutorial shows several advanced configuration features available in the PULSAR HRI C++ API. In addition to changing configuration values and saving them to persistent memory, this version also tests the actuator in different control modes so you can verify the applied settings in practice.

!!! warning
    Make sure the actuator can move freely and safely before starting the example.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the actuator is connected and reachable,
- the user has permission to access the communication device,
- the actuator can move safely in the selected test conditions.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>

using namespace pcp_api;
```

## Overview

This example performs the following steps:

1. Connects to one actuator.
2. Changes the actuator address.
3. Updates torque and speed performance profiles.
4. Sets custom control parameters.
5. Saves the configuration to persistent memory.
6. Tests the configuration in position, speed, and torque modes.
7. Reads back selected parameters.
8. Disconnects and closes the adapter.

## Connect to the adapter and actuator

The code below creates the adapter, connects to the actuator, and prints basic device information.

```cpp
std::string port = PCP_over_USB::get_port();
// std::string port = "COM1";

std::cout << "Connecting to " << port << std::endl;
PCP_over_USB adapter(port);

constexpr int ACTUATOR_ADDRESS = 0;  // 0 for direct USB connection, or use the actuator address if using CAN
PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);

if (!actuator.connect()) {
    std::cerr << "Could not connect to the actuator "
              << ACTUATOR_ADDRESS << std::endl;
    adapter.close();
    throw std::runtime_error("Actuator connection failed");
}

std::cout << "Connected to the actuator "
          << actuator.address()
          << " (model: " << actuator.model()
          << ", firmware: " << actuator.firmware_version()
          << ")"
          << std::endl;
```

## Change the actuator address

Set a new PCP address for the actuator and print the updated value.

```cpp
actuator.changeAddress(0x15);

std::cout << "Actuator new address: " << actuator.address() << std::endl;
```

## Change performance profiles

Select predefined performance profiles for the torque and speed controllers.

```cpp
std::cout << "Setting performance parameters..." << std::endl;
actuator.set_torque_performance(PulsarActuator::TorquePerformance::AGGRESSIVE);
actuator.set_speed_performance(PulsarActuator::SpeedPerformance::BALANCED);
```

## Set custom control parameters

Use `set_parameters()` to update one or more control parameters at the same time.

```cpp
actuator.set_parameters({
    {PulsarActuator::PCP_Parameters::K_DAMPING, 7.7f},
    {PulsarActuator::PCP_Parameters::K_STIFFNESS, 8.8f},
});
```

## Save the configuration

Save the current configuration so the new settings are retained across power cycles.

```cpp
actuator.save_config();
```

## Test the position control mode

Switch to `POSITION` mode, apply a setpoint, start the actuator, wait for the movement to complete, and then stop it.

```cpp
std::cout << "Testing new configuration with the position control mode..." << std::endl;
actuator.change_mode(PulsarActuator::Mode::POSITION);
actuator.change_setpoint(0.7854f);  // rad, about 45 degrees

actuator.start();

std::this_thread::sleep_for(std::chrono::seconds(2));

actuator.stop();

std::this_thread::sleep_for(std::chrono::seconds(2));
```

## Test the speed control mode

Switch to `SPEED` mode, apply a speed setpoint, run the actuator for a few seconds, and then stop it.

```cpp
std::cout << "Testing speed control mode..." << std::endl;
actuator.change_mode(PulsarActuator::Mode::SPEED);
actuator.change_setpoint(0.5f);  // rad/s

actuator.start();

std::this_thread::sleep_for(std::chrono::seconds(5));

actuator.stop();

std::this_thread::sleep_for(std::chrono::seconds(2));
```

## Test the torque control mode

Switch to `TORQUE` mode, apply a torque setpoint, keep the actuator running for a few seconds, and then stop it.

```cpp
std::cout << "Testing torque control mode..." << std::endl;
actuator.change_mode(PulsarActuator::Mode::TORQUE);
actuator.change_setpoint(0.3f);  // Nm

actuator.start();

std::this_thread::sleep_for(std::chrono::seconds(5));

actuator.stop();

std::this_thread::sleep_for(std::chrono::seconds(2));
```

## Read back parameters

Use `get_parameters()` to verify selected configuration values.

```cpp
auto params = actuator.get_parameters({
    PulsarActuator::PCP_Parameters::MODE,
    PulsarActuator::PCP_Parameters::SETPOINT,
    PulsarActuator::PCP_Parameters::K_STIFFNESS,
});

std::cout << "Read parameters:" << std::endl;
for (const auto& [parameter, value] : params) {
    std::cout << "  parameter " << static_cast<int>(parameter)
              << " -> " << value << std::endl;
}

std::cout << "K_STIFFNESS = "
          << params[PulsarActuator::PCP_Parameters::K_STIFFNESS]
          << std::endl;
```

## Disconnect and clean up

Disconnect the actuator and close the adapter when the test is finished.

```cpp
actuator.disconnect();
adapter.close();
```

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>

using namespace pcp_api;

int main()
{
    PCP_over_USB* adapter_ptr = nullptr;
    PulsarActuator* actuator_ptr = nullptr;

    try {
        std::string port = PCP_over_USB::get_port();
        // std::string port = "COM1";

        std::cout << "Connecting to " << port << std::endl;
        PCP_over_USB adapter(port);
        adapter_ptr = &adapter;

        constexpr int ACTUATOR_ADDRESS = 0;  // 0 for direct USB connection, or use the actuator address if using CAN
        PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);
        actuator_ptr = &actuator;

        if (!actuator.connect()) {
            std::cerr << "Could not connect to the actuator "
                      << ACTUATOR_ADDRESS << std::endl;
            adapter.close();
            return 1;
        }

        std::cout << "Connected to the actuator "
                  << actuator.address()
                  << " (model: " << actuator.model()
                  << ", firmware: " << actuator.firmware_version()
                  << ")"
                  << std::endl;

        actuator.changeAddress(0x15);

        std::cout << "Actuator new address: " << actuator.address() << std::endl;

        std::cout << "Setting performance parameters..." << std::endl;
        actuator.set_torque_performance(PulsarActuator::TorquePerformance::AGGRESSIVE);
        actuator.set_speed_performance(PulsarActuator::SpeedPerformance::BALANCED);

        actuator.set_parameters({
            {PulsarActuator::PCP_Parameters::K_DAMPING, 7.7f},
            {PulsarActuator::PCP_Parameters::K_STIFFNESS, 8.8f},
        });

        actuator.save_config();

        std::cout << "Testing new configuration with the position control mode..." << std::endl;
        actuator.change_mode(PulsarActuator::Mode::POSITION);
        actuator.change_setpoint(0.7854f);  // rad, about 45 degrees

        actuator.start();
        std::this_thread::sleep_for(std::chrono::seconds(2));
        actuator.stop();
        std::this_thread::sleep_for(std::chrono::seconds(2));

        std::cout << "Testing speed control mode..." << std::endl;
        actuator.change_mode(PulsarActuator::Mode::SPEED);
        actuator.change_setpoint(0.5f);  // rad/s

        actuator.start();
        std::this_thread::sleep_for(std::chrono::seconds(5));
        actuator.stop();
        std::this_thread::sleep_for(std::chrono::seconds(2));

        std::cout << "Testing torque control mode..." << std::endl;
        actuator.change_mode(PulsarActuator::Mode::TORQUE);
        actuator.change_setpoint(0.3f);  // Nm

        actuator.start();
        std::this_thread::sleep_for(std::chrono::seconds(5));
        actuator.stop();
        std::this_thread::sleep_for(std::chrono::seconds(2));

        auto params = actuator.get_parameters({
            PulsarActuator::PCP_Parameters::MODE,
            PulsarActuator::PCP_Parameters::SETPOINT,
            PulsarActuator::PCP_Parameters::K_STIFFNESS,
        });

        std::cout << "Read parameters:" << std::endl;
        for (const auto& [parameter, value] : params) {
            std::cout << "  parameter " << static_cast<int>(parameter)
                      << " -> " << value << std::endl;
        }

        std::cout << "K_STIFFNESS = "
                  << params[PulsarActuator::PCP_Parameters::K_STIFFNESS]
                  << std::endl;

        actuator.disconnect();
        adapter.close();
    }
    catch (const std::exception& e) {
        if (actuator_ptr != nullptr) {
            try {
                actuator_ptr->disconnect();
            } catch (...) {
            }
        }

        if (adapter_ptr != nullptr) {
            try {
                adapter_ptr->close();
            } catch (...) {
            }
        }

        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```

## Example build command

Adjust the include path, library path, and library names to match your build output.

```bash
g++ -std=c++17 <filename>.cpp -I../include -L. -lpcp_api -lpthread -lserialport -o <filename>
```