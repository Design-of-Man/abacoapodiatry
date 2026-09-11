"""Google Business Profile review counts, stated once.

A snapshot, not a feed. This is a static site with no build-time network access
to Google's API, and the number the practice's own site can honestly claim is
whatever GBP showed the last time someone actually looked -- never a live
figure the page pretends to have just checked. Per-office review data on GBP:
Jupiter carries the practice's reviews (this file); Palm Beach Gardens has
none yet, so it gets no AggregateRating block until it does.

Refresh this by hand whenever GBP is pulled (the analytics skill, or Windsor's
google_my_business connector: fields review_total_count, review_average_rating_total
on the Jupiter location) and bump AS_OF. Do not wire this to fetch live --
Google's own number moves day to day, and a page asserting a rating it did not
just verify is worse than one that is a few weeks stale but honestly dated.
"""

JUPITER = {
    "count": 188,
    "rating": 4.9,
}

AS_OF = "2026-09-04"
SOURCE = "Google Business Profile, Jupiter location"


def aggregate_rating_property(item_id: str) -> str:
    """The `"aggregateRating": {...},` JSON-LD property line, or '' if there is
    nothing to claim. Callers splice this in right before another property so
    an empty result leaves valid JSON either way -- never a dangling comma.
    """
    if not JUPITER["count"]:
        return ""
    import json
    obj = json.dumps({
        "@type": "AggregateRating",
        "ratingValue": JUPITER["rating"],
        "reviewCount": JUPITER["count"],
        "itemReviewed": {"@id": item_id},
    })
    return f'"aggregateRating": {obj},'
