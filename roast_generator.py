"""Roast generator.

Produces a randomly chosen, tongue-in-cheek message for a subscription based
on its health classification. There are dedicated message pools for each
category, with well over forty unique lines in total.
"""

import random

from calculations import HEALTHY, WARNING, WASTE

# Praise for subscriptions that genuinely earn their keep.
HEALTHY_ROASTS = [
    "Money well spent.",
    "Finally, a responsible financial decision.",
    "This one actually pulls its weight.",
    "A rare subscription with a pulse.",
    "Certified worth-it. Treat the others like this.",
    "You and this subscription are in a healthy relationship.",
    "Your accountant would be proud.",
    "Peak value detected. Carry on.",
    "This is what getting your money's worth looks like.",
    "No notes. Genuinely a good buy.",
    "The blueprint for how subscriptions should behave.",
    "Low cost, high love. Keep it.",
    "This subscription earns its spot on the bill.",
    "A wholesome little line item.",
    "If only they were all this good.",
]

# Gentle warnings for subscriptions on the edge.
WARNING_ROASTS = [
    "We're keeping an eye on this one.",
    "Borderline subscription abuse.",
    "It's not wasteful yet, but it's auditioning for the role.",
    "Use it or you'll be roasted next month.",
    "Living dangerously close to the cancel button.",
    "The vibes are mid. The value is mid-er.",
    "One bad month away from the chopping block.",
    "Skating by on a technicality.",
    "Not great, not terrible. Just expensive-ish.",
    "This one is on thin ice and it knows it.",
    "Could be worse, could be a lot better.",
    "Half worth it. Which half is up to you.",
    "Flirting with financial regret.",
    "A coin flip between value and waste.",
    "Prove yourself or get cut.",
]

# No mercy for subscriptions that drain the wallet for nothing.
WASTE_ROASTS = [
    "You've forgotten this exists.",
    "This is basically a monthly donation.",
    "Cancel me already.",
    "Your wallet deserves justice.",
    "A subscription so unused it's practically a charity.",
    "Paying rent for an app you never visit.",
    "This is a ghost on your bank statement.",
    "Even the company is surprised you're still paying.",
    "You're funding their holiday party. That's it.",
    "Delete it before it files for emancipation.",
    "The most expensive icon on your home screen.",
    "Money in, nothing out. Classic waste.",
    "This subscription is gaslighting your budget.",
    "It's not a subscription, it's a leak.",
    "Out of sight, out of mind, still on the bill.",
    "A masterclass in setting money on fire.",
    "Your most loyal expense and your least used app.",
    "This belongs in a museum of regret.",
    "Cancel it and treat yourself with the savings.",
    "You're paying premium for a dust collector.",
]


def get_roast(health):
    """Return a random roast message that matches the given health label.

    Falls back to the waste pool for any unexpected value so the UI always
    has something to display.
    """
    pools = {
        HEALTHY: HEALTHY_ROASTS,
        WARNING: WARNING_ROASTS,
        WASTE: WASTE_ROASTS,
    }
    return random.choice(pools.get(health, WASTE_ROASTS))
