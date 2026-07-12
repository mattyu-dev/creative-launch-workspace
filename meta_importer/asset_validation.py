from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from .launch_workspace import LaunchPlan, ManifestRow, SUPPORTED_FORMATS


ASSET_METADATA_FIELDS = [
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

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov"}


def read_asset_metadata(path: str | Path) -> dict[str, dict[str, str]]:
    metadata_path = Path(path)
    with metadata_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {row.get("asset_path", ""): row for row in rows if row.get("asset_path")}


def validate_asset_metadata(
    plan: LaunchPlan, metadata_path: str | Path
) -> dict[str, object]:
    metadata = read_asset_metadata(metadata_path)
    issues: list[dict[str, object]] = []

    for row in plan.rows:
        asset = metadata.get(row.asset_path)
        if not asset:
            issues.append(
                _asset_issue(
                    row,
                    "blocker",
                    "missing_asset_metadata",
                    "No synthetic asset metadata exists for the manifest asset path.",
                    "Add the asset path to the synthetic asset metadata fixture.",
                )
            )
            continue
        issues.extend(_validate_asset_row(row, asset))

    blocker_count = sum(1 for issue in issues if issue["severity"] == "blocker")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    return {
        "contract_version": "synthetic_asset_validation.v1",
        "asset_metadata_path": str(metadata_path),
        "rows_checked": len(plan.rows),
        "unique_assets": len(metadata),
        "status": "blocked" if blocker_count else "warning" if warning_count else "pass",
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "metadata_rows": len(metadata),
            "image_like_rows": sum(
                1 for row in plan.rows if _expected_media_kind(row.format) == "image"
            ),
            "video_rows": sum(
                1 for row in plan.rows if _expected_media_kind(row.format) == "video"
            ),
            "unsupported_format_rows": sum(
                1 for row in plan.rows if row.format not in SUPPORTED_FORMATS
            ),
        },
    }


def _validate_asset_row(row: ManifestRow, asset: dict[str, str]) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    expected_kind = _expected_media_kind(row.format)
    if expected_kind is None:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "unsupported_asset_format",
                "The asset format is outside the supported offline launch formats.",
                "Convert the asset to image, video, carousel, or story before export.",
            )
        )
        return issues

    if asset.get("declared_format") != row.format:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_format_mismatch",
                "Synthetic metadata format does not match the manifest format.",
                "Regenerate or correct the asset metadata fixture.",
            )
        )
    if row.asset_hash and asset.get("asset_hash") != row.asset_hash:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_hash_mismatch",
                "Synthetic metadata hash does not match the manifest asset hash.",
                "Regenerate the manifest and metadata from the same source rows.",
            )
        )
    if asset.get("media_kind") != expected_kind:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_media_kind_mismatch",
                "Synthetic metadata media kind is incompatible with the manifest format.",
                "Correct the media kind or remap the row format.",
            )
        )

    suffix = Path(row.asset_path).suffix.lower()
    if expected_kind == "video":
        if suffix not in VIDEO_EXTENSIONS:
            issues.append(
                _asset_issue(
                    row,
                    "blocker",
                    "video_extension_mismatch",
                    "Video rows must reference a video-like file extension.",
                    "Use an .mp4 or .mov synthetic path for video rows.",
                )
            )
        if _number(asset.get("duration_seconds")) <= 0:
            issues.append(
                _asset_issue(
                    row,
                    "blocker",
                    "video_duration_missing",
                    "Video metadata requires positive duration_seconds.",
                    "Add duration metadata before export.",
                )
            )
    else:
        if suffix not in IMAGE_EXTENSIONS:
            issues.append(
                _asset_issue(
                    row,
                    "blocker",
                    "image_extension_mismatch",
                    "Image-like rows must reference an image-like file extension.",
                    "Use a .jpg, .jpeg, .png, or .webp synthetic path.",
                )
            )
        if _number(asset.get("width_px")) <= 0 or _number(asset.get("height_px")) <= 0:
            issues.append(
                _asset_issue(
                    row,
                    "blocker",
                    "image_dimensions_missing",
                    "Image-like metadata requires positive width and height.",
                    "Add dimensions before export.",
                )
            )

    if _number(asset.get("file_size_bytes")) <= 0:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_size_missing",
                "Synthetic metadata requires positive file_size_bytes.",
                "Add file size metadata before export.",
            )
        )
    if not asset.get("checksum_sha256"):
        issues.append(
            _asset_issue(
                row,
                "warning",
                "asset_checksum_missing",
                "Synthetic metadata is missing checksum_sha256.",
                "Add a checksum before relying on asset identity.",
            )
        )
    issues.extend(_validate_asset_bytes(row, asset, expected_kind))
    return issues


def _expected_media_kind(format_value: str) -> str | None:
    if format_value == "video":
        return "video"
    if format_value in {"image", "story", "carousel"}:
        return "image"
    return None


def _number(value: str | None) -> float:
    try:
        return float(value or 0)
    except ValueError:
        return 0


def _validate_asset_bytes(
    row: ManifestRow, asset: dict[str, str], expected_kind: str
) -> list[dict[str, object]]:
    path = Path(row.asset_path)
    if not path.is_file():
        return [
            _asset_issue(
                row,
                "blocker",
                "asset_file_missing",
                "Synthetic asset metadata exists, but the asset file is absent.",
                "Materialize the synthetic asset fixture before trusting file-byte QA.",
            )
        ]

    data = path.read_bytes()
    issues: list[dict[str, object]] = []
    checksum = asset.get("checksum_sha256", "")
    if checksum and checksum != hashlib.sha256(data).hexdigest():
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_checksum_mismatch",
                "Synthetic asset file bytes do not match checksum_sha256.",
                "Regenerate metadata from the current synthetic asset file.",
            )
        )

    size = int(_number(asset.get("file_size_bytes")))
    if size and size != len(data):
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_size_mismatch",
                "Synthetic asset file byte size does not match metadata.",
                "Regenerate file_size_bytes from the current synthetic asset file.",
            )
        )

    detected_mime = _detect_mime(data)
    declared_mime = asset.get("detected_mime", "")
    if declared_mime and declared_mime != detected_mime:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_mime_mismatch",
                "Synthetic asset bytes do not match the declared MIME signature.",
                "Regenerate metadata from the current synthetic asset file.",
            )
        )
    if expected_kind == "image" and detected_mime not in {"image/jpeg", "image/png", "image/webp"}:
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_image_signature_mismatch",
                "Image-like rows must reference image-like synthetic file bytes.",
                "Replace the synthetic asset with image-like bytes.",
            )
        )
    if expected_kind == "video" and detected_mime != "video/mp4":
        issues.append(
            _asset_issue(
                row,
                "blocker",
                "asset_video_signature_mismatch",
                "Video rows must reference video-like synthetic file bytes.",
                "Replace the synthetic asset with video-like bytes.",
            )
        )
    return issues


def _detect_mime(data: bytes) -> str:
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "image/webp"
    if len(data) >= 12 and data[4:8] == b"ftyp":
        return "video/mp4"
    return "application/octet-stream"


def _asset_issue(
    row: ManifestRow,
    severity: str,
    code: str,
    message: str,
    proposed_fix: str,
) -> dict[str, object]:
    return {
        "source_row": row.source_row,
        "creative_id": row.creative_id,
        "asset_path": row.asset_path,
        "severity": severity,
        "code": code,
        "owner": "Creative Ops Manager",
        "message": message,
        "proposed_fix": proposed_fix,
    }
