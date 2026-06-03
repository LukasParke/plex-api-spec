#!/usr/bin/env python3
"""
Extract inline schemas from plex-api-spec.yaml into reusable components.
Run from repo root: python scripts/extract_schemas.py
"""

import os
import sys
import yaml
from copy import deepcopy

SPEC_PATH = "plex-api-spec.yaml"


def load_spec():
    if not os.path.exists(SPEC_PATH):
        print(f"Error: Specification file not found at {SPEC_PATH}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(SPEC_PATH) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML in {SPEC_PATH}: {e}", file=sys.stderr)
        sys.exit(1)


def save_spec(spec):
    with open(SPEC_PATH, "w") as f:
        yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _safe_extract(spec, path_keys, schema_name, item_key="items"):
    """Safely extract an inline schema from a nested path."""
    try:
        current = spec
        for key in path_keys:
            current = current[key]
        spec["components"]["schemas"][schema_name] = deepcopy(current)
        # Replace with $ref
        parent = spec
        for key in path_keys[:-1]:
            parent = parent[key]
        parent[path_keys[-1]] = {"$ref": f"#/components/schemas/{schema_name}"}
        print(f"Extracted {schema_name} schema")
    except KeyError as e:
        print(f"Warning: Could not extract {schema_name} schema - missing key: {e}", file=sys.stderr)


def extract_activity(spec):
    """Extract Activity inline schema from /activities GET 200 response."""
    _safe_extract(
        spec,
        ["paths", "/activities", "get", "responses", "200", "content",
         "application/json", "schema", "properties", "MediaContainer",
         "allOf", 0, "properties", "Activity", "items"],
        "Activity",
    )


def extract_butler_task(spec):
    """Extract ButlerTask inline schema from /butler GET 200 response."""
    _safe_extract(
        spec,
        ["paths", "/butler", "get", "responses", "200", "content",
         "application/json", "schema", "properties", "ButlerTasks",
         "properties", "ButlerTask", "items"],
        "ButlerTask",
    )


def extract_updater_release(spec):
    """Extract Release inline schema from /updater/status GET 200 response."""
    _safe_extract(
        spec,
        ["paths", "/updater/status", "get", "responses", "200", "content",
         "application/json", "schema", "properties", "MediaContainer",
         "allOf", 0, "properties", "Release", "items"],
        "UpdaterRelease",
    )


def extract_download_queue(spec):
    """Extract DownloadQueue inline schema from POST /downloadQueue 200 response."""
    _safe_extract(
        spec,
        ["paths", "/downloadQueue", "post", "responses", "200", "content",
         "application/json", "schema", "properties", "MediaContainer",
         "allOf", 1, "properties", "DownloadQueue"],
        "DownloadQueue",
        item_key=None,
    )


def extract_download_queue_item(spec):
    """Extract DownloadQueueItem inline schema from GET /downloadQueue/{queueId}/items."""
    _safe_extract(
        spec,
        ["paths", "/downloadQueue/{queueId}/items", "get", "responses", "200",
         "content", "application/json", "schema", "properties", "MediaContainer",
         "allOf", 1, "properties", "DownloadQueueItem", "items"],
        "DownloadQueueItem",
    )


def extract_media_grabber(spec):
    """Extract MediaGrabber inline schema from GET /media/grabbers."""
    _safe_extract(
        spec,
        ["paths", "/media/grabbers", "get", "responses", "200", "content",
         "application/json", "schema", "properties", "MediaContainer",
         "allOf", 1, "properties", "MediaGrabber", "items"],
        "MediaGrabber",
    )


def extract_device_channel(spec):
    """Extract DeviceChannel inline schema from GET /media/grabbers/devices/{deviceId}/channels."""
    _safe_extract(
        spec,
        ["paths", "/media/grabbers/devices/{deviceId}/channels", "get",
         "responses", "200", "content", "application/json", "schema",
         "properties", "MediaContainer", "allOf", 1, "properties",
         "DeviceChannel", "items"],
        "DeviceChannel",
    )


def main():
    spec = load_spec()
    extract_activity(spec)
    extract_butler_task(spec)
    extract_updater_release(spec)
    extract_download_queue(spec)
    extract_download_queue_item(spec)
    extract_media_grabber(spec)
    extract_device_channel(spec)
    save_spec(spec)
    print(f"Saved {SPEC_PATH}")


if __name__ == "__main__":
    main()
