"""Database models.

Defines the SQLAlchemy ``db`` instance and the single ``Subscription`` model.
Computed metrics (cost per use, health, waste score, ...) are exposed as
read-only properties that delegate to the pure functions in ``calculations``
so templates can access them naturally, e.g. ``subscription.cost_per_use``.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

import calculations

# The shared SQLAlchemy instance. It is bound to the Flask app inside the
# application factory in app.py via ``db.init_app(app)``.
db = SQLAlchemy()


class Subscription(db.Model):
    """A single tracked subscription and its derived waste metrics."""

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    billing_cycle = db.Column(db.String(10), nullable=False)  # "monthly"/"yearly"
    price = db.Column(db.Float, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    last_used = db.Column(db.Date, nullable=False)
    uses = db.Column(db.Integer, nullable=False, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ------------------------------------------------------------------ #
    # Derived metrics (not stored in the database)
    # ------------------------------------------------------------------ #
    @property
    def monthly_cost(self):
        """Normalised monthly cost of this subscription."""
        return calculations.monthly_cost(self.price, self.billing_cycle)

    @property
    def yearly_cost(self):
        """Normalised yearly cost of this subscription."""
        return calculations.yearly_cost(self.price, self.billing_cycle)

    @property
    def cost_per_use(self):
        """How much each use of this subscription costs."""
        return calculations.cost_per_use(self.price, self.uses)

    @property
    def days_since_used(self):
        """Number of days since the subscription was last used."""
        return calculations.days_since_used(self.last_used)

    @property
    def health(self):
        """Health label: Healthy, Warning or Waste."""
        return calculations.get_health(self.price, self.uses, self.last_used)

    @property
    def waste_score(self):
        """Integer waste score from 0 (great value) to 100 (pure waste)."""
        return calculations.get_waste_score(self.price, self.uses, self.last_used)

    @property
    def money_wasted_monthly(self):
        """Monthly money considered wasted for this subscription."""
        return calculations.money_wasted_monthly(
            self.price, self.billing_cycle, self.uses, self.last_used
        )

    def __repr__(self):
        return f"<Subscription {self.name!r} ({self.billing_cycle})>"
