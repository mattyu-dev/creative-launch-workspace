from __future__ import annotations

from dataclasses import asdict
from urllib.parse import parse_qsl, urlparse

from .clock import today_iso
from .launch_workspace import AdCandidate, LaunchPlan

OBJECTIVE_MAP = {
    "awareness": "OUTCOME_AWARENESS",
    "traffic": "OUTCOME_TRAFFIC",
    "engagement": "OUTCOME_ENGAGEMENT",
    "leads": "OUTCOME_LEADS",
    "app_promotion": "OUTCOME_APP_PROMOTION",
    "sales": "OUTCOME_SALES",
}

PLACEMENT_MAP = {
    "feed": {
        "publisher_platforms": ["facebook"],
        "facebook_positions": ["feed"],
        "status": "needs_sandbox_validation",
    },
    "story": {
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["story"],
        "instagram_positions": ["story"],
        "status": "needs_sandbox_validation",
    },
    "reels": {
        "publisher_platforms": ["instagram"],
        "instagram_positions": ["reels"],
        "status": "needs_sandbox_validation",
    },
    "marketplace": {
        "publisher_platforms": ["facebook"],
        "facebook_positions": ["marketplace"],
        "status": "needs_sandbox_validation",
    },
    "right_column": {
        "publisher_platforms": ["facebook"],
        "facebook_positions": ["right_hand_column"],
        "status": "needs_sandbox_validation",
    },
    "search": {
        "publisher_platforms": ["facebook"],
        "facebook_positions": ["search"],
        "status": "needs_sandbox_validation",
    },
}


def build_platform_payload_preview(plan: LaunchPlan) -> dict[str, object]:
    payloads = [_candidate_payload(candidate) for candidate in plan.candidates]
    readiness_counts: dict[str, int] = {}
    for payload in payloads:
        readiness = str(payload["payload_readiness"])
        readiness_counts[readiness] = readiness_counts.get(readiness, 0) + 1

    return {
        "product": "Creative Launch Workspace for Meta Ads",
        "contract_version": "meta_platform_payload_preview.v1",
        "source_contract_version": "offline_launch_plan.v2",
        "mode": "offline_platform_payload_preview_only",
        "generated_at": today_iso(),
        "mutation_allowed": False,
        "meta_api_compatibility": "mapped_not_executed",
        "data_classification": "synthetic_fixture_only",
        "asset_storage_policy": {
            "strategy": "meta_native_zero_retention_candidate",
            "current_status": "designed_not_executed",
            "preferred_destination": "business_creative_asset_management_folder",
            "fallback_destination": "ad_account_media_asset",
            "durable_local_storage": "metadata_lineage_only",
            "local_original_retention": "none_after_successful_upload_after_G4_approval",
            "durable_local_fields": [
                "source_asset_hash",
                "source_manifest_row",
                "meta_image_hash_or_video_id",
                "business_creative_folder_id",
                "upload_audit_event_id",
            ],
        },
        "source_manifest": plan.source_manifest,
        "summary": {
            "row_count": len(payloads),
            "readiness_counts": readiness_counts,
            "all_payloads_blocked": all(payload["payload_readiness"] != "ready_for_validate_only" for payload in payloads),
        },
        "hard_blocks": [
            "No account alias has been resolved to a real act_<AD_ACCOUNT_ID>.",
            "No Business ID or Business Creative Asset Management folder has been resolved.",
            "No Page or Instagram identity has been approved.",
            "No access token, OAuth flow, app secret, or system user is loaded.",
            "No real media has been uploaded to Meta business creative folders, adimages, or advideos.",
            "No transient asset retention/deletion path has been approved.",
            "No payload may be sent to Meta without HITL plus Platform/Security approval.",
        ],
        "payloads": payloads,
    }


def _candidate_payload(candidate: AdCandidate) -> dict[str, object]:
    blocked_fields = _blocked_fields(candidate)
    field_status = _field_status(candidate, blocked_fields)
    return {
        "creative_id": candidate.creative_id,
        "source_row": candidate.source_row,
        "idempotency_key": candidate.idempotency_key,
        "batch_state": candidate.batch_state,
        "payload_readiness": "draft_blocked",
        "mutation_allowed": False,
        "execution_options": ["validate_only"],
        "blocked_fields": blocked_fields,
        "platform_field_status": field_status,
        "platform_sequence": [
            _campaign_step(candidate),
            _adset_step(candidate),
            _media_step(candidate),
            _creative_step(candidate),
            _ad_step(candidate),
        ],
        "source_candidate": asdict(candidate),
    }


