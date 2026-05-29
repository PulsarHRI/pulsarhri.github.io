# Set Up Virtual Actuators

Virtual actuators are configured in software using AUGUR Digital Twin (DTwin) assets and the PULSAR HRI Python API. They let you run actuator-control examples without connecting physical hardware. The first public DTwin beta asset release is available for Linux x86_64 and Windows x86_64.

To set up a virtual actuator workflow:

1. Install Python API 2.0.0 as described in [Install Python API](../control/python_api/install_python_api.md).
2. Install the required DTwin assets as described in [Download AUGUR Digital Twin Assets](../download/download_dtwin.md).
3. Follow the [Python API for Virtual Actuator with DTwin](../quickstarts/quickstart_virtual_python_api.md) quickstart.

!!! note
    The current public DTwin package is a first beta release for Linux x86_64 and Windows x86_64. It includes generated assets for `P100`, `P90`, `PULSE115`, and `PULSE98`; check the download manifest for future versions and platforms.
