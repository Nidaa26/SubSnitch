#!/usr/bin/env python3
"""One-command launcher for Subscription Autopsy (macOS, Windows & Linux).

Run it with::

    python run.py        (Windows)
    python3 run.py       (macOS / Linux)

On first launch it creates a local virtual environment in ``.venv``, installs
the dependencies from ``requirements.txt`` into it, then starts the Flask
development server and opens your browser. On later launches it skips straight
to starting the server. No manual virtual-environment juggling required.
"""

import os
import subprocess
import sys
import time
import webbrowser

# Project paths 
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")
URL = "http://127.0.0.1:5000"


def venv_python():
    """Return the path to the Python interpreter inside the virtual env."""
    if os.name == "nt":  # Windows
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")  # macOS / Linux


def running_inside_venv():
    """True when the current interpreter is the project's virtual env."""
    return os.path.abspath(sys.executable) == os.path.abspath(venv_python())


def create_venv():
    """Create the virtual environment if it does not already exist."""
    if not os.path.exists(venv_python()):
        print("📦 Creating virtual environment in .venv ...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])


def install_requirements():
    """Install/upgrade dependencies inside the virtual environment."""
    print("⬇️  Installing dependencies ...")
    python = venv_python()
    subprocess.check_call([python, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call(
        [python, "-m", "pip", "install", "-r",
         os.path.join(PROJECT_DIR, "requirements.txt")]
    )


def bootstrap_and_relaunch():
    """Set up the venv then re-run this script using the venv's interpreter."""
    create_venv()
    install_requirements()
    print("🚀 Starting Subscription Autopsy ...")
    # Re-run this exact script with the virtual environment's Python so the
    # Flask app imports the freshly installed packages.
    os.execv(venv_python(), [venv_python(), os.path.abspath(__file__)])


def start_server():
    """Open the browser and launch the Flask development server."""
    print(f"✅ Subscription Autopsy is running at {URL}")
    print("   Press CTRL+C to stop.")

    # Open the browser shortly after the server starts. We only do this once.
    if os.environ.get("AUTOPSY_BROWSER_OPENED") != "1":
        os.environ["AUTOPSY_BROWSER_OPENED"] = "1"
        try:
            time.sleep(1)
            webbrowser.open(URL)
        except Exception:
            # Opening a browser is a nicety, never fatal.
            pass

    # Import here so this only happens once dependencies are guaranteed present.
    from app import app
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    if running_inside_venv():
        start_server()
    else:
        bootstrap_and_relaunch()
