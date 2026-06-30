"""Waste analysis calculations.

This module contains pure helper functions that turn raw subscription values
(price, billing cycle, uses, last-used date) into the derived metrics the app
displays: monthly/yearly cost, cost per use, a health classification and a
0-100 waste score.

Keeping these functions free of any database or Flask dependency makes them
trivial to reason about and test.
"""

from datetime import date

# Health classification labels used throughout the application.
HEALTHY = "Healthy"
WARNING = "Warning"
WASTE = "Waste"

# A subscription that has not been used for longer than this many days is
# automatically considered wasteful, regardless of its cost per use.
STALE_DAYS = 45

# Cost-per-use thresholds (in dollars) that separate the health categories.
HEALTHY_THRESHOLD = 1.0
WARNING_THRESHOLD = 5.0


def monthly_cost(price, billing_cycle):
    """Return the normalised monthly cost of a subscription.

    Yearly subscriptions are divided by twelve so every subscription can be
    compared on a level monthly basis.
    """
    if billing_cycle == "yearly":
        return price / 12.0
    return price


def yearly_cost(price, billing_cycle):
    """Return the normalised yearly cost of a subscription."""
    if billing_cycle == "monthly":
        return price * 12.0
    return price


def cost_per_use(price, uses):
    """Return how much each use of the subscription costs.

    The price used here is the price for the current billing cycle, matching
    the ``uses`` value which counts uses during that same cycle. When a
    subscription has never been used we fall back to the full price so the
    figure reflects that every dollar has been wasted.
    """
    if uses and uses > 0:
        return price / uses
    return price


def days_since_used(last_used):
    """Return the number of days since the subscription was last used."""
    if last_used is None:
        return None
    return (date.today() - last_used).days


def get_health(price, uses, last_used):
    """Classify a subscription as Healthy, Warning or Waste.

    The rules, in priority order:
      * Never used, or unused for more than ``STALE_DAYS`` days -> Waste.
      * Cost per use above the warning threshold -> Waste.
      * Cost per use between the healthy and warning thresholds -> Warning.
      * Anything cheaper per use -> Healthy.
    """
    stale = days_since_used(last_used)

    if not uses or uses <= 0:
        return WASTE
    if stale is not None and stale > STALE_DAYS:
        return WASTE

    per_use = cost_per_use(price, uses)
    if per_use > WARNING_THRESHOLD:
        return WASTE
    if per_use >= HEALTHY_THRESHOLD:
        return WARNING
    return HEALTHY


def get_waste_score(price, uses, last_used):
    """Return an integer waste score from 0 (great value) to 100 (pure waste).

    The score blends two signals, each contributing up to 50 points:
      * how expensive each use is relative to the warning threshold, and
      * how long the subscription has gone unused relative to ``STALE_DAYS``.
    """
    per_use = cost_per_use(price, uses)
    cost_component = min(per_use / WARNING_THRESHOLD * 50.0, 50.0)

    stale = days_since_used(last_used)
    if stale is None:
        stale_component = 50.0
    else:
        stale_component = min(max(stale, 0) / STALE_DAYS * 50.0, 50.0)

    # A subscription that has never been used is always maximally wasteful.
    if not uses or uses <= 0:
        return 100

    score = round(cost_component + stale_component)
    return max(0, min(100, score))


def money_wasted_monthly(price, billing_cycle, uses, last_used):
    """Return the monthly money considered wasted for a subscription.

    The full normalised monthly cost is counted as wasted whenever the
    subscription is classified as Waste; otherwise nothing is wasted.
    """
    if get_health(price, uses, last_used) == WASTE:
        return monthly_cost(price, billing_cycle)
    return 0.0
