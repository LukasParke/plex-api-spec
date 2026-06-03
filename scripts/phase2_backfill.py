#!/usr/bin/env python3
"""
Phase 2: Critical Path Backfill
Adds missing CRITICAL/HIGH priority endpoints and schemas to plex-api-spec.yaml.
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


def add_schemas(spec):
    """Add WebSocket/Event schemas and other missing reusable schemas."""
    schemas = spec.setdefault("components", {}).setdefault("schemas", {})

    schemas["NotificationContainer"] = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "description": "The notification type"},
            "size": {"type": "integer", "description": "Number of notifications"},
            "PlaySessionStateNotification": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/PlaySessionStateNotification"},
            },
            "StatusNotification": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/StatusNotification"},
            },
            "ReachabilityNotification": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/ReachabilityNotification"},
            },
            "TimelineEntry": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/TimelineEntry"},
            },
        },
    }

    schemas["PlaySessionStateNotification"] = {
        "type": "object",
        "description": "Real-time playback state change notification",
        "properties": {
            "sessionKey": {"type": "string"},
            "guid": {"type": "string"},
            "ratingKey": {"type": "string"},
            "url": {"type": "string"},
            "key": {"type": "string"},
            "viewOffset": {"type": "integer"},
            "playQueueItemID": {"type": "integer"},
            "playQueueID": {"type": "integer"},
            "state": {"type": "string", "enum": ["playing", "paused", "stopped"]},
            "transcodeSession": {"type": "string"},
            "controllable": {"type": "string"},
        },
    }

    schemas["StatusNotification"] = {
        "type": "object",
        "description": "Server status notification (e.g. library scan complete)",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "type": {"type": "string"},
        },
    }

    schemas["ReachabilityNotification"] = {
        "type": "object",
        "description": "Server reachability status change notification",
        "properties": {
            "status": {"type": "string"},
        },
    }

    schemas["TimelineEntry"] = {
        "type": "object",
        "description": "A timeline update entry delivered via WebSocket or EventSource",
        "properties": {
            "itemID": {"type": "integer"},
            "type": {"type": "integer"},
            "title": {"type": "string"},
            "state": {"type": "integer"},
            "playQueueItemID": {"type": "integer"},
            "metadataState": {"type": "string"},
        },
    }

    print("Added event/notification schemas")


def add_plex_tv_endpoints(spec):
    """Add missing plex.tv v2 authentication and account endpoints."""
    paths = spec.setdefault("paths", {})

    # Common X-Plex parameter references
    x_plex_params = [
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

    # Standard 200 response for simple OK
    ok_200 = {"description": "OK"}
    bad_request = {"$ref": "#/components/responses/400"}
    unauthorized = {"$ref": "#/components/responses/401"}

    # OAuth PIN Flow
    paths.setdefault("/pins", {})
    paths["/pins"] = {
        "post": {
            "operationId": "createOAuthPin",
            "summary": "Create OAuth PIN",
            "description": "Create a 4-character PIN for device linking via OAuth. The user must visit https://plex.tv/link and enter the PIN to authorize the device.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "security": [{"clientIdentifier": []}],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "PIN created successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "code": {"type": "string"},
                                    "product": {"type": "string"},
                                    "trusted": {"type": "boolean"},
                                    "qr": {"type": "string"},
                                    "clientIdentifier": {"type": "string"},
                                    "expiresIn": {"type": "integer"},
                                    "createdAt": {"type": "string"},
                                    "expiresAt": {"type": "string"},
                                    "authToken": {"type": "string", "nullable": True},
                                    "newRegistration": {"type": "boolean"},
                                },
                            }
                        }
                    },
                },
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    paths.setdefault("/pins/{pinId}", {})
    paths["/pins/{pinId}"] = {
        "get": {
            "operationId": "getOAuthPin",
            "summary": "Get OAuth PIN Status",
            "description": "Poll the PIN status. Returns authToken when the user has linked the device.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "security": [{"clientIdentifier": []}],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "pinId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {
                "200": {
                    "description": "PIN status",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "code": {"type": "string"},
                                    "product": {"type": "string"},
                                    "trusted": {"type": "boolean"},
                                    "qr": {"type": "string"},
                                    "clientIdentifier": {"type": "string"},
                                    "expiresIn": {"type": "integer"},
                                    "createdAt": {"type": "string"},
                                    "expiresAt": {"type": "string"},
                                    "authToken": {"type": "string", "nullable": True},
                                    "newRegistration": {"type": "boolean"},
                                    "pmsIdentifier": {"type": "string", "nullable": True},
                                    "pmsVersion": {"type": "string", "nullable": True},
                                },
                            }
                        }
                    },
                },
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    # Sign out
    paths.setdefault("/users/signout", {})
    paths["/users/signout"] = {
        "delete": {
            "operationId": "signOut",
            "summary": "Sign Out",
            "description": "Invalidate the current authentication token.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x_plex_params),
            "responses": {"200": ok_200, "400": deepcopy(bad_request)},
        }
    }

    # Ping
    paths.setdefault("/ping", {})
    paths["/ping"] = {
        "get": {
            "operationId": "ping",
            "summary": "Ping",
            "description": "Health / latency check. No authentication required.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "security": [],
            "responses": {"200": ok_200},
        }
    }

    # Friends
    paths.setdefault("/friends", {})
    paths["/friends"] = {
        "get": {
            "operationId": "getFriends",
            "summary": "Get Friends",
            "description": "Get the list of friends and shared users.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "List of friends",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "users": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "uuid": {"type": "string"},
                                                "title": {"type": "string"},
                                                "username": {"type": "string"},
                                                "email": {"type": "string"},
                                                "thumb": {"type": "string"},
                                            },
                                        },
                                    }
                                },
                            }
                        }
                    },
                },
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    print("Added plex.tv auth/account endpoints")


def add_core_pms_endpoints(spec):
    """Add critical missing PMS local endpoints."""
    paths = spec.setdefault("paths", {})

    x_plex_params = [
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

    ok_200 = {"description": "OK"}

    # /clients
    paths.setdefault("/clients", {})
    paths["/clients"] = {
        "get": {
            "operationId": "getClients",
            "summary": "Get Clients",
            "description": "Get a list of connected Plex clients.",
            "tags": ["General"],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "List of clients",
                    "content": {
                        "application/json": {
                            "schema": {
                                "allOf": [
                                    {"$ref": "#/components/schemas/MediaContainer"},
                                    {
                                        "type": "object",
                                        "properties": {
                                            "Server": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/PlexDevice"},
                                            }
                                        },
                                    },
                                ]
                            }
                        }
                    },
                }
            },
        }
    }

    # /accounts
    paths.setdefault("/accounts", {})
    paths["/accounts"] = {
        "get": {
            "operationId": "getSystemAccounts",
            "summary": "Get System Accounts",
            "description": "Get a list of local system accounts.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x_plex_params),
            "responses": {"200": ok_200},
        }
    }

    # /devices
    paths.setdefault("/devices", {})
    paths["/devices"] = {
        "get": {
            "operationId": "getSystemDevices",
            "summary": "Get System Devices",
            "description": "Get a list of local system devices.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x_plex_params),
            "responses": {"200": ok_200},
        }
    }

    # /servers
    paths.setdefault("/servers", {})
    paths["/servers"] = {
        "get": {
            "operationId": "getLocalServers",
            "summary": "Get Local Servers",
            "description": "Get a list of local servers.",
            "tags": ["General"],
            "parameters": deepcopy(x_plex_params),
            "responses": {"200": ok_200},
        }
    }

    # /library/sections/{sectionId}/onDeck
    paths.setdefault("/library/sections/{sectionId}/onDeck", {})
    paths["/library/sections/{sectionId}/onDeck"] = {
        "get": {
            "operationId": "getOnDeck",
            "summary": "Get On Deck",
            "description": "Get On Deck items for a library section.",
            "tags": ["Library"],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "sectionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {
                "200": {
                    "description": "On Deck items",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MediaContainerWithMetadata"}
                        }
                    },
                }
            },
        }
    }

    # /library/sections/{sectionId}/recentlyAdded
    paths.setdefault("/library/sections/{sectionId}/recentlyAdded", {})
    paths["/library/sections/{sectionId}/recentlyAdded"] = {
        "get": {
            "operationId": "getRecentlyAddedBySection",
            "summary": "Get Recently Added by Section",
            "description": "Get recently added items for a specific library section.",
            "tags": ["Library"],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "sectionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {
                "200": {
                    "description": "Recently added items",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MediaContainerWithMetadata"}
                        }
                    },
                }
            },
        }
    }

    # /library/recentlyAdded
    paths.setdefault("/library/recentlyAdded", {})
    paths["/library/recentlyAdded"] = {
        "get": {
            "operationId": "getRecentlyAdded",
            "summary": "Get Recently Added",
            "description": "Get globally recently added items across all libraries.",
            "tags": ["Library"],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "Recently added items",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MediaContainerWithMetadata"}
                        }
                    },
                }
            },
        }
    }

    # /hubs/home/recentlyAdded
    paths.setdefault("/hubs/home/recentlyAdded", {})
    paths["/hubs/home/recentlyAdded"] = {
        "get": {
            "operationId": "getHomeRecentlyAdded",
            "summary": "Get Home Recently Added",
            "description": "Get hub-centric recently added items.",
            "tags": ["Hubs"],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "Recently added hub items",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MediaContainerWithHubs"}
                        }
                    },
                }
            },
        }
    }

    # /system/agents
    paths.setdefault("/system/agents", {})
    paths["/system/agents"] = {
        "get": {
            "operationId": "getMetadataAgents",
            "summary": "Get Metadata Agents",
            "description": "Get a list of available metadata agents.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x_plex_params),
            "responses": {"200": ok_200},
        }
    }

    # /actions/removeFromContinueWatching
    paths.setdefault("/actions/removeFromContinueWatching", {})
    paths["/actions/removeFromContinueWatching"] = {
        "put": {
            "operationId": "removeFromContinueWatching",
            "summary": "Remove from Continue Watching",
            "description": "Remove an item from the Continue Watching hub.",
            "tags": ["General"],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "ratingKey",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok_200},
        }
    }

    print("Added core PMS missing endpoints")


def add_cloud_provider_endpoints(spec):
    """Add Plex Discover / Cloud provider endpoints."""
    paths = spec.setdefault("paths", {})

    x_plex_params = [
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

    ok_200 = {"description": "OK"}
    bad_request = {"$ref": "#/components/responses/400"}
    unauthorized = {"$ref": "#/components/responses/401"}

    # Discover search
    paths.setdefault("/library/search", {})
    paths["/library/search"] = {
        "get": {
            "operationId": "searchDiscover",
            "summary": "Search Discover",
            "description": "Search movies and shows in Plex Discover.",
            "tags": ["Provider"],
            "servers": [{"url": "https://discover.provider.plex.tv"}],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "query",
                    "in": "query",
                    "schema": {"type": "string"},
                },
                {
                    "name": "limit",
                    "in": "query",
                    "schema": {"type": "integer", "default": 10},
                },
                {
                    "name": "searchTypes",
                    "in": "query",
                    "schema": {"type": "string", "example": "movies,tv"},
                },
                {
                    "name": "searchProviders",
                    "in": "query",
                    "schema": {
                        "type": "string",
                        "example": "discover,PLEXAVOD,PLEXTVOD",
                    },
                },
                {
                    "name": "includeMetadata",
                    "in": "query",
                    "schema": {"type": "integer", "default": 1},
                },
            ],
            "responses": {
                "200": ok_200,
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    # Discover watchlist
    paths.setdefault("/library/sections/watchlist/all", {})
    paths["/library/sections/watchlist/all"] = {
        "get": {
            "operationId": "getWatchlist",
            "summary": "Get Watchlist",
            "description": "Get the user's Plex Discover watchlist.",
            "tags": ["Provider"],
            "servers": [{"url": "https://discover.provider.plex.tv"}],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "200": {
                    "description": "Watchlist items",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MediaContainerWithMetadata"}
                        }
                    },
                },
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    # Add to watchlist
    paths.setdefault("/actions/addToWatchlist", {})
    paths["/actions/addToWatchlist"] = {
        "post": {
            "operationId": "addToWatchlist",
            "summary": "Add to Watchlist",
            "description": "Add an item to the user's Plex Discover watchlist.",
            "tags": ["Provider"],
            "servers": [{"url": "https://discover.provider.plex.tv"}],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "uri",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {
                "200": ok_200,
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    # Remove from watchlist
    paths.setdefault("/actions/removeFromWatchlist", {})
    paths["/actions/removeFromWatchlist"] = {
        "post": {
            "operationId": "removeFromWatchlist",
            "summary": "Remove from Watchlist",
            "description": "Remove an item from the user's Plex Discover watchlist.",
            "tags": ["Provider"],
            "servers": [{"url": "https://discover.provider.plex.tv"}],
            "parameters": deepcopy(x_plex_params)
            + [
                {
                    "name": "uri",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {
                "200": ok_200,
                "400": deepcopy(bad_request),
                "401": deepcopy(unauthorized),
            },
        }
    }

    print("Added cloud provider endpoints")


def add_websocket_path(spec):
    """Add the plural WebSocket notification path."""
    paths = spec.setdefault("paths", {})

    x_plex_params = [
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

    paths.setdefault("/:/websockets/notifications", {})
    paths["/:/websockets/notifications"] = {
        "get": {
            "operationId": "getWebsocketNotifications",
            "summary": "Get WebSocket Notifications",
            "description": "WebSocket endpoint for real-time notifications (plural alias). Connect with X-Plex-Token header. Delivers NotificationContainer messages.",
            "tags": ["Events"],
            "parameters": deepcopy(x_plex_params),
            "responses": {
                "101": {
                    "description": "Switching Protocols - WebSocket connection established",
                },
                "200": {
                    "description": "WebSocket messages",
                    "content": {
                        "application/octet-stream": {
                            "schema": {"$ref": "#/components/schemas/NotificationContainer"}
                        }
                    },
                },
            },
        }
    }

    print("Added WebSocket plural alias path")


def main():
    spec = load_spec()
    add_schemas(spec)
    add_plex_tv_endpoints(spec)
    add_core_pms_endpoints(spec)
    add_cloud_provider_endpoints(spec)
    add_websocket_path(spec)
    save_spec(spec)
    print(f"Saved {SPEC_PATH}")


if __name__ == "__main__":
    main()
