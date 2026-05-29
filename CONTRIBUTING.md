# Contributing

Thank you for helping improve the PULSAR HRI documentation.

This repository uses [MkDocs](https://www.mkdocs.org/) with the Material theme.
Documentation source files live under `docs/`, and navigation is configured in
`mkdocs.yml`.

## Local Preview

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

Install the documentation dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the live preview server:

```bash
python -m mkdocs serve
```

Open:

```text
http://127.0.0.1:8000
```

Stop the server with `Ctrl+C`.

## Validation

Before submitting changes, run:

```bash
python -m mkdocs build --strict
```

Running MkDocs through `python -m` ensures the command uses the active virtual
environment instead of a stale global executable. The build should complete
successfully.

## Writing Guidelines

- Write for public users.
- Keep instructions safe for real hardware.
- Prefer links to stable public resources.
- Do not include private company links, credentials, or internal-only details.
- Keep changes focused and avoid unrelated formatting churn.
