# Logging Actuator Data to CSV

This tutorial shows how to log data from a PULSAR HRI actuator to a CSV file for later analysis. It covers how to connect to the actuator, select the feedback items to record, write samples to a CSV file, and stop the session cleanly.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the actuator is connected and reachable,
- the user has permission to access the communication device,
- the output directory is writable.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;
```

## Connect to the adapter and actuator

Most of the setup is shared with the other examples. The code below initializes the adapter and connects to one actuator.

```cpp
std::string port = PCP_over_USB::get_port();
// std::string port = "COM1";

std::cout << "Connecting to " << port << std::endl;
PCP_over_USB adapter(port);
PulsarActuator actuator(adapter, 0);

if (!actuator.connect()) {
    std::cerr << "Could not connect to the actuator "
              << actuator.address()
              << std::endl;
    adapter.close();
    throw std::runtime_error("Actuator connection failed");
}

std::cout << "Connected to the actuator "
          << actuator.address()
          << " (model: "
          << actuator.model()
          << ", firmware: "
          << actuator.firmware_version()
          << ")"
          << std::endl;
```

## Select the items to log

Choose the feedback items you want to save to the CSV file. In this example, the current in the three motor phases is logged.

```cpp
std::vector<PulsarActuator::PCP_Items> items_to_log = {
    PulsarActuator::PCP_Items::IA,
    PulsarActuator::PCP_Items::IB,
    PulsarActuator::PCP_Items::IC,
};
```

## Prepare CSV logging

Open the CSV file and write the header. Keep the column order consistent with the order used when writing feedback samples. 

```cpp
std::ofstream csv_file("log.csv");
if (!csv_file.is_open()) {
    actuator.disconnect();
    adapter.close();
    throw std::runtime_error("Could not open log.csv for writing");
}

csv_file << "Timestamp";
for (const auto item : items_to_log) {
    csv_file << ',' << item_name(item);
}
csv_file << '\n';
```

## Define the feedback callback

The callback writes one CSV row for each feedback sample.

```cpp
std::ofstream* csv_output = &csv_file;
auto* selected_items = &items_to_log;

auto actuator_feedback = [csv_output, selected_items](
    int /* address */,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    using clock = std::chrono::system_clock;
    const auto now = clock::now();
    const auto timestamp =
        std::chrono::duration<double>(now.time_since_epoch()).count();

    (*csv_output) << timestamp;
    for (const auto item : *selected_items) {
        (*csv_output) << ',' << feedback.at(item);
    }
    (*csv_output) << '\n';
};
```

This callback uses the same item order as the CSV header, so the logged columns always stay aligned with the selected feedback items.

## Configure the feedback rate

Configure the feedback items and request high-frequency feedback at `1 kHz`.

```cpp
actuator.setFeedbackItems(items_to_log);
actuator.setFeedbackRate(PulsarActuator::Rates::RATE_1KHZ);
```

## Start the actuator and log data

This example runs the actuator in `SPEED` mode for `3` seconds, stores the feedback in `log.csv`, and then closes the session cleanly.

```cpp
actuator.change_mode(PulsarActuator::Mode::SPEED);
actuator.change_setpoint(1.0f);  // rad/s
actuator.set_feedback_callback(actuator_feedback);
actuator.start();

std::this_thread::sleep_for(std::chrono::seconds(3));

actuator.disconnect();
std::this_thread::sleep_for(std::chrono::milliseconds(100));
adapter.close();
csv_file.close();
```

## Example output

This code generates a CSV file named `log.csv` with the logged data. The first column is the timestamp, and the following columns are the actuator values.

| Timestamp | IA | IB | IC |
|-----------|----|----|----|
| 1642780800.123 | 0.15 | -0.08 | 0.12 |
| 1642780800.124 | 0.16 | -0.09 | 0.13 |
| 1642780800.125 | 0.17 | -0.10 | 0.14 |

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;

std::string item_name(PulsarActuator::PCP_Items item)
{
    switch (item) {
        case PulsarActuator::PCP_Items::IA: return "IA";
        case PulsarActuator::PCP_Items::IB: return "IB";
        case PulsarActuator::PCP_Items::IC: return "IC";
        default: return "UNKNOWN";
    }
}

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

        PulsarActuator actuator(adapter, 0);
        actuator_ptr = &actuator;

        if (!actuator.connect()) {
            std::cerr << "Could not connect to the actuator "
                      << actuator.address()
                      << std::endl;
            adapter.close();
            return 1;
        }

        std::cout << "Connected to the actuator "
                  << actuator.address()
                  << " (model: "
                  << actuator.model()
                  << ", firmware: "
                  << actuator.firmware_version()
                  << ")"
                  << std::endl;

        std::vector<PulsarActuator::PCP_Items> items_to_log = {
            PulsarActuator::PCP_Items::IA,
            PulsarActuator::PCP_Items::IB,
            PulsarActuator::PCP_Items::IC,
        };

        std::ofstream csv_file("log.csv");
        if (!csv_file.is_open()) {
            actuator.disconnect();
            adapter.close();
            std::cerr << "Could not open log.csv for writing" << std::endl;
            return 1;
        }

        csv_file << "Timestamp";
        for (const auto item : items_to_log) {
            csv_file << ',' << item_name(item);
        }
        csv_file << '\n';

        std::ofstream* csv_output = &csv_file;
        auto* selected_items = &items_to_log;

        auto actuator_feedback = [csv_output, selected_items](
            int /* address */,
            const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
        {
            using clock = std::chrono::system_clock;
            const auto now = clock::now();
            const auto timestamp =
                std::chrono::duration<double>(now.time_since_epoch()).count();

            (*csv_output) << timestamp;
            for (const auto item : *selected_items) {
                (*csv_output) << ',' << feedback.at(item);
            }
            (*csv_output) << '\n';
        };

        actuator.setFeedbackItems(items_to_log);
        actuator.setFeedbackRate(PulsarActuator::Rates::RATE_1KHZ);

        actuator.change_mode(PulsarActuator::Mode::SPEED);
        actuator.change_setpoint(1.0f);  // rad/s
        actuator.set_feedback_callback(actuator_feedback);
        actuator.start();

        std::this_thread::sleep_for(std::chrono::seconds(3));

        actuator.disconnect();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        adapter.close();
        csv_file.close();

        std::cout << "Log saved to: "
                  << std::filesystem::absolute("log.csv")
                  << std::endl;
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