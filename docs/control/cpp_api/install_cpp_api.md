# Install C++ API

This guide walks you through the installation of the PULSAR HRI C++ API, which allows you to programmatically control and interact with PULSAR actuators from C++ applications.

The C++ API is distributed as a prebuilt SDK containing:

- C++ headers,
- a compiled shared library,
- CMake package files,
- examples,
- and the `pulsar-cli` command-line tool.

The current release targets Linux x86_64 systems, mainly Ubuntu/Debian.

---

## Available Packages

PULSAR HRI provides the C++ API in two Linux package formats:

```text
pcp-api-cpp-<version>-linux-x86_64.deb
pcp-api-cpp-<version>-linux-x86_64.tar.gz
```

Use the `.deb` package if you are using Ubuntu or Debian.

Use the `.tar.gz` archive if you want a manual installation in a custom location, such as `/opt/pcp_api`.

---

## Requirements

The C++ API currently targets Linux x86_64 systems.

### Runtime dependency

The C++ API requires `libserialport` for serial communication.

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install libserialport0
```

### Build tools

If you plan to build examples or your own C++ applications, install:

```bash
sudo apt update
sudo apt install build-essential cmake
```

### Serial device permissions

You may need permission to access the USB-CAN adapter device.

On Ubuntu/Debian systems, add your user to the `dialout` group:

```bash
sudo usermod -aG dialout $USER
```

Then log out and log back in.

You can verify your groups with:

```bash
groups
```

You can check the USB device permissions with:

```bash
ls -l /dev/ttyACM0
```

---

# Option 1: Installation from `.deb`

For Ubuntu/Debian systems, the recommended installation method is the Debian package.

Download:

```text
pcp-api-cpp-<version>-linux-x86_64.deb
```

Install it with:

```bash
sudo apt install ./pcp-api-cpp-<version>-linux-x86_64.deb
```

---

# Option 2: Installation from `.tar.gz`

Use this method if you want to install the SDK manually into a custom folder.

Download:

```text
pcp-api-cpp-<version>-linux-x86_64.tar.gz
```

Extract it to a location of your choice. For a system-like local installation, `/opt/pcp_api` is recommended:

```bash
sudo mkdir -p /opt/pcp_api
sudo tar -xzf pcp-api-cpp-<version>-linux-x86_64.tar.gz -C /opt/pcp_api
```

The extracted SDK should contain a structure similar to:

```text
/opt/pcp_api/
├── include/
│   └── pcp_api/
├── lib/
│   ├── libpcp_api.so
│   └── cmake/pcp_api/
├── bin/
│   └── pulsar-cli
└── share/
    └── pcp_api/
```

---

## Using the C++ API in Your Project

The SDK provides a CMake package, so the recommended way to use it is through `find_package`.

Create a `CMakeLists.txt` file:

```cmake
cmake_minimum_required(VERSION 3.16)
project(my_pulsar_app LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pcp_api CONFIG REQUIRED)

add_executable(my_pulsar_app main.cpp)
target_link_libraries(my_pulsar_app PRIVATE pcp_api::pcp_api)
```

Create a simple `main.cpp`:

```cpp
#include <iostream>
#include <pcp_api/pcp_api.hpp>

int main() {
    auto ports = pcp_api::PCP_over_USB::get_ports();

    std::cout << "Detected ports: " << ports.size() << std::endl;
    for (const auto& port : ports) {
        std::cout << "  " << port << std::endl;
    }

    return 0;
}
```

---

## Building When Installed from `.deb`

If the API was installed using the `.deb` package, CMake should find it automatically:

```bash
cmake -S . -B build
cmake --build build
```

Run:

```bash
./build/my_pulsar_app
```

---

## Building When Installed from `.tar.gz`

If the SDK was extracted manually, pass the SDK path to CMake:

```bash
cmake -S . -B build -DCMAKE_PREFIX_PATH=/opt/pcp_api
cmake --build build
```

Run:

```bash
LD_LIBRARY_PATH=/opt/pcp_api/lib:$LD_LIBRARY_PATH ./build/my_pulsar_app
```

---

## Runtime Library Path

If you installed the SDK from the `.tar.gz` archive, Linux may need help finding `libpcp_api.so` at runtime.

For temporary use:

```bash
export LD_LIBRARY_PATH=/opt/pcp_api/lib:$LD_LIBRARY_PATH
```

To make this permanent for your shell, add the line above to your `~/.bashrc` or equivalent shell configuration file.

If you installed the API using the `.deb`, you normally do not need to set `LD_LIBRARY_PATH`.

---

## Checking Package Integrity

If a `SHA256SUMS` file is provided, verify the downloaded files:

```bash
sha256sum -c SHA256SUMS
```

Run this command in the same folder as the downloaded package files.

---

## Uninstalling

### If installed from `.deb`

```bash
sudo apt remove pcp-api-cpp
```

To remove configuration files as well, if any:

```bash
sudo apt purge pcp-api-cpp
```

### If installed from `.tar.gz`

Remove the installation folder:

```bash
sudo rm -rf /opt/pcp_api
```

If you added `LD_LIBRARY_PATH` to your shell configuration, remove that line from `~/.bashrc` or equivalent.

---

## Troubleshooting

### `libpcp_api.so: cannot open shared object file`

The dynamic library cannot be found at runtime.

If you installed from `.tar.gz`, set:

```bash
export LD_LIBRARY_PATH=/opt/pcp_api/lib:$LD_LIBRARY_PATH
```

Then rerun your application.

If you installed from `.deb`, run:

```bash
sudo ldconfig
```

---

### `SerialPort: failed to open port /dev/ttyACM0`

Your user may not have permission to access the USB serial device.

Add your user to the `dialout` group:

```bash
sudo usermod -aG dialout $USER
```

Then log out and log back in.

Check the device permissions:

```bash
ls -l /dev/ttyACM0
```

---

### `libserialport.so` not found

Install the runtime serial communication library:

```bash
sudo apt update
sudo apt install libserialport0
```

For development from source, install:

```bash
sudo apt install libserialport-dev
```

---

### CMake cannot find `pcp_api`

If installed from `.tar.gz`, make sure you pass the SDK path:

```bash
cmake -S . -B build -DCMAKE_PREFIX_PATH=/opt/pcp_api
```

Check that the CMake package files exist:

```bash
ls /opt/pcp_api/lib/cmake/pcp_api
```

If installed from `.deb`, check:

```bash
dpkg -L pcp-api-cpp | grep cmake
```

---

### `pulsar-cli: command not found`

If installed from `.deb`, check:

```bash
dpkg -L pcp-api-cpp | grep pulsar-cli
```

If installed from `.tar.gz`, call the CLI using its full path:

```bash
/opt/pcp_api/bin/pulsar-cli --help
```

or add it to your `PATH`:

```bash
export PATH=/opt/pcp_api/bin:$PATH
```

---

## Next Steps

Once the C++ API is installed, you can:

- Use the [command-line interface](cli.md) to quickly interact with PULSAR hardware.
- Build and test the [provided examples](example_single_actuator.md).
- Integrate the C++ API into your own CMake projects.
- Use the generated headers under `include/pcp_api/` as the main API reference.
- Contact the [PULSAR HRI support team](../../support.md) if you encounter installation or hardware communication issues.