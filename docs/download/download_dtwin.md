# Download AUGUR Digital Twin

AUGUR DTwin asset packages provide the generated shared libraries and Python bindings needed to run PULSAR HRI virtual actuator examples.

## Temporary test package

The current public package is a dummy release used to validate the download workflow before publishing real generated DTwin assets. It contains placeholder files only and cannot run a real virtual actuator model.

- Latest test version: `20260213-test`
- Models: `DUMMY`
- Manifest: [`dtwin_assets_manifest.json`](dtwin_assets_manifest.json)
- Archive: [`pulsar-dtwin-assets-20260213-test.zip`](dtwin_assets/pulsar-dtwin-assets-20260213-test.zip)

From the Python API repository, install the package with:

```bash
pixi run -e examples install-dtwin-assets --version 20260213-test
```

Once real DTwin packages are published, this page will keep the newest compatible release at the top while preserving older versions for compatibility checks.

For support, [contact our team](../support.md).
