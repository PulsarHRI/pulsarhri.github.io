# Python API Examples

Runnable Python examples live in the public examples repository:

```text
https://github.com/PulsarHRI/pcp_api_python_examples
```

The examples repository is versioned separately from the Python API package so tutorials can be updated without requiring a new API wheel release.

It contains:

- lightweight quickstart examples for real hardware;
- deeper tutorials for broader functionality and realistic use cases;
- DTwin and virtual actuator examples.
- robot-level examples using robot model assets.

## Repository README

Follow the [examples repository README](https://github.com/PulsarHRI/pcp_api_python_examples#readme) for the current setup and run instructions. It covers the required tools, including Pixi, and gets you from clone to running examples in a handful of commands.

Virtual and robot-level examples require generated assets. A first DTwin beta asset release is available for Linux x86_64 and Windows x86_64, covering `P100`, `P90`, `PULSE115`, and `PULSE98`; robot model asset releases include the Single Link 1DOF and Pulse Arm 4DOF models. The examples repository README describes the current installer workflow, while the [AUGUR Digital Twin download page](../../download/download_dtwin.md) and [Robot Model Assets download page](../../download/download_robot_assets.md) list the published packages and manifests.
