"""Application configuration.

Holds the Flask configuration values for Subscription Autopsy. Keeping
configuration in a dedicated module makes it easy to swap settings between
development and production without touching application logic.
"""

import os

# Absolute path to the directory that contains this file. Using an absolute
# path guarantees the SQLite database is created in the project root no matter
# which directory the app is launched from.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared across every environment."""

    # Secret key used to sign session cookies and flash messages. In a real
    # deployment this should be supplied through an environment variable.
    SECRET_KEY = os.environ.get("SECRET_KEY", "subscription-autopsy-secret-key")

    # SQLite connection string pointing at database.db in the project root.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    )

    # Disable the event system we do not use; this silences a warning and
    # avoids unnecessary overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
