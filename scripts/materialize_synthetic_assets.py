#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fixtures/fake_agency_creatives/manifest_v2.csv"
METADATA = ROOT / "fixtures/fake_agency_creatives/asset_metadata.csv"

FIELDS = [
    "asset_path",
    "asset_hash",
    "declared_format",
    "media_kind",
    "detected_mime",
    "width_px",
    "height_px",
    "duration_seconds",
    "file_size_bytes",
    "checksum_sha256",
    "metadata_source",
]

DIMENSIONS = {
    "image": ("image", "image/jpeg", 1200, 1200, 0),
    "carousel": ("image", "image/jpeg", 1080, 1080, 0),
    "story": ("image", "image/jpeg", 1080, 1920, 0),
    "video": ("video", "video/mp4", 1080, 1920, 12),
    "collection": ("unsupported", "application/octet-stream", 0, 0, 0),
}


def main() -> int:
    with MANIFEST.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    by_path: dict[str, dict[str, str]] = {}
    for row in rows:
        by_path.setdefault(row["asset_path"], row)

    metadata_rows = []
    for asset_path, row in sorted(by_path.items()):
        declared_format = row["format"]
        media_kind, detected_mime, width, height, duration = DIMENSIONS.get(
            declared_format, ("unsupported", "application/octet-stream", 0, 0, 0)
        )
        path = ROOT / asset_path
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = _asset_bytes(asset_path, declared_format, detected_mime)
        path.write_bytes(payload)
        metadata_rows.append(
            {
                "asset_path": asset_path,
                "asset_hash": row.get("asset_hash", ""),
                "declared_format": declared_format,
                "media_kind": media_kind,
                "detected_mime": detected_mime,
                "width_px": str(width),
                "height_px": str(height),
                "duration_seconds": str(duration),
                "file_size_bytes": str(len(payload)),
                "checksum_sha256": hashlib.sha256(payload).hexdigest(),
                "metadata_source": "materialized_synthetic_fixture_bytes",
            }
        )

    with METADATA.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(metadata_rows)

    print(f"Wrote {len(metadata_rows)} synthetic assets")
    print(f"Wrote {METADATA.relative_to(ROOT)}")
    return 0


def _asset_bytes(asset_path: str, declared_format: str, detected_mime: str) -> bytes:
    marker = f"META_IMPORTER_SYNTHETIC_ASSET|{asset_path}|{declared_format}".encode()
    if detected_mime == "video/mp4":
        return b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom" + marker
    if detected_mime == "image/jpeg":
        return b"\xff\xd8\xff\xe0" + marker + b"\xff\xd9"
    return b"META_IMPORTER_UNSUPPORTED_ASSET|" + marker


if __name__ == "__main__":
    raise SystemExit(main())
