#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "fixtures/fake_agency_creatives/manifest.csv"
TARGET = ROOT / "fixtures/fake_agency_creatives/manifest_v2.csv"
ASSET_METADATA = ROOT / "fixtures/fake_agency_creatives/asset_metadata.csv"

EXTRA_FIELDS = [
    "account_id_alias",
    "objective",
    "placement",
    "asset_hash",
    "variant_group",
    "hook",
    "language",
    "country",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "post_id",
    "post_id_type",
    "source_system",
    "source_row_id",
    "reviewer",
    "approved_at",
]


def main() -> int:
    with SOURCE.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) + EXTRA_FIELDS

    enriched = []
    for index, row in enumerate(rows, start=1):
        row = dict(row)
        country = country_for(row["adset_key"])
        language = "fr" if country == "FR" else "en"
        asset_hash = hashlib.sha256(row["asset_path"].encode()).hexdigest()[:16]
        variant_group = f"{row['campaign_key']}_{row['adset_key']}"
        post_id_type = "existing" if row["qa_issue"] == "duplicate_asset" else "new"
        post_id = f"post_{asset_hash[:10]}" if post_id_type == "existing" else ""
        approved = row["approval_status"] == "approved"
        row.update(
            {
                "account_id_alias": f"acct_fixture_{country.lower()}",
                "objective": objective_for(row["campaign_key"]),
                "placement": placement_for(row["format"]),
                "asset_hash": asset_hash,
                "variant_group": variant_group,
                "hook": row["primary_text"].split(" for ", 1)[0].lower().replace(" ", "_"),
                "language": language,
                "country": country,
                "utm_source": "facebook",
                "utm_medium": "paid_social",
                "utm_campaign": row["campaign_key"],
                "utm_content": f"{row['creative_id']}_{variant_group}",
                "utm_term": row["adset_key"],
                "post_id": post_id,
                "post_id_type": post_id_type,
                "source_system": "synthetic_sheet",
                "source_row_id": f"row_{index:03d}",
                "reviewer": "fixture_approver" if approved else "",
                "approved_at": "2026-07-05" if approved else "",
            }
        )
        enriched.append(row)

    with TARGET.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)

    write_asset_metadata(enriched)

    print(f"Wrote {TARGET.relative_to(ROOT)}")
    print(f"Wrote {ASSET_METADATA.relative_to(ROOT)}")
    return 0


def write_asset_metadata(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "asset_path",
        "asset_hash",
        "declared_format",
        "media_kind",
        "width_px",
        "height_px",
        "duration_seconds",
        "file_size_bytes",
        "checksum_sha256",
        "metadata_source",
    ]
    seen: set[str] = set()
    metadata_rows = []
    for row in rows:
        asset_path = row["asset_path"]
        if asset_path in seen:
            continue
        seen.add(asset_path)
        metadata_rows.append(asset_metadata_for(row))

    with ASSET_METADATA.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)


def asset_metadata_for(row: dict[str, str]) -> dict[str, str]:
    format_value = row["format"]
    media_kind = media_kind_for(format_value)
    width, height, duration = dimensions_for(format_value)
    checksum = hashlib.sha256(
        f"{row['asset_path']}|{row['asset_hash']}|{format_value}".encode()
    ).hexdigest()
    return {
        "asset_path": row["asset_path"],
        "asset_hash": row["asset_hash"],
        "declared_format": format_value,
        "media_kind": media_kind,
        "width_px": str(width),
        "height_px": str(height),
        "duration_seconds": str(duration),
        "file_size_bytes": str(file_size_for(format_value)),
        "checksum_sha256": checksum,
        "metadata_source": "synthetic_fixture_generator",
    }


def media_kind_for(format_value: str) -> str:
    if format_value == "video":
        return "video"
    if format_value in {"image", "story", "carousel"}:
        return "image"
    return "unsupported"


def dimensions_for(format_value: str) -> tuple[int, int, int]:
    if format_value == "video":
        return 1080, 1920, 12
    if format_value == "story":
        return 1080, 1920, 0
    if format_value == "carousel":
        return 1080, 1080, 0
    if format_value == "image":
        return 1200, 1200, 0
    return 0, 0, 0


def file_size_for(format_value: str) -> int:
    if format_value == "video":
        return 2400000
    if format_value == "story":
        return 420000
    if format_value == "carousel":
        return 680000
    if format_value == "image":
        return 360000
    return 0


def objective_for(campaign_key: str) -> str:
    if "sale" in campaign_key:
        return "sales"
    if "evergreen" in campaign_key:
        return "engagement"
    return "traffic"


def placement_for(format_value: str) -> str:
    if format_value == "story":
        return "story"
    if format_value == "video":
        return "reels"
    return "feed"


def country_for(adset_key: str) -> str:
    if adset_key.endswith("_fr"):
        return "FR"
    if adset_key.endswith("_ca"):
        return "CA"
    if adset_key.endswith("_uk"):
        return "GB"
    return "US"


if __name__ == "__main__":
    raise SystemExit(main())
