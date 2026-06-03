#!/usr/bin/env python3
"""
Phase 2b: Client Remote-Control Protocol & Query Parameters
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


def get_x_plex_params():
    return [
        {"$ref": "#/components/parameters/accepts"},
        {"$ref": "#/components/parameters/X-Plex-Client-Identifier"},
        {"$ref": "#/components/parameters/X-Plex-Product"},
        {"$ref": "#/components/parameters/X-Plex-Version"},
        {"$ref": "#/components/parameters/X-Plex-Platform"},
        {"$ref": "#/components/parameters/X-Plex-Platform-Version"},
        {"$ref": "#/components/parameters/X-Plex-Device"},
        {"$ref": "#/components/parameters/X-Plex-Model"},
        {"$ref": "#/components/parameters/X-Plex-Device-Vendor"},
        {"$ref": "#/components/parameters/X-Plex-Device-Name"},
        {"$ref": "#/components/parameters/X-Plex-Marketplace"},
    ]


def ok_200():
    return {"description": "OK"}


def add_client_control_endpoints(spec):
    """Add the Plex Client Remote-Control Protocol endpoints."""
    paths = spec.setdefault("paths", {})
    x = get_x_plex_params()
    ok = ok_200()

    # Base params for all player endpoints
    player_params = deepcopy(x) + [
        {
            "name": "X-Plex-Target-Client-Identifier",
            "in": "header",
            "description": "The client identifier of the target device to control. If omitted, the command is sent to the default/active client.",
            "schema": {"type": "string"},
        }
    ]

    # Simple playback commands (POST, no body)
    simple_commands = [
        ("play", "Play", "Start playback on the client"),
        ("pause", "Pause", "Pause playback on the client"),
        ("stop", "Stop", "Stop playback on the client"),
        ("stepForward", "Step Forward", "Step forward one frame"),
        ("stepBack", "Step Back", "Step back one frame"),
        ("mute", "Mute", "Mute the client audio"),
        ("unmute", "Unmute", "Unmute the client audio"),
        ("refreshPlayQueue", "Refresh Play Queue", "Refresh the play queue on the client"),
    ]

    for cmd, summary, desc in simple_commands:
        path = f"/player/playback/{cmd}"
        paths.setdefault(path, {})
        paths[path] = {
            "post": {
                "operationId": f"player{cmd.title().replace('_', '')}",
                "summary": f"Player {summary}",
                "description": desc,
                "tags": ["Playback"],
                "parameters": deepcopy(player_params),
                "responses": {"200": ok},
            }
        }

    # Commands with query params
    paths.setdefault("/player/playback/seek", {})
    paths["/player/playback/seek"] = {
        "post": {
            "operationId": "playerSeek",
            "summary": "Player Seek",
            "description": "Seek to a specific time in the current playback.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "offset",
                    "in": "query",
                    "description": "Target offset in milliseconds",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/skipTo", {})
    paths["/player/playback/skipTo"] = {
        "post": {
            "operationId": "playerSkipTo",
            "summary": "Player Skip To",
            "description": "Skip to a specific item in the play queue.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "key",
                    "in": "query",
                    "description": "The key of the item to skip to",
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/skipBy", {})
    paths["/player/playback/skipBy"] = {
        "post": {
            "operationId": "playerSkipBy",
            "summary": "Player Skip By",
            "description": "Skip forward or backward by a number of items.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "offset",
                    "in": "query",
                    "description": "Number of items to skip (positive for forward, negative for backward)",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setParameters", {})
    paths["/player/playback/setParameters"] = {
        "post": {
            "operationId": "playerSetParameters",
            "summary": "Player Set Parameters",
            "description": "Set shuffle, repeat, and volume parameters.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "shuffle",
                    "in": "query",
                    "schema": {"type": "integer", "enum": [0, 1]},
                },
                {
                    "name": "repeat",
                    "in": "query",
                    "schema": {"type": "integer", "enum": [0, 1, 2]},
                },
                {
                    "name": "volume",
                    "in": "query",
                    "schema": {"type": "integer", "minimum": 0, "maximum": 100},
                },
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setStreams", {})
    paths["/player/playback/setStreams"] = {
        "post": {
            "operationId": "playerSetStreams",
            "summary": "Player Set Streams",
            "description": "Set active audio, subtitle, and video streams.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "audioStreamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                },
                {
                    "name": "subtitleStreamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                },
                {
                    "name": "videoStreamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                },
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/subtitleStream", {})
    paths["/player/playback/subtitleStream"] = {
        "post": {
            "operationId": "playerSubtitleStream",
            "summary": "Player Subtitle Stream",
            "description": "Change the active subtitle stream.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "streamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/audioStream", {})
    paths["/player/playback/audioStream"] = {
        "post": {
            "operationId": "playerAudioStream",
            "summary": "Player Audio Stream",
            "description": "Change the active audio stream.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "streamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/videoStream", {})
    paths["/player/playback/videoStream"] = {
        "post": {
            "operationId": "playerVideoStream",
            "summary": "Player Video Stream",
            "description": "Change the active video stream.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "streamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/volume", {})
    paths["/player/playback/volume"] = {
        "post": {
            "operationId": "playerVolume",
            "summary": "Player Volume",
            "description": "Set the client volume.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "level",
                    "in": "query",
                    "schema": {"type": "integer", "minimum": 0, "maximum": 100},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setTextStream", {})
    paths["/player/playback/setTextStream"] = {
        "post": {
            "operationId": "playerSetTextStream",
            "summary": "Player Set Text Stream",
            "description": "Set the active text stream.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "streamID",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setRating", {})
    paths["/player/playback/setRating"] = {
        "post": {
            "operationId": "playerSetRating",
            "summary": "Player Set Rating",
            "description": "Rate the currently playing item.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "rating",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setViewOffset", {})
    paths["/player/playback/setViewOffset"] = {
        "post": {
            "operationId": "playerSetViewOffset",
            "summary": "Player Set View Offset",
            "description": "Set the resume offset for the current item.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "offset",
                    "in": "query",
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/setState", {})
    paths["/player/playback/setState"] = {
        "post": {
            "operationId": "playerSetState",
            "summary": "Player Set State",
            "description": "Set the playback state directly.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "state",
                    "in": "query",
                    "schema": {"type": "string", "enum": ["playing", "paused", "stopped"]},
                }
            ],
            "responses": {"200": ok},
        }
    }

    paths.setdefault("/player/playback/playMedia", {})
    paths["/player/playback/playMedia"] = {
        "post": {
            "operationId": "playerPlayMedia",
            "summary": "Player Play Media",
            "description": "Play a specific media item on the client.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params)
            + [
                {
                    "name": "key",
                    "in": "query",
                    "description": "The key of the media item to play",
                    "schema": {"type": "string"},
                },
                {
                    "name": "offset",
                    "in": "query",
                    "schema": {"type": "integer"},
                },
                {
                    "name": "machineIdentifier",
                    "in": "query",
                    "schema": {"type": "string"},
                },
            ],
            "responses": {"200": ok},
        }
    }

    # Player timeline poll
    paths.setdefault("/player/timeline/poll", {})
    paths["/player/timeline/poll"] = {
        "get": {
            "operationId": "playerPollTimeline",
            "summary": "Player Poll Timeline",
            "description": "Poll the client for current playback timeline.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params),
            "responses": {"200": ok},
        }
    }

    # Client resources
    paths.setdefault("/player/resources", {})
    paths["/player/resources"] = {
        "get": {
            "operationId": "getClientResources",
            "summary": "Get Client Resources",
            "description": "Get client capabilities and device info.",
            "tags": ["Playback"],
            "parameters": deepcopy(player_params),
            "responses": {"200": ok},
        }
    }

    print(f"Added {len([p for p in paths if p.startswith('/player/')])} client control endpoints")


def add_query_params(spec):
    """Add critical missing query parameters to existing endpoints."""

    # Common include/exclude params
    include_markers = {
        "name": "includeMarkers",
        "in": "query",
        "description": "Include intro/credits markers in the response",
        "schema": {"type": "boolean"},
    }
    include_guids = {
        "name": "includeGuids",
        "in": "query",
        "description": "Include external GUIDs (e.g. TMDB, TVDB) in the response",
        "schema": {"type": "boolean"},
    }
    include_chapters = {
        "name": "includeChapters",
        "in": "query",
        "description": "Include chapter data in the response",
        "schema": {"type": "boolean"},
    }
    include_external_media = {
        "name": "includeExternalMedia",
        "in": "query",
        "description": "Include external/online media in the response",
        "schema": {"type": "boolean"},
    }
    include_extras = {
        "name": "includeExtras",
        "in": "query",
        "description": "Include trailers, behind-the-scenes, and other extras",
        "schema": {"type": "boolean"},
    }
    include_related = {
        "name": "includeRelated",
        "in": "query",
        "description": "Include related items in the response",
        "schema": {"type": "boolean"},
    }
    include_on_deck = {
        "name": "includeOnDeck",
        "in": "query",
        "description": "Include On Deck status in the response",
        "schema": {"type": "boolean"},
    }
    include_popular_leaves = {
        "name": "includePopularLeaves",
        "in": "query",
        "description": "Include popular episodes in the response",
        "schema": {"type": "boolean"},
    }
    include_reviews = {
        "name": "includeReviews",
        "in": "query",
        "description": "Include user reviews in the response",
        "schema": {"type": "boolean"},
    }
    include_stations = {
        "name": "includeStations",
        "in": "query",
        "description": "Include radio station data in the response",
        "schema": {"type": "boolean"},
    }
    check_files = {
        "name": "checkFiles",
        "in": "query",
        "description": "Verify file existence on disk",
        "schema": {"type": "boolean"},
    }
    exclude_elements = {
        "name": "excludeElements",
        "in": "query",
        "description": "Comma-separated list of elements to exclude from the response",
        "schema": {"type": "string"},
    }
    exclude_fields = {
        "name": "excludeFields",
        "in": "query",
        "description": "Comma-separated list of fields to exclude from the response",
        "schema": {"type": "string"},
    }
    include_collections = {
        "name": "includeCollections",
        "in": "query",
        "description": "Include collection results in search hubs",
        "schema": {"type": "boolean"},
    }

    # Add to /library/metadata/{ids} GET
    meta_get = spec["paths"]["/library/metadata/{ids}"]["get"]
    existing_params = meta_get.get("parameters", [])
    new_params = [
        include_markers, include_guids, include_chapters, include_external_media,
        include_extras, include_related, include_on_deck, include_popular_leaves,
        include_reviews, include_stations, check_files, exclude_elements, exclude_fields,
    ]
    for p in new_params:
        if not any(ep.get("name") == p["name"] for ep in existing_params):
            existing_params.append(p)
    print("Added query params to /library/metadata/{ids}")

    # Add to /library/sections/{sectionId}/all GET
    section_all = spec["paths"]["/library/sections/{sectionId}/all"]["get"]
    existing_params = section_all.get("parameters", [])
    new_params = [
        include_guids, include_external_media, include_extras, include_related,
        include_on_deck, include_popular_leaves, include_reviews, include_stations,
        check_files, exclude_elements, exclude_fields,
    ]
    for p in new_params:
        if not any(ep.get("name") == p["name"] for ep in existing_params):
            existing_params.append(p)
    print("Added query params to /library/sections/{sectionId}/all")

    # Add to /hubs/search GET
    hubs_search = spec["paths"]["/hubs/search"]["get"]
    existing_params = hubs_search.get("parameters", [])
    if not any(ep.get("name") == "includeCollections" for ep in existing_params):
        existing_params.append(include_collections)
    print("Added query params to /hubs/search")

    # Add to /hubs/search/voice GET
    hubs_voice = spec["paths"]["/hubs/search/voice"]["get"]
    existing_params = hubs_voice.get("parameters", [])
    if not any(ep.get("name") == "includeCollections" for ep in existing_params):
        existing_params.append(include_collections)
    print("Added query params to /hubs/search/voice")

    # Add to /status/sessions/history/all GET
    history = spec["paths"]["/status/sessions/history/all"]["get"]
    existing_params = history.get("parameters", [])
    new_params = [exclude_elements, exclude_fields]
    for p in new_params:
        if not any(ep.get("name") == p["name"] for ep in existing_params):
            existing_params.append(p)
    print("Added query params to /status/sessions/history/all")


def main():
    spec = load_spec()
    add_client_control_endpoints(spec)
    add_query_params(spec)
    save_spec(spec)
    print(f"Saved {SPEC_PATH}")


if __name__ == "__main__":
    main()
