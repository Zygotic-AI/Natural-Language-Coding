"""Strip markdown links for machine parsers (fitness, landmines) after TERMS linking."""

from __future__ import annotations

import re

_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_links(text: str) -> str:
    return _LINK.sub(r"\1", text)
