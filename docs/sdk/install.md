Pulsar Python SDK
{ .pulsar-home-eyebrow }

# Install Pulsar Python SDK

[Pixi](https://pixi.prefix.dev/latest/installation/) is the recommended package and environment manager for Pulsar SDK projects. It installs Python and native dependencies together, pins them per project, and provides the same project commands on Linux and Windows.

## Install [Pixi](https://pixi.prefix.dev/latest/installation/)

=== "Linux"

    ```bash
    curl -fsSL https://pixi.sh/install.sh | sh
    ```

=== "Windows PowerShell"

    ```powershell
    powershell -ExecutionPolicy Bypass -c "irm -useb https://pixi.sh/install.ps1 | iex"
    ```

Restart the terminal after installation, then create a project and add the public Pulsar channel:

```bash
pixi init my-pulsar-project
cd my-pulsar-project
pixi workspace channel add --prepend https://prefix.dev/pulsarhri/pulsar-forge
pixi add pulsar-sdk
```

For virtual actuators, install the model assets too:

```bash
pixi add pulsar-assets
```

Run Python or the CLI through [Pixi](https://pixi.prefix.dev/latest/installation/):

```bash
pixi run python -c "import pulsar_sdk; print('Pulsar Python SDK installed')"
pixi run pulsar-cli --help
```

The public channel does not require authentication. The project commands above are identical on Linux and Windows.

## pip and venv

For physical-actuator projects that use a conventional Python environment:

=== "Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pulsar-sdk
    ```

=== "Windows PowerShell"

    ```powershell
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pulsar-sdk
    ```

AUGUR Digital Twin assets are distributed separately as `pulsar-assets`; [Pixi](https://pixi.prefix.dev/latest/installation/) is the recommended complete virtual-actuator setup.

## Verify hardware compatibility

Physical actuators require firmware **2.0.4 or newer**. If an older actuator needs an update, visit the [Firmware page](../firmware/index.md).

## Next steps

- [Physical actuator over direct USB with Pulsar Python SDK](../quickstart/sdk_usb.md)
- [Virtual actuator with Pulsar Python SDK](../quickstart/sdk_virtual.md)
- [Core concepts and workflow](core_workflow.md)
