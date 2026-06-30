

import csv
import io
from datetime import datetime

from calculations import HEALTHY, WARNING, WASTE

# Selectable categories offered in the add/edit forms and the filter menu.
CATEGORIES = [
    "Streaming",
    "Music",
    "Software",
    "AI Tools",
    "Cloud Storage",
    "Gaming",
    "News",
    "Fitness",
    "Productivity",
    "Shopping",
    "Other",
]

# Supported billing cycles.
BILLING_CYCLES = ["monthly", "yearly"]

# Health labels exposed to the filter menu.
HEALTH_OPTIONS = [HEALTHY, WARNING, WASTE]

# Sort options: maps the value used in the URL to a human-readable label.
SORT_OPTIONS = {
    "recent": "Recently Added",
    "price_high": "Highest Price",
    "price_low": "Lowest Price",
    "wasteful": "Most Wasteful",
    "least_used": "Least Used",
}

# Date format used by HTML5 date inputs and stored representations.
DATE_FORMAT = "%Y-%m-%d"


def parse_date(value):
    """Parse a YYYY-MM-DD string into a ``date`` or return ``None``."""
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT).date()
    except (ValueError, AttributeError):
        return None


def validate_subscription_form(form):
    """Validate raw form data for adding/editing a subscription.

    Returns a ``(data, errors)`` tuple where ``data`` is a dictionary of
    cleaned values ready to assign to a model and ``errors`` is a list of
    human-readable error strings. When ``errors`` is empty the data is valid.
    """
    errors = []

    # Name 
    name = (form.get("name") or "").strip()
    if not name:
        errors.append("Subscription name is required.")
    elif len(name) > 100:
        errors.append("Subscription name must be 100 characters or fewer.")

    # Category 
    category = (form.get("category") or "").strip()
    if category not in CATEGORIES:
        errors.append("Please choose a valid category.")

    # Billing cycle 
    billing_cycle = (form.get("billing_cycle") or "").strip().lower()
    if billing_cycle not in BILLING_CYCLES:
        errors.append("Billing cycle must be monthly or yearly.")

    # Price 
    price = None
    raw_price = (form.get("price") or "").strip()
    try:
        price = float(raw_price)
        if price <= 0:
            errors.append("Price must be greater than zero.")
    except ValueError:
        errors.append("Price must be a valid number.")

    # Renewal date 
    renewal_date = parse_date(form.get("renewal_date"))
    if renewal_date is None:
        errors.append("Please provide a valid renewal date.")

    # Last used date 
    last_used = parse_date(form.get("last_used"))
    if last_used is None:
        errors.append("Please provide a valid last-used date.")

    # Uses 
    uses = None
    raw_uses = (form.get("uses") or "").strip()
    try:
        uses = int(raw_uses)
        if uses < 0:
            errors.append("Number of uses cannot be negative.")
    except ValueError:
        errors.append("Number of uses must be a whole number.")

    # Notes (optional) 
    notes = (form.get("notes") or "").strip()

    data = {
        "name": name,
        "category": category,
        "billing_cycle": billing_cycle,
        "price": price,
        "renewal_date": renewal_date,
        "last_used": last_used,
        "uses": uses,
        "notes": notes,
    }
    return data, errors


def filter_subscriptions(subscriptions, category=None, billing_cycle=None,
                         health=None, search=None):
    """Return the subscriptions matching the provided filter criteria.

    Filtering is performed in Python because some fields (health) are derived
    at runtime rather than stored in the database.
    """
    result = list(subscriptions)

    if search:
        needle = search.strip().lower()
        result = [s for s in result if needle in s.name.lower()]

    if category and category != "all":
        result = [s for s in result if s.category == category]

    if billing_cycle and billing_cycle != "all":
        result = [s for s in result if s.billing_cycle == billing_cycle]

    if health and health != "all":
        result = [s for s in result if s.health == health]

    return result


def sort_subscriptions(subscriptions, sort_key):
    """Return the subscriptions ordered according to ``sort_key``."""
    result = list(subscriptions)

    if sort_key == "price_high":
        result.sort(key=lambda s: s.monthly_cost, reverse=True)
    elif sort_key == "price_low":
        result.sort(key=lambda s: s.monthly_cost)
    elif sort_key == "wasteful":
        result.sort(key=lambda s: s.waste_score, reverse=True)
    elif sort_key == "least_used":
        result.sort(key=lambda s: s.uses)
    else:  # "recent" and any unknown value
        result.sort(key=lambda s: s.created_at, reverse=True)

    return result


def subscriptions_to_csv(subscriptions):
    """Serialise subscriptions (with their derived metrics) into CSV text."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Name", "Category", "Billing Cycle", "Price", "Monthly Cost",
        "Yearly Cost", "Renewal Date", "Last Used", "Uses",
        "Cost Per Use", "Waste Score", "Health", "Notes", "Created At",
    ])

    for s in subscriptions:
        writer.writerow([
            s.name,
            s.category,
            s.billing_cycle,
            f"{s.price:.2f}",
            f"{s.monthly_cost:.2f}",
            f"{s.yearly_cost:.2f}",
            s.renewal_date.strftime(DATE_FORMAT) if s.renewal_date else "",
            s.last_used.strftime(DATE_FORMAT) if s.last_used else "",
            s.uses,
            f"{s.cost_per_use:.2f}",
            s.waste_score,
            s.health,
            s.notes or "",
            s.created_at.strftime("%Y-%m-%d %H:%M") if s.created_at else "",
        ])

    return output.getvalue()