def _campaign_step(candidate: AdCandidate) -> dict[str, object]:
    return {
        "object": "Campaign",
        "method": "POST",
        "target_endpoint": "/act_<AD_ACCOUNT_ID>/campaigns",
        "payload": {
            "name": candidate.campaign_key,
            "objective": OBJECTIVE_MAP.get(candidate.objective, ""),
            "status": "PAUSED",
            "special_ad_categories": ["NONE"],
            "execution_options": ["validate_only"],
        },
        "required_before_send": ["resolved_ad_account_id", "special_ad_category_policy"],
    }


def _adset_step(candidate: AdCandidate) -> dict[str, object]:
    return {
        "object": "AdSet",
        "method": "POST",
        "target_endpoint": "/act_<AD_ACCOUNT_ID>/adsets",
        "payload": {
            "name": candidate.adset_key,
            "campaign_id": "<CAMPAIGN_ID_FROM_PREVIOUS_STEP>",
            "status": "PAUSED",
            "destination_type": "WEBSITE",
            "optimization_goal": _optimization_goal(candidate.objective),
            "billing_event": "IMPRESSIONS",
            "targeting": _targeting(candidate),
            "execution_options": ["validate_only"],
        },
        "required_before_send": [
            "campaign_id",
            "budget_policy",
            "targeting_policy",
            "optimization_billing_policy",
        ],
    }


def _media_step(candidate: AdCandidate) -> dict[str, object]:
    if candidate.format == "video":
        return {
            "object": "BusinessVideo or AdVideo",
            "method": "POST",
            "target_endpoint": "/<BUSINESS_ID>/videos",
            "fallback_endpoint": "/act_<AD_ACCOUNT_ID>/advideos",
            "destination": "Meta Business creative folder when approved; ad account video asset as fallback.",
            "local_storage_policy": "transient_upload_stream_only_no_original_retention_after_success",
            "payload": {
                "name": candidate.name,
                "title": candidate.name,
                "creative_folder_id": "<BUSINESS_CREATIVE_FOLDER_ID>",
                "upload_phase": "<UPLOAD_PHASE>",
            },
            "required_before_send": [
                "resolved_business_id_or_ad_account_id",
                "business_creative_folder_id_if_using_folder",
                "real_video_file",
                "file_size",
                "chunk_upload_policy",
                "transient_retention_deletion_policy",
                "upload_response_lineage",
            ],
        }
    return {
        "object": "BusinessImage or AdImage",
        "method": "POST",
        "target_endpoint": "/<BUSINESS_ID>/images",
        "fallback_endpoint": "/act_<AD_ACCOUNT_ID>/adimages",
        "destination": "Meta Business creative folder when approved; ad account image asset as fallback.",
        "local_storage_policy": "transient_upload_stream_only_no_original_retention_after_success",
        "payload": {
            "name": candidate.name,
            "creative_folder_id": "<BUSINESS_CREATIVE_FOLDER_ID>",
            "source_asset_path": candidate.asset_path,
            "source_asset_hash": candidate.asset_hash,
        },
        "required_before_send": [
            "resolved_business_id_or_ad_account_id",
            "business_creative_folder_id_if_using_folder",
            "real_image_file",
            "image_bytes_or_upload_policy",
            "transient_retention_deletion_policy",
            "upload_response_lineage",
        ],
    }


def _creative_step(candidate: AdCandidate) -> dict[str, object]:
    return {
        "object": "AdCreative",
        "method": "POST",
        "target_endpoint": "/act_<AD_ACCOUNT_ID>/adcreatives",
        "payload": {
            "name": candidate.name,
            "object_story_id": _existing_story_id(candidate),
            "object_story_spec": _object_story_spec(candidate),
            "url_tags": _url_tags(candidate),
            "execution_options": ["validate_only"],
        },
        "required_before_send": [
            "page_id_or_instagram_user_id",
            "media_upload_response",
            "existing_post_ownership_if_reuse",
        ],
    }


def _ad_step(candidate: AdCandidate) -> dict[str, object]:
    return {
        "object": "Ad",
        "method": "POST",
        "target_endpoint": "/act_<AD_ACCOUNT_ID>/ads",
        "payload": {
            "name": candidate.name,
            "adset_id": "<ADSET_ID_FROM_PREVIOUS_STEP>",
            "creative": {"creative_id": "<ADCREATIVE_ID_FROM_PREVIOUS_STEP>"},
            "status": "PAUSED",
            "execution_options": ["validate_only"],
        },
        "required_before_send": ["adset_id", "adcreative_id", "operator_approval"],
    }


