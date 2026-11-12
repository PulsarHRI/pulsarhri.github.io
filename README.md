# PULSAR HRI Developer Hub

This repository contains the public [PULSAR HRI Developer Hub](https://pulsarhri.github.io/).

The current documentation covers:

- PULSE actuator hardware, setup, USB, and CAN FD;
- Pulsar App browser and desktop workflows;
- Pulsar Python SDK for physical and virtual actuators;
- AUGUR Digital Twin and co-simulation;
- actuator control architectures;
- CAD, datasheets, support, and known issues.

## Documentation versions

The published site uses `mike` to keep both documentation generations available:

- `3.0.0` — current Developer Hub and Pulsar Python SDK documentation;
- `2.0.4` — preserved legacy API documentation and downloads.

Use the version selector in the site header to switch versions.

## Serve locally with Pixi

Install the locked documentation environment:

```bash
pixi install
```

### Preview only the current source

```bash
pixi run serve
```

Open `http://127.0.0.1:8000`. This uses plain MkDocs and intentionally does **not** show the documentation-version selector.

### Preview both documentation versions

```bash
pixi run serve-versions
```

This prepares `2.0.4` and `3.0.0` in the local `gh-pages` branch, starts Mike, and prints the local URL. Open that URL to use the version selector in the site header.

The preparation step is local only and does not push `gh-pages`.

### Validate the site

```bash
pixi run build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for virtual-environment commands and publication details.
