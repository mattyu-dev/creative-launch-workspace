#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import hashlib
import struct
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
    "image": ("image", "image/jpeg", 64, 64, 0),
    "carousel": ("image", "image/jpeg", 64, 64, 0),
    "story": ("image", "image/jpeg", 64, 64, 0),
    "video": ("video", "video/mp4", 64, 64, 1),
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
                "metadata_source": "materialized_decodable_synthetic_media",
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
        return _VIDEO_MP4 + struct.pack(">I4s", 8 + len(marker), b"free") + marker
    if detected_mime == "image/jpeg":
        comment = b"\xff\xfe" + struct.pack(">H", len(marker) + 2) + marker
        return _IMAGE_JPEG[:-2] + comment + b"\xff\xd9"
    return b"META_IMPORTER_UNSUPPORTED_ASSET|" + marker


_IMAGE_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAgAAAQABAAD//gAQTGF2YzYyLjI4LjEwMgD/2wBDAAgEBAQEBAUFBQUFBQYGBgYGBgYGBgYGBgYHBwcICAgHBwcGBgcHCAgICAkJCQgICAgJCQoKCgwMCwsODg4RERT/xABNAAEBAAAAAAAAAAAAAAAAAAAABwEBAQEAAAAAAAAAAAAAAAAAAAMEEAEAAAAAAAAAAAAAAAAAAAAAEQEAAAAAAAAAAAAAAAAAAAAA/8AAEQgAQABAAwEiAAIRAAMRAP/aAAwDAQACEQMRAD8AtQDEsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//9k="
)

_VIDEO_MP4 = base64.b64decode(
    "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"
)


if __name__ == "__main__":
    raise SystemExit(main())
