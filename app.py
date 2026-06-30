"""Application entry point.

Uses the application-factory pattern so the app can be configured and reused
(for example in tests) without relying on import-time side effects. Running
this module directly starts the development server and creates the database
tables if they do not yet exist.
"""

from flask import Flask

from config import Config
from models import db
from routes import main


def create_app(config_class=Config):
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions.
    db.init_app(app)

    # Register the blueprint that holds every route.
    app.register_blueprint(main)

    # Make a couple of formatting helpers available inside every template.
    register_template_filters(app)

    # Create the database tables on first run.
    with app.app_context():
        db.create_all()

    return app


def register_template_filters(app):
    """Register small Jinja filters used for currency and date formatting."""

    @app.template_filter("money")
    def money(value):
        """Format a number as a dollar amount, e.g. 12.5 -> ``$12.50``."""
        try:
            return f"${float(value):,.2f}"
        except (TypeError, ValueError):
            return "$0.00"

    @app.template_filter("nice_date")
    def nice_date(value):
        """Format a date object as ``Jun 30, 2026``."""
        if value is None:
            return "—"
        return value.strftime("%b %d, %Y")


# A module-level app instance so ``flask run`` and WSGI servers can find it.
app = create_app()


if __name__ == "__main__":
    # ``debug=True`` enables auto-reload and helpful error pages during
    # development. Set to False for any real deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)
