"""Application routes.

All user-facing pages live on a single Flask blueprint named ``main``. Each
view keeps its logic small by leaning on the calculations, roast, model and
utility modules.
"""

from flask import (
    Blueprint, Response, flash, redirect, render_template, request, url_for,
)

import utils
from calculations import HEALTHY, WASTE
from models import Subscription, db
from roast_generator import get_roast

main = Blueprint("main", __name__)


def _attach_roasts(subscriptions):
    """Attach a freshly chosen roast to each subscription for this request."""
    for subscription in subscriptions:
        subscription.roast = get_roast(subscription.health)
    return subscriptions


@main.route("/")
def dashboard():
    """Render the dashboard with high-level spending and waste summaries."""
    subscriptions = Subscription.query.all()

    total_monthly = sum(s.monthly_cost for s in subscriptions)
    total_yearly = sum(s.yearly_cost for s in subscriptions)
    active_count = len(subscriptions)
    wasted_monthly = sum(s.money_wasted_monthly for s in subscriptions)

    if subscriptions:
        average_cost_per_use = (
            sum(s.cost_per_use for s in subscriptions) / len(subscriptions)
        )
        worst = max(subscriptions, key=lambda s: s.waste_score)
        # Best value: the lowest cost-per-use among subscriptions actually used.
        used = [s for s in subscriptions if s.uses and s.uses > 0]
        best = min(used, key=lambda s: s.cost_per_use) if used else None
        recent = sorted(
            subscriptions, key=lambda s: s.created_at, reverse=True
        )[:3]
    else:
        average_cost_per_use = 0.0
        worst = None
        best = None
        recent = []

    # Attach roast messages so the cards can display them.
    _attach_roasts([s for s in (worst, best) if s is not None])
    _attach_roasts(recent)

    return render_template(
        "dashboard.html",
        total_monthly=total_monthly,
        total_yearly=total_yearly,
        active_count=active_count,
        wasted_monthly=wasted_monthly,
        wasted_yearly=wasted_monthly * 12,
        average_cost_per_use=average_cost_per_use,
        worst=worst,
        best=best,
        recent=recent,
    )


@main.route("/subscriptions")
def subscriptions():
    """List subscriptions with search, filtering and sorting (all via GET)."""
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "all")
    billing_cycle = request.args.get("billing_cycle", "all")
    health = request.args.get("health", "all")
    sort_key = request.args.get("sort", "recent")

    all_subscriptions = Subscription.query.all()
    filtered = utils.filter_subscriptions(
        all_subscriptions,
        category=category,
        billing_cycle=billing_cycle,
        health=health,
        search=search,
    )
    ordered = utils.sort_subscriptions(filtered, sort_key)
    _attach_roasts(ordered)

    return render_template(
        "subscriptions.html",
        subscriptions=ordered,
        total_count=len(all_subscriptions),
        search=search,
        selected_category=category,
        selected_billing=billing_cycle,
        selected_health=health,
        selected_sort=sort_key,
        categories=utils.CATEGORIES,
        billing_cycles=utils.BILLING_CYCLES,
        health_options=utils.HEALTH_OPTIONS,
        sort_options=utils.SORT_OPTIONS,
    )


@main.route("/add", methods=["GET", "POST"])
def add_subscription():
    """Display and process the add-subscription form."""
    if request.method == "POST":
        data, errors = utils.validate_subscription_form(request.form)
        if errors:
            for message in errors:
                flash(message, "error")
            # Re-render the form preserving what the user already typed.
            return render_template(
                "add_subscription.html",
                form_data=request.form,
                categories=utils.CATEGORIES,
                billing_cycles=utils.BILLING_CYCLES,
            )

        subscription = Subscription(**data)
        db.session.add(subscription)
        db.session.commit()
        flash(f"Subscription '{subscription.name}' added.", "success")
        return redirect(url_for("main.subscriptions"))

    return render_template(
        "add_subscription.html",
        form_data={},
        categories=utils.CATEGORIES,
        billing_cycles=utils.BILLING_CYCLES,
    )


@main.route("/edit/<int:subscription_id>", methods=["GET", "POST"])
def edit_subscription(subscription_id):
    """Display and process the edit-subscription form."""
    subscription = Subscription.query.get_or_404(subscription_id)

    if request.method == "POST":
        data, errors = utils.validate_subscription_form(request.form)
        if errors:
            for message in errors:
                flash(message, "error")
            return render_template(
                "edit_subscription.html",
                subscription=subscription,
                form_data=request.form,
                categories=utils.CATEGORIES,
                billing_cycles=utils.BILLING_CYCLES,
            )

        for field, value in data.items():
            setattr(subscription, field, value)
        db.session.commit()
        flash(f"Subscription '{subscription.name}' updated.", "success")
        return redirect(url_for("main.subscriptions"))

    return render_template(
        "edit_subscription.html",
        subscription=subscription,
        form_data=subscription,
        categories=utils.CATEGORIES,
        billing_cycles=utils.BILLING_CYCLES,
    )


@main.route("/delete/<int:subscription_id>", methods=["GET", "POST"])
def delete_subscription(subscription_id):
    """Show a confirmation page (GET) and perform the deletion (POST)."""
    subscription = Subscription.query.get_or_404(subscription_id)

    if request.method == "POST":
        name = subscription.name
        db.session.delete(subscription)
        db.session.commit()
        flash(f"Subscription '{name}' deleted.", "success")
        return redirect(url_for("main.subscriptions"))

    return render_template(
        "delete_confirmation.html", subscription=subscription
    )


@main.route("/statistics")
def statistics():
    """Render aggregate statistics across all subscriptions."""
    subscriptions = Subscription.query.all()

    if not subscriptions:
        return render_template("statistics.html", has_data=False)

    most_expensive = max(subscriptions, key=lambda s: s.monthly_cost)
    cheapest = min(subscriptions, key=lambda s: s.monthly_cost)
    highest_cpu = max(subscriptions, key=lambda s: s.cost_per_use)
    lowest_cpu = min(subscriptions, key=lambda s: s.cost_per_use)
    longest_unused = max(subscriptions, key=lambda s: s.days_since_used or 0)

    count = len(subscriptions)
    avg_monthly = sum(s.monthly_cost for s in subscriptions) / count
    avg_cpu = sum(s.cost_per_use for s in subscriptions) / count
    wasted_year = sum(s.money_wasted_monthly for s in subscriptions) * 12

    # Health breakdown counts for the bar chart rendered in pure CSS.
    breakdown = {label: 0 for label in utils.HEALTH_OPTIONS}
    for s in subscriptions:
        breakdown[s.health] += 1

    return render_template(
        "statistics.html",
        has_data=True,
        count=count,
        most_expensive=most_expensive,
        cheapest=cheapest,
        highest_cpu=highest_cpu,
        lowest_cpu=lowest_cpu,
        longest_unused=longest_unused,
        avg_monthly=avg_monthly,
        avg_cpu=avg_cpu,
        wasted_year=wasted_year,
        breakdown=breakdown,
        healthy_label=HEALTHY,
        waste_label=WASTE,
    )


@main.route("/export")
def export_csv():
    """Export every subscription as a downloadable CSV file."""
    subscriptions = Subscription.query.order_by(Subscription.created_at).all()
    csv_text = utils.subscriptions_to_csv(subscriptions)
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=subscription_autopsy.csv"
        },
    )
