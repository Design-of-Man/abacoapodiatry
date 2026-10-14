"""Google Business Profile review counts, stated once.

A snapshot, not a feed. This is a static site with no build-time network access
to Google's API, and the number the practice's own site can honestly claim is
whatever GBP showed the last time someone actually looked -- never a live
figure the page pretends to have just checked. Per-office review data on GBP:
Jupiter carries the practice's reviews (this file); Palm Beach Gardens has
none yet (0 on 2026-10-14).

Refresh this by hand whenever GBP is pulled (the analytics skill, or Windsor's
google_my_business connector: fields review_total_count, review_average_rating_total
on the Jupiter location) and bump AS_OF. Do not wire this to fetch live --
Google's own number moves day to day, and a page asserting a rating it did not
just verify is worse than one that is a few weeks stale but honestly dated.

NO REVIEW SCHEMA. An AggregateRating block built from this file shipped on
every page from 2026-09-03 to 2026-10-14. It was removed on purpose: Google
treats review markup that a business publishes about itself (LocalBusiness or
Organization reviewing itself) as self-serving and ineligible for review rich
results, and the agency rule for every practice site is no AggregateRating and
no Review schema at all. The numbers here are shown to people as plain,
dated, linked text (`visible_line()`), which is allowed and is the part that
actually persuades. `_dev/preflight.py` fails the build if either type comes
back. Do not reintroduce `aggregate_rating_property()` output into JSON-LD.
"""
import html

JUPITER = {
    "count": 193,
    "rating": 4.9,
    # Google Maps listing for the Jupiter office (cid from the GBP API).
    "url": "https://maps.google.com/maps?cid=11864858736782389427",
}

AS_OF = "2026-10-14"
AS_OF_HUMAN = "October 14, 2026"
SOURCE = "Google Business Profile, Jupiter location"


def aggregate_rating_property(item_id: str) -> str:
    """Deliberately empty. See the module docstring: no review schema.

    Kept as a function (returning '') so template.html's {{REVIEW_LD_CLINIC}}
    placeholder still resolves to valid JSON without a template edit.
    """
    return ""


def visible_line() -> str:
    """Dated, linked, human-readable review count for page copy (HTML)."""
    if not JUPITER["count"]:
        return ""
    return (f'Our Jupiter office has {JUPITER["count"]} Google reviews with a '
            f'{JUPITER["rating"]} average, as of {AS_OF_HUMAN}. '
            f'<a href="{html.escape(JUPITER["url"])}" rel="noopener">Read them on Google</a>.')
