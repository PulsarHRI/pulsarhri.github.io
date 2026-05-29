# Quickstart Tutorial: Python API for a Virtual Actuator with DTwin

This page outlines the fastest path to running a virtual actuator through the PULSAR HRI Python API and AUGUR Digital Twin (DTwin) assets.

Virtual actuators are intended for software-side testing and tutorials. They do not require a powered actuator, USB cable, CAN adapter, or CAN bus wiring.

## What You'll Need

- Python API 2.0.0 installed as described in [Install Python API](../control/python_api/install_python_api.md).
- DTwin assets installed as described in [Download AUGUR Digital Twin Assets](../download/download_dtwin.md). The first beta asset release is available for Linux x86_64 and Windows x86_64.
- The public examples repository described in [Python API Examples](../control/python_api/examples.md).

## Step-by-Step Guide

1. Install the Python API in a project environment. Pixi is recommended for new projects.
2. Install the DTwin asset package required by the virtual actuator example you want to run.
3. Follow the examples repository README to launch the virtual actuator examples.
4. Use the [`PulsarActuatorVirtual`](../control/python_api/class_PulsarActuatorVirtual.md) API reference when adapting an example into your own code.

The virtual API follows the same control-mode structure as `PulsarActuatorReal`, with virtual-only methods for selecting DTwin assets and advancing simulation steps.

!!! note
    The current public DTwin package is a first beta release for Linux x86_64 and Windows x86_64. It includes generated assets for `P100`, `P90`, `PULSE115`, and `PULSE98`; check the download manifest for future versions and platforms.
