<h1 class="pulsar-visually-hidden">PULSAR HRI Ecosystem Documentation</h1>

<p align="center">
  <img class="pulsar-theme-logo pulsar-theme-logo--light" src="assets/images/pulsarhri_logo_black.png" alt="PULSAR HRI">
  <img class="pulsar-theme-logo pulsar-theme-logo--dark" src="assets/images/pulsarhri_logo_white.png" alt="PULSAR HRI">
</p>

Welcome to the **[PULSAR HRI](https://pulsarhri.com/) Ecosystem Documentation**!

Whether you're a researcher, developer, or engineer, the content on this website will help you get up and running with PULSAR products. 
PULSAR HRI develops best-in-class actuation systems and a surrounding ecosystem to enable next-generation robotics.

### ⚡ First Time Here?

If you can't wait to see your actuator moving, just go straight to the [**No-Code GUI Quickstart**](quickstarts/quickstart_pulsar_app.md) to set up, power your actuator and get moving in minutes controlling it directly from your browser!

!!! tip
    Make sure to read the following short section: it will allow you to easily find what you need on the website.

## 🧭 Ecosystem Overview

At a glance, these are the main elements of the PULSAR HRI ecosystem:

<p align="center">
  <img src="/assets/images/high_level_diagram_ecosystem_black_no_logo.png" alt="High-level ecosystem diagram" width="80%">
</p>

- **REAL ACTUATORS** which, once [set up](set_up/set_up_real.md), offer the following [hardware communication interfaces](communicate/communicate_real.md): 
    - Direct **USB** connection, to connect to a single actuator for quick tests and firmware updates.
    - **CAN** communication (CAN FD at selectable 1 or 5 MBps), to connect to multiple actuators in robotic systems.
<br><br>
- **VIRTUAL ACTUATORS** closely matching their real counterparts' behavior. These virtual actuators can be set up through:
    - [**AUGUR Digital Twin (DTwin)**](set_up/set_up_virtual.md): a first beta release is available for Linux x86_64. It models the physics of the real actuator and runs the exact same control algorithms.
<br><br>
- **CONTROL INTERFACES** of different kinds and for different needs, used to control both real and virtual actuators:
    - [**PULSAR App GUI**](control/pulsar_app/pulsar_app.md): A no-code GUI for single-actuator testing, available in the browser or as a desktop package
        - offering [the easiest quickstart experience](quickstarts/quickstart_pulsar_app.md) to get familiar with PULSAR HRI actuators and their control.
    - [**Python API**](control/python_api/install_python_api.md): A flexible way to control real and virtual actuators from Python, from quick experiments to multi-actuator workflows at high update rates, both for Real and AUGUR-powered Virtual Actuators
        - with several [example quickstart and in-depth tutorials as jupyter notebooks](control/python_api/examples.md)
    - [**C++ API**](control/cpp_api/install_cpp_api.md): A lower-level option for more demanding and real-time applications.

!!! note
    A quick alignment on naming we use:
    
    - **Motors** = Direct-drive units without a transmission.
    - **Actuators** = Motors with an integrated transmission.

A question we often hear is: 
>*"How are you different from other actuator companies?"*

Glad you asked. Check out [PULSAR HRI's website](https://pulsarhri.com/technology/) for answers!

---

### 🆘 Need help? 
Visit our [Support page](support.md) or check the [FAQ](faq.md).

---
![Actuator to digital twin transition](assets/images/actuators_digital_twin_transition_5loops.gif){ loading=lazy }
