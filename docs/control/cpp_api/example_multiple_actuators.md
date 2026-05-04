# Controlling Multiple Real Actuators

This tutorial shows how to control multiple PULSAR HRI actuators from a single CAN to USB adapter. It focuses on what is specific to multi-actuator setups: configuring several devices on the same bus, assigning different setpoints, and starting and stopping them together.

The actuators are connected to the CAN bus through the adapter, and the adapter is connected to the host computer through USB.

!!! warning
    Do not forget the termination resistors at the ends of the CAN bus.

Before running the example, identify the PCP addresses of your actuators and replace the example addresses below with the actual values used in your setup.

!!! warning
    Make sure the actuators can move freely and safely before starting the example.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the CAN to USB adapter is connected,
- the CAN bus is wired correctly and terminated,
- the actuators are powered and reachable on the bus,
- the user has permission to access the communication device.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <atomic>
#include <chrono>
#include <csignal>
#include <iomanip>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;
```

## Connect to the adapter

Create a list with the addresses of the actuators you want to control, then create one `PCP_over_USB` adapter and reuse it for all actuators on the bus.

```cpp
std::vector<int> actuator_addresses = {0x10, 0x11};  // Replace with your actual addresses

std::string port = PCP_over_USB::get_port();
// std::string port = "COM1";

std::cout << "Connecting to " << port << std::endl;
PCP_over_USB adapter(port);
```

## Define the feedback callback

In this example, the callback prints the reported position of each actuator.

```cpp
void actuator_feedback(
    int address,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    auto it = feedback.find(PulsarActuator::PCP_Items::POSITION_FB);

    if (it != feedback.end()) {
        std::cout << "Actuator 0x"
                  << std::hex << std::uppercase << address
                  << std::dec
                  << " position: "
                  << std::fixed << std::setprecision(2)
                  << it->second
                  << " rad"
                  << std::endl;
    }
}
```

## Initialize actuators and apply common configuration

Create each actuator from the same adapter, connect it, configure the feedback items and rate, switch it to `SPEED` mode, and register the feedback callback.

Use smart pointers to store the actuators, since `PulsarActuator` is not intended to be copied.

```cpp
std::vector<std::unique_ptr<PulsarActuator>> actuators;
actuators.reserve(actuator_addresses.size());

for (int address : actuator_addresses) {
    auto actuator = std::make_unique<PulsarActuator>(adapter, address);

    if (!actuator->connect()) {
        std::cerr << "Could not connect to actuator 0x"
                  << std::hex << std::uppercase << address
                  << std::dec << std::endl;

        for (auto& connected_actuator : actuators) {
            connected_actuator->disconnect();
        }
        adapter.close();
        throw std::runtime_error("Actuator connection failed");
    }

    std::cout << "Connected to actuator 0x"
              << std::hex << std::uppercase << address
              << std::dec
              << " (model: " << actuator->model()
              << ", firmware: " << actuator->firmware_version()
              << ")"
              << std::endl;

    actuator->setFeedbackItems({
        PulsarActuator::PCP_Items::POSITION_FB,
    });

    actuator->setFeedbackRate(PulsarActuator::Rates::RATE_10HZ);
    actuator->change_mode(PulsarActuator::Mode::SPEED);
    actuator->set_feedback_callback(actuator_feedback);

    actuators.push_back(std::move(actuator));
}
```

## Configure each actuator

Once the actuators are initialized, assign the desired setpoint to each one.

```cpp
if (actuators.size() >= 1) {
    actuators[0]->change_setpoint(0.2f);  // rad/s
}

if (actuators.size() >= 2) {
    actuators[1]->change_setpoint(0.3f);  // rad/s
}
```

Adjust the setpoints and the number of actuators to match your setup.

## Run the actuators

Start all actuators and keep the application alive until the user presses `Ctrl+C`.

```cpp
std::atomic<bool> keep_running{true};

extern "C" void stop_actuators_handler(int)
{
    keep_running = false;
}

std::signal(SIGINT, stop_actuators_handler);

for (auto& actuator : actuators) {
    actuator->start();
}

std::cout << "Actuators started. Press Ctrl+C to stop." << std::endl;

while (keep_running) {
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}
```

## Stop and clean up

When the loop finishes, disconnect all actuators and close the adapter.

```cpp
for (auto& actuator : actuators) {
    actuator->disconnect();
}

std::this_thread::sleep_for(std::chrono::milliseconds(100));
adapter.close();
```

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <atomic>
#include <chrono>
#include <csignal>
#include <iomanip>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;

std::atomic<bool> keep_running{true};

void actuator_feedback(
    int address,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    auto it = feedback.find(PulsarActuator::PCP_Items::POSITION_FB);

    if (it != feedback.end()) {
        std::cout << "Actuator 0x"
                  << std::hex << std::uppercase << address
                  << std::dec
                  << " position: "
                  << std::fixed << std::setprecision(2)
                  << it->second
                  << " rad"
                  << std::endl;
    }
}

extern "C" void stop_actuators_handler(int)
{
    keep_running = false;
}

int main()
{
    PCP_over_USB* adapter_ptr = nullptr;

    try {
        std::vector<int> actuator_addresses = {0x10, 0x11};  // Replace with your actual addresses

        std::string port = PCP_over_USB::get_port();
        // std::string port = "COM1";

        std::cout << "Connecting to " << port << std::endl;
        PCP_over_USB adapter(port);
        adapter_ptr = &adapter;

        std::vector<std::unique_ptr<PulsarActuator>> actuators;
        actuators.reserve(actuator_addresses.size());

        for (int address : actuator_addresses) {
            auto actuator = std::make_unique<PulsarActuator>(adapter, address);

            if (!actuator->connect()) {
                std::cerr << "Could not connect to actuator 0x"
                          << std::hex << std::uppercase << address
                          << std::dec << std::endl;

                for (auto& connected_actuator : actuators) {
                    try {
                        connected_actuator->disconnect();
                    } catch (...) {
                    }
                }

                adapter.close();
                return 1;
            }

            std::cout << "Connected to actuator 0x"
                      << std::hex << std::uppercase << address
                      << std::dec
                      << " (model: " << actuator->model()
                      << ", firmware: " << actuator->firmware_version()
                      << ")"
                      << std::endl;

            actuator->setFeedbackItems({
                PulsarActuator::PCP_Items::POSITION_FB,
            });

            actuator->setFeedbackRate(PulsarActuator::Rates::RATE_10HZ);
            actuator->change_mode(PulsarActuator::Mode::SPEED);
            actuator->set_feedback_callback(actuator_feedback);

            actuators.push_back(std::move(actuator));
        }

        if (actuators.size() >= 1) {
            actuators[0]->change_setpoint(0.2f);  // rad/s
        }

        if (actuators.size() >= 2) {
            actuators[1]->change_setpoint(0.3f);  // rad/s
        }

        std::signal(SIGINT, stop_actuators_handler);

        for (auto& actuator : actuators) {
            actuator->start();
        }

        std::cout << "Actuators started. Press Ctrl+C to stop." << std::endl;

        while (keep_running) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        for (auto& actuator : actuators) {
            actuator->disconnect();
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        adapter.close();
    }
    catch (const std::exception& e) {
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