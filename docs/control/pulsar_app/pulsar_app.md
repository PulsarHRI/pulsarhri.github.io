# PULSAR App: No-Code GUI

!!! note
    Currently, the PULSAR App works only with real actuators, not with virtual actuators.

The **PULSAR App** is the no-code GUI for connecting to, configuring, controlling, and monitoring a PULSAR actuator. It is available in two forms:

- > **Browser app**: open [https://app.pulsarhri.com/](https://app.pulsarhri.com/)
- **Desktop app**: download and launch the installable desktop package

Both forms provide the same guided interface, so the quickstart workflow applies whether you launch it from the browser or from the desktop package.

This tool is ideal for:
- **Quick testing** and tuning actuator parameters
- **Visualizing data** such as position, speed, and torque
- **Running diagnostics** without using scripts

### ⚙️ System Requirements

- **Connection**: The actuator must be **powered on** and connected through a supported communication path. The no-code quickstart uses a direct USB connection.
- **Browser app**: Requires browser permission to access the connected device. Tested on Linux and Windows. Chrome or Chromium-based browsers are recommended; Firefox may have issues.
- **Desktop app compatibility**: Tested on **Windows**.

At this stage, the app supports controlling **one actuator at a time**.

### 📦 How to Launch the App

- Use the [browser app](https://app.pulsarhri.com/) for the fastest start.
- Download the desktop package [here](../../download/download_app.md).


### 🚀 Key Features

- Browse and connect to available actuators.
- Switch between control modes: Speed, Position, Torque, and Impedance.
- Change control parameters (e.g., position Kp, torque limits).
- View real-time plots of actuator feedback.
- Run basic motion sequences interactively.

### 🔍 Learn by Doing

To walk through your first experience with the app, check out the [Quickstart Guide](../../quickstarts/quickstart_pulsar_app.md).
It covers:
- Powering and connecting your actuator.
- Using the GUI to change control modes and parameters.
- Safety tips for live testing.
- Interacting with the actuator in real-time.

### 🖼 Interface Preview

![PULSAR App GUI](../../assets/images/GUI_01.png)
