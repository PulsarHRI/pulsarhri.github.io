# Install Python API

This guide walks you through the installation of the PULSAR HRI Python API, which allows you to programmatically control and interact with PULSAR actuators.

This section targets Python API 2.0.0.


## Installation

The Python package is published on PyPI as `pcp-api` and imported in Python as `pcp_api`.

For new projects, use [Pixi](https://pixi.prefix.dev/dev/). It keeps the Python version and dependencies pinned per project, which makes examples and shared research code easier to reproduce.

```bash
pixi init pulsar-api-demo
cd pulsar-api-demo
pixi add python
pixi add --pypi pcp-api
```

You can then run Python inside the Pixi environment:

```bash
pixi run python -c "import pcp_api; print('pcp_api installed')"
```

If you are already using a Python virtual environment, `venv`, `pipenv`, `poetry`, or `uv` are also valid options. With `venv` and `pip`, install the package with:

```bash
python -m pip install --upgrade pcp-api
```


## Verifying the Installation

To confirm that the installation was successful, run the following command:

```bash
python -m pip show pcp-api
```

If you installed with Pixi, run the same check inside the Pixi environment:

```bash
pixi run python -m pip show pcp-api
```

These commands should display information about the installed package, including its version and location. If you see this information, the installation was successful.

## Next Steps

Once the API is installed, you can:

* Use the [command-line interface](cli.md) to quickly interact with PULSAR hardware.
* Run the [public Python examples](examples.md).
* Explore the [code documentation](class_PulsarActuatorReal.md) for detailed usage instructions.
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an [issue](https://github.com/PulsarHRI/pulsarhri.github.io/issues).
