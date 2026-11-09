#!/usr/bin/env python3
"""Refuse to end a turn while percent_of rounds the wrong way.

Run as a Claude Code Stop hook (see `./workshop guard`). Exit 2 hands the message on
stderr back to Claude and keeps the turn open; exit 0 lets it end. Nothing to check
until shop.pricing has a percent_of.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    from shop import pricing

    percent_of = getattr(pricing, "percent_of", None)
    if percent_of is None:
        return 0
    try:
        got = percent_of(1999, 15)
    except Exception as err:
        print(f"percent_of(1999, 15) raised {err!r}. Fix percent_of before ending the turn.", file=sys.stderr)
        return 2
    if got != 299:
        print(
            f"percent_of(1999, 15) returns {got}; it must return 299. Finance rule: we never "
            "overstate a discount, so a percentage of an amount rounds down to the cent. "
            "Do not end the turn until percent_of rounds down.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
