from __future__ import annotations

import os
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return a reproducible UTC clock when SOURCE_DATE_EPOCH is set."""

    raw_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if raw_epoch is None:
        return datetime.now(timezone.utc).replace(microsecond=0)
    try:
        epoch = int(raw_epoch)
    except ValueError as exc:
        raise ValueError("SOURCE_DATE_EPOCH must be an integer Unix timestamp") from exc
    return datetime.fromtimestamp(epoch, tz=timezone.utc).replace(microsecond=0)


def today_iso() -> str:
    return utc_now().date().isoformat()


def now_iso() -> str:
    return utc_now().isoformat()
