#!/usr/bin/env python3
"""
Extract heavily duplicated inline schemas into reusable components.
Targets the duplicate-schemas warnings from Speakeasy lint.
"""

import yaml
import copy

SPEC_PATH = "plex-api-spec.yaml"

def load_spec():
    with open(SPEC_PATH, "r") as f:
        return yaml.safe_load(f)

def save_spec(spec):
    with open(SPEC_PATH, "w") as f:
        yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def find_and_replace(obj, target, replacement):
    """Recursively find target dict and replace with replacement."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, dict) and v == target:
                obj[k] = copy.deepcopy(replacement)
            else:
                find_and_replace(v, target, replacement)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, dict) and item == target:
                obj[i] = copy.deepcopy(replacement)
            else:
                find_and_replace(item, target, replacement)

def main():
    spec = load_spec()
    schemas = spec.setdefault("components", {}).setdefault("schemas", {})

    # 1. PlexBoolean - the 0/1 enum used for boolean-like fields
    plex_boolean = {"type": "integer", "enum": [0, 1], "description": "Plex boolean: 0 = false, 1 = true"}
    schemas["PlexBoolean"] = plex_boolean
    # Replace all inline {type: integer, enum: [0, 1]} with $ref
    find_and_replace(spec, {"type": "integer", "enum": [0, 1]}, {"$ref": "#/components/schemas/PlexBoolean"})

    # 2. PlexError - the code/message/status error object
    plex_error = {
        "type": "object",
        "properties": {
            "code": {"type": "integer"},
            "message": {"type": "string"},
            "status": {"type": "integer"},
        },
        "description": "Plex API error detail",
    }
    schemas["PlexError"] = plex_error
    # Replace inline error objects
    find_and_replace(spec, plex_error, {"$ref": "#/components/schemas/PlexError"})

    # 3. ConnectionProtocol - lan/wan/cellular
    conn_proto = {"type": "string", "enum": ["lan", "wan", "cellular"]}
    schemas["ConnectionProtocol"] = conn_proto
    find_and_replace(spec, conn_proto, {"$ref": "#/components/schemas/ConnectionProtocol"})

    # 4. StreamProtocol - http/hls/dash
    stream_proto = {"type": "string", "enum": ["http", "hls", "dash"]}
    schemas["StreamProtocol"] = stream_proto
    find_and_replace(spec, stream_proto, {"$ref": "#/components/schemas/StreamProtocol"})

    # 5. SubtitleBurnMode - auto/burn/none/subtitle/only_text/image
    burn_mode = {"type": "string", "enum": ["auto", "burn", "none", "subtitle", "only_text", "image"]}
    schemas["SubtitleBurnMode"] = burn_mode
    find_and_replace(spec, burn_mode, {"$ref": "#/components/schemas/SubtitleBurnMode"})

    # 6. MediaType - audio/video/photo
    media_type = {"type": "string", "enum": ["audio", "video", "photo"]}
    schemas["MediaType"] = media_type
    find_and_replace(spec, media_type, {"$ref": "#/components/schemas/MediaType"})

    # 7. PlaybackState - playing/paused/stopped
    playback_state = {"type": "string", "enum": ["playing", "paused", "stopped"]}
    schemas["PlaybackState"] = playback_state
    find_and_replace(spec, playback_state, {"$ref": "#/components/schemas/PlaybackState"})

    # 8. ButlerTaskType - all the butler task enum values
    butler_tasks = {
        "type": "string",
        "enum": [
            "AutomaticUpdates",
            "BackupDatabase",
            "ButlerTaskGenerateAdMarkers",
            "ButlerTaskGenerateChapterThumbnails",
            "ButlerTaskGeneratePreviewFiles",
            "ButlerTaskGenerateStaticMedia",
            "ButlerTaskGenerateStaticPreview",
            "ButlerTaskGenerateVideoPreview",
            "ButlerTaskIndexLibraries",
            "ButlerTaskRefreshLibraries",
            "ButlerTaskRefreshLocalMedia",
            "ButlerTaskUpgradeMediaAnalysis",
            "CleanOldBundles",
            "CleanOldCacheFiles",
            "CleanOldMediaAssets",
            "DeepMediaAnalysis",
            "OptimizeDatabase",
            "RefreshLibraries",
            "RefreshPeriodicMetadata",
            "UpgradeMediaAnalysis",
        ],
    }
    schemas["ButlerTaskType"] = butler_tasks
    find_and_replace(spec, butler_tasks, {"$ref": "#/components/schemas/ButlerTaskType"})

    # 9. UpdateStatus - available/downloading/downloaded/...
    update_status = {
        "type": "string",
        "enum": [
            "available",
            "downloading",
            "downloaded",
            "installing",
            "installed",
            "error",
            "restarting",
        ],
    }
    schemas["UpdateStatus"] = update_status
    find_and_replace(spec, update_status, {"$ref": "#/components/schemas/UpdateStatus"})

    # 10. ImageType - thumb/art/clearLogo/poster/banner/background
    image_type = {"type": "string", "enum": ["thumb", "art", "clearLogo", "poster", "banner", "background"]}
    schemas["ImageType"] = image_type
    find_and_replace(spec, image_type, {"$ref": "#/components/schemas/ImageType"})

    # 11. CountType - all/count
    count_type = {"type": "string", "enum": ["all", "count"]}
    schemas["CountType"] = count_type
    find_and_replace(spec, count_type, {"$ref": "#/components/schemas/CountType"})

    save_spec(spec)
    print(f"Extracted {len(schemas)} total schemas")
    print("Done. Run prettier and speakeasy lint to validate.")

if __name__ == "__main__":
    main()
