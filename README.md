**# PULSAR HRI Ecosystem Documentation website**

The content of this Repo gets published in the [PULSAR HRI Ecosystem Documentation website](https://pulsarhri.github.io).

Related Confluence Space [HERE](https://arquimeagroup.atlassian.net/wiki/spaces/HU/pages/2626453638/PULSAR+Ecosystem+Documentation)

## 📘 Local Preview: Editing and Visualizing the Documentation

To preview and edit the PULSAR documentation locally in your browser:

### ✅ 1. Create a virtual environment (recommended)

You can install the Python dependencies globally, but it is **highly recommended** to use a virtual environment to avoid polluting your system Python.

If you choose to install globally:

```bash
pip install -r requirements.txt
```

If you prefer a virtual environment (recommended), make sure `venv` is installed:

* **Ubuntu**:

  ```bash
  sudo apt update
  sudo apt install python3-venv
  ```
* **Windows**:
  Usually comes with Python. If not, install Python from [https://www.python.org](https://www.python.org) and ensure you check the box "Add Python to PATH" during installation.

Then, from the root of the repo:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

---

### ✅ 2. Install dependencies

Once the virtual environment is active, install the required packages:

```bash
pip install -r requirements.txt
```

---

### ✅ 3. Start the local server

From the root of the repository (where `mkdocs.yml` is located), run:

```bash
mkdocs serve
```

This will start a live-reloading dev server at:

```
http://127.0.0.1:8000
```

Visit that address in your browser to view the documentation.

As you edit `.md` files under `docs/`, the page will update automatically.

---

### ❌ To stop the server

Press `CTRL+C` in the terminal.

---

### 🚀 To Publish

Commit and push your changes to the `main` branch.
