# Install Pulsar Python SDK

Pixi is the recommended installation method because it pins Python and native packages per project.

## Pixi

Create a project and add the public Pulsar channel:

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

Run Python or the CLI through Pixi:

```bash
pixi run python -c "import pulsar_sdk; print('Pulsar Python SDK installed')"
pixi run pulsar-cli --help
```

The public channel does not require authentication.

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

AUGUR Digital Twin assets are distributed separately as `pulsar-assets`; Pixi is the recommended complete virtual-actuator setup.

## Verify hardware compatibility

Physical actuators require firmware **2.0.4 or newer**. If an older actuator needs an update, [contact support](../support.md).

## Next steps

- [Single actuator with Pulsar Python SDK](../quickstart/sdk_usb.md)
- [Virtual actuator with Pulsar Python SDK](../quickstart/sdk_virtual.md)
- [Core workflow](core_workflow.md)
