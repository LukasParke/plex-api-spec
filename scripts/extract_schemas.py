#!/usr/bin/env python3
"""
Extract inline schemas from plex-api-spec.yaml into reusable components.
Run from repo root: python scripts/extract_schemas.py
"""

import yaml
from copy import deepcopy

SPEC_PATH = "plex-api-spec.yaml"


def load_spec():
    with open(SPEC_PATH, "r") as f:
        return yaml.safe_load(f)


def save_spec(spec):
    with open(SPEC_PATH, "w") as f:
        yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def extract_activity(spec):
    """Extract Activity inline schema from /activities GET 200 response."""
    items = spec["paths"]["/activities"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][0]["properties"]["Activity"][
        "items"
    ]
    spec["components"]["schemas"]["Activity"] = items
    spec["paths"]["/activities"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][0]["properties"]["Activity"][
        "items"
    ] = {"$ref": "#/components/schemas/Activity"}
    print("Extracted Activity schema")


def extract_butler_task(spec):
    """Extract ButlerTask inline schema from /butler GET 200 response."""
    items = spec["paths"]["/butler"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["ButlerTasks"]["properties"]["ButlerTask"]["items"]
    spec["components"]["schemas"]["ButlerTask"] = items
    spec["paths"]["/butler"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["ButlerTasks"]["properties"]["ButlerTask"]["items"] = {
        "$ref": "#/components/schemas/ButlerTask"
    }
    print("Extracted ButlerTask schema")


def extract_updater_release(spec):
    """Extract Release inline schema from /updater/status GET 200 response."""
    items = spec["paths"]["/updater/status"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][0]["properties"]["Release"][
        "items"
    ]
    spec["components"]["schemas"]["UpdaterRelease"] = items
    spec["paths"]["/updater/status"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][0]["properties"]["Release"][
        "items"
    ] = {"$ref": "#/components/schemas/UpdaterRelease"}
    print("Extracted UpdaterRelease schema")


def extract_download_queue(spec):
    """Extract DownloadQueue inline schema from POST /downloadQueue 200 response."""
    schema = spec["paths"]["/downloadQueue"]["post"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][1]["properties"]["DownloadQueue"]
    spec["components"]["schemas"]["DownloadQueue"] = schema
    spec["paths"]["/downloadQueue"]["post"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][1]["properties"][
        "DownloadQueue"
    ] = {"$ref": "#/components/schemas/DownloadQueue"}
    print("Extracted DownloadQueue schema")


def extract_download_queue_item(spec):
    """Extract DownloadQueueItem inline schema from GET /downloadQueue/{queueId}/items."""
    items = spec["paths"]["/downloadQueue/{queueId}/items"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["properties"]["MediaContainer"]["allOf"][1][
        "properties"
    ]["DownloadQueueItem"]["items"]
    spec["components"]["schemas"]["DownloadQueueItem"] = items
    spec["paths"]["/downloadQueue/{queueId}/items"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["properties"]["MediaContainer"]["allOf"][1][
        "properties"
    ]["DownloadQueueItem"]["items"] = {"$ref": "#/components/schemas/DownloadQueueItem"}
    print("Extracted DownloadQueueItem schema")


def extract_media_grabber(spec):
    """Extract MediaGrabber inline schema from GET /media/grabbers."""
    items = spec["paths"]["/media/grabbers"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][1]["properties"][
        "MediaGrabber"
    ]["items"]
    spec["components"]["schemas"]["MediaGrabber"] = items
    spec["paths"]["/media/grabbers"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["properties"]["MediaContainer"]["allOf"][1]["properties"][
        "MediaGrabber"
    ]["items"] = {"$ref": "#/components/schemas/MediaGrabber"}
    print("Extracted MediaGrabber schema")


def extract_device_channel(spec):
    """Extract DeviceChannel inline schema from GET /media/grabbers/devices/{deviceId}/channels."""
    items = spec["paths"]["/media/grabbers/devices/{deviceId}/channels"]["get"][
        "responses"
    ]["200"]["content"]["application/json"]["schema"]["properties"]["MediaContainer"][
        "allOf"
    ][1]["properties"]["DeviceChannel"]["items"]
    spec["components"]["schemas"]["DeviceChannel"] = items
    spec["paths"]["/media/grabbers/devices/{deviceId}/channels"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]["properties"]["MediaContainer"][
        "allOf"
    ][1]["properties"]["DeviceChannel"]["items"] = {
        "$ref": "#/components/schemas/DeviceChannel"
    }
    print("Extracted DeviceChannel schema")


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
