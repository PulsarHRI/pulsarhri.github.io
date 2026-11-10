# Contributing

Thank you for helping improve the PulsarHRI Developer Hub.

The site uses MkDocs with the Material theme. Current source pages live under `docs/`, navigation is configured in `mkdocs.yml`, and published versions are managed with `mike`.

## Local preview

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Preview only the current source version:

```bash
python -m mkdocs serve
# or
pixi run serve
```

Open `http://127.0.0.1:8000`. A plain MkDocs preview does not contain Mike's `versions.json`, so it intentionally does not show the version selector.

## Validation

Before submitting changes, run:

```bash
python -m mkdocs build --strict
```

The build must complete without warnings.

## Versioned preview

Prepare both versions in the local `gh-pages` branch and start Mike:

```bash
pixi run serve-versions
```

Without Pixi, run:

```bash
python tools/prepare_versioned_docs.py
mike serve
```

Open the URL printed by Mike. The header then shows a selector for `2.0.4` and `3.0.0`.

The preparation script rebuilds the current working tree as `3.0.0` and bootstraps `2.0.4` from its preserved Git commit when needed. It does not push. Normal contributors should not run `mike deploy --push`; GitHub Actions handles publication.

## SDK reference updates

The public SDK contract, API reference, and diagrams are currently copied manually from the private SDK source. For every SDK release:

1. compare the public surface and behavior contract;
2. update `docs/sdk/user_contract.md`;
3. update `docs/sdk/api_reference.md`;
4. replace diagrams under `docs/sdk/assets/diagrams/` when changed;
5. update task guides and examples affected by behavior changes;
6. run the strict build and search for stale names or versions.

Do not publish private repository URLs, source paths, credentials, testing channels, or hidden engineering APIs.

## Writing guidelines

- Write for public users.
- Use `PulsarHRI`, `Pulsar App`, `Pulsar SDK`, `AUGUR Digital Twin`, and uppercase `PULSE` model names.
- Keep real-hardware instructions safe and include shutdown behavior.
- Prefer stable public links.
- Keep current and legacy documentation concerns separate.
- Avoid unrelated formatting churn.