def _blocked_fields(candidate: AdCandidate) -> list[dict[str, str]]:
    blocked = [
        {
            "field": "account_id_alias",
            "reason": "Alias is local only and is not a real act_<AD_ACCOUNT_ID>.",
        },
        {
            "field": "business_id",
            "reason": "No Business ID has been approved for Meta Business Creative Asset Management.",
        },
        {
            "field": "creative_folder_id",
            "reason": "No Meta creative folder has been approved or created for this synthetic fixture.",
        },
        {
            "field": "page_id_or_instagram_user_id",
            "reason": "No Page or Instagram identity has been approved for this synthetic fixture.",
        },
        {
            "field": "media_upload_response",
            "reason": "No image_hash or video_id from Meta upload exists.",
        },
    ]
    if candidate.batch_state != "launch_ready":
        blocked.append(
            {
                "field": "batch_state",
                "reason": f"Candidate is {candidate.batch_state}, not launch_ready.",
            }
        )
    if candidate.objective not in OBJECTIVE_MAP:
        blocked.append({"field": "objective", "reason": "Objective has no official enum mapping."})
    if candidate.placement not in PLACEMENT_MAP:
        blocked.append({"field": "placement", "reason": "Placement has no targeting draft mapping."})
    if candidate.format not in {"image", "video", "carousel", "story"}:
        blocked.append({"field": "format", "reason": "Format is unsupported by the offline workspace."})
    if candidate.post_id_type == "existing":
        blocked.append(
            {
                "field": "object_story_id",
                "reason": "Existing post reuse needs ownership and compatibility proof.",
            }
        )
    return blocked


def _field_status(candidate: AdCandidate, blocked_fields: list[dict[str, str]]) -> dict[str, str]:
    blocked_names = {item["field"] for item in blocked_fields}
    return {
        "account_id_alias": "blocked_local_alias" if "account_id_alias" in blocked_names else "mapped",
        "campaign_key": "mapped_to_campaign_name",
        "objective": "mapped_to_enum" if candidate.objective in OBJECTIVE_MAP else "blocked_unmapped",
        "adset_key": "mapped_to_adset_name",
        "placement": "draft_targeting_needs_sandbox" if candidate.placement in PLACEMENT_MAP else "blocked_unmapped",
        "asset_hash": "local_source_hash_not_meta_hash",
        "asset_storage": "planned_meta_native_zero_retention",
        "business_id": "blocked_until_G3_G4_approval",
        "creative_folder_id": "blocked_until_business_folder_proof",
        "destination_url": "mapped_to_link_data",
        "utm_fields": "mapped_to_url_tags",
        "post_id": "blocked_for_existing_post_reuse" if candidate.post_id_type == "existing" else "create_new_story_spec",
        "idempotency_key": "local_only",
        "approval_record": "local_only",
    }


def _targeting(candidate: AdCandidate) -> dict[str, object]:
    placement = {k: v for k, v in PLACEMENT_MAP.get(candidate.placement, {}).items() if k != "status"}
    targeting: dict[str, object] = {
        "geo_locations": {"countries": [candidate.country]} if candidate.country else {},
        "device_platforms": ["mobile", "desktop"],
    }
    targeting.update(placement)
    return targeting


def _object_story_spec(candidate: AdCandidate) -> dict[str, object]:
    spec: dict[str, object] = {
        "page_id": "<PAGE_ID_REQUIRED>",
        "link_data": {
            "message": candidate.hook or candidate.name,
            "name": candidate.name,
            "link": _base_link(candidate.final_url_preview or candidate.destination_url),
            "call_to_action": {
                "type": "LEARN_MORE",
                "value": {"link": _base_link(candidate.final_url_preview or candidate.destination_url)},
            },
        },
    }
    if candidate.format == "video":
        spec["video_data"] = {
            "video_id": "<VIDEO_ID_FROM_ADVIDEOS>",
            "message": candidate.hook or candidate.name,
            "title": candidate.name,
        }
    else:
        spec["link_data"]["image_hash"] = "<IMAGE_HASH_FROM_ADIMAGES>"
    return spec


def _existing_story_id(candidate: AdCandidate) -> str:
    return candidate.post_id if candidate.post_id_type == "existing" else ""


def _url_tags(candidate: AdCandidate) -> str:
    url = candidate.final_url_preview or candidate.destination_url
    parsed = urlparse(url)
    return "&".join(f"{key}={value}" for key, value in parse_qsl(parsed.query, keep_blank_values=True))


def _base_link(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(query="", fragment="").geturl()


def _optimization_goal(objective: str) -> str:
    if objective == "traffic":
        return "LINK_CLICKS"
    if objective == "sales":
        return "OFFSITE_CONVERSIONS"
    if objective == "leads":
        return "LEAD_GENERATION"
    if objective == "engagement":
        return "POST_ENGAGEMENT"
    if objective == "awareness":
        return "REACH"
    if objective == "app_promotion":
        return "APP_INSTALLS"
    return "NONE"
