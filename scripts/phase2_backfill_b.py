#!/usr/bin/env python3
"""
Phase 2b: Additional critical endpoints
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


def add_plex_tv_sharing(spec):
    paths = spec.setdefault("paths", {})
    x = get_x_plex_params()
    ok = ok_200()
    bad = {"$ref": "#/components/responses/400"}
    unauth = {"$ref": "#/components/responses/401"}

    # POST /shared_servers
    paths.setdefault("/shared_servers", {})
    paths["/shared_servers"] = {
        "post": {
            "operationId": "shareServer",
            "summary": "Share Server",
            "description": "Share a server with a friend or managed user.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x),
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    # PUT/DELETE /sharings/{userId}
    paths.setdefault("/sharings/{userId}", {})
    paths["/sharings/{userId}"] = {
        "put": {
            "operationId": "updateShare",
            "summary": "Update Share",
            "description": "Update friend filters (allowSync, filterMovies, etc.).",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "userId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
        "delete": {
            "operationId": "removeShare",
            "summary": "Remove Share",
            "description": "Remove a share / friend.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "userId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
    }

    # PUT /home/users/restricted/{userId}
    paths.setdefault("/home/users/restricted/{userId}", {})
    paths["/home/users/restricted/{userId}"] = {
        "put": {
            "operationId": "updateRestrictedUser",
            "summary": "Update Restricted User",
            "description": "Update restricted (managed) home user settings.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api/v2"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "userId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    # GET/POST /home/users
    paths.setdefault("/home/users", {})
    paths["/home/users"] = {
        "get": {
            "operationId": "getHomeUsers",
            "summary": "Get Home Users",
            "description": "Get the list of Plex Home users.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x),
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
        "post": {
            "operationId": "createHomeUser",
            "summary": "Create Home User",
            "description": "Create a new Plex Home user.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x),
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
    }

    # DELETE/PUT /home/users/{userId}
    paths.setdefault("/home/users/{userId}", {})
    paths["/home/users/{userId}"] = {
        "delete": {
            "operationId": "deleteHomeUser",
            "summary": "Delete Home User",
            "description": "Remove a Plex Home user.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "userId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
        "put": {
            "operationId": "updateHomeUser",
            "summary": "Update Home User",
            "description": "Update a Plex Home user.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "userId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        },
    }

    # POST /home/users/{id}/switch
    paths.setdefault("/home/users/{id}/switch", {})
    paths["/home/users/{id}/switch"] = {
        "post": {
            "operationId": "switchHomeUser",
            "summary": "Switch Home User",
            "description": "Switch to a Plex Home user and return a new auth token.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    # POST /servers/{machineId}/shared_servers
    paths.setdefault("/servers/{machineId}/shared_servers", {})
    paths["/servers/{machineId}/shared_servers"] = {
        "post": {
            "operationId": "shareServerLegacy",
            "summary": "Share Server (Legacy v1)",
            "description": "Share a library with a friend (legacy v1 XML endpoint).",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "machineId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    # GET /servers/{machineId}
    paths.setdefault("/servers/{machineId}", {})
    paths["/servers/{machineId}"] = {
        "get": {
            "operationId": "getServerDetails",
            "summary": "Get Server Details",
            "description": "Get server details for sharing.",
            "tags": ["Users"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "machineId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    # GET /claim/token.json
    paths.setdefault("/claim/token.json", {})
    paths["/claim/token.json"] = {
        "get": {
            "operationId": "getClaimToken",
            "summary": "Get Claim Token",
            "description": "Get a claim token for new server setup.",
            "tags": ["Authentication"],
            "servers": [{"url": "https://plex.tv/api"}],
            "parameters": deepcopy(x),
            "responses": {"200": ok, "400": deepcopy(bad), "401": deepcopy(unauth)},
        }
    }

    print("Added plex.tv sharing/home/claim endpoints")


def add_core_pms_remaining(spec):
    paths = spec.setdefault("paths", {})
    x = get_x_plex_params()
    ok = ok_200()

    # GET /system/agents/{agentId}
    paths.setdefault("/system/agents/{agentId}", {})
    paths["/system/agents/{agentId}"] = {
        "get": {
            "operationId": "getMetadataAgentDetails",
            "summary": "Get Metadata Agent Details",
            "description": "Get details and settings for a specific metadata agent.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "agentId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    # GET /system/settings
    paths.setdefault("/system/settings", {})
    paths["/system/settings"] = {
        "get": {
            "operationId": "getSystemSettings",
            "summary": "Get System Settings",
            "description": "Get system-level settings.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /system/updates
    paths.setdefault("/system/updates", {})
    paths["/system/updates"] = {
        "get": {
            "operationId": "checkForSystemUpdates",
            "summary": "Check for System Updates",
            "description": "Check for available PMS updates.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /diagnostics
    paths.setdefault("/diagnostics", {})
    paths["/diagnostics"] = {
        "get": {
            "operationId": "getDiagnostics",
            "summary": "Get Diagnostics",
            "description": "Get server diagnostics overview.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /diagnostics/databases
    paths.setdefault("/diagnostics/databases", {})
    paths["/diagnostics/databases"] = {
        "get": {
            "operationId": "downloadDatabaseDiagnostics",
            "summary": "Download Database Diagnostics",
            "description": "Download server database diagnostics bundle.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /diagnostics/logs
    paths.setdefault("/diagnostics/logs", {})
    paths["/diagnostics/logs"] = {
        "get": {
            "operationId": "downloadLogBundle",
            "summary": "Download Log Bundle",
            "description": "Download server logs bundle.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /statistics/bandwidth
    paths.setdefault("/statistics/bandwidth", {})
    paths["/statistics/bandwidth"] = {
        "get": {
            "operationId": "getBandwidthStatistics",
            "summary": "Get Bandwidth Statistics",
            "description": "Get dashboard bandwidth data.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "timespan",
                    "in": "query",
                    "schema": {"type": "integer", "minimum": 1, "maximum": 6},
                }
            ],
            "responses": {"200": ok},
        }
    }

    # GET /statistics/resources
    paths.setdefault("/statistics/resources", {})
    paths["/statistics/resources"] = {
        "get": {
            "operationId": "getResourceStatistics",
            "summary": "Get Resource Statistics",
            "description": "Get dashboard resource data.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /services/browse
    paths.setdefault("/services/browse", {})
    paths["/services/browse"] = {
        "get": {
            "operationId": "browseFilesystem",
            "summary": "Browse Filesystem",
            "description": "Browse filesystem paths accessible to the server.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "includeFiles",
                    "in": "query",
                    "schema": {"type": "boolean"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    # GET /services/browse/{base64path}
    paths.setdefault("/services/browse/{base64path}", {})
    paths["/services/browse/{base64path}"] = {
        "get": {
            "operationId": "browseFilesystemPath",
            "summary": "Browse Filesystem Path",
            "description": "Browse a specific filesystem path.",
            "tags": ["General"],
            "security": [{"token": ["admin"]}],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "base64path",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    # GET /sync
    paths.setdefault("/sync", {})
    paths["/sync"] = {
        "get": {
            "operationId": "getSyncStatus",
            "summary": "Get Sync Status",
            "description": "Get sync status overview.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /sync/items
    paths.setdefault("/sync/items", {})
    paths["/sync/items"] = {
        "get": {
            "operationId": "getSyncItems",
            "summary": "Get Sync Items",
            "description": "Get sync items list.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /sync/items/{syncId}
    paths.setdefault("/sync/items/{syncId}", {})
    paths["/sync/items/{syncId}"] = {
        "get": {
            "operationId": "getSyncItem",
            "summary": "Get Sync Item",
            "description": "Get sync item details.",
            "tags": ["General"],
            "parameters": deepcopy(x)
            + [
                {
                    "name": "syncId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "responses": {"200": ok},
        }
    }

    # GET /sync/queue
    paths.setdefault("/sync/queue", {})
    paths["/sync/queue"] = {
        "get": {
            "operationId": "getSyncQueue",
            "summary": "Get Sync Queue",
            "description": "Get sync queue.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /sync/transcodeQueue
    paths.setdefault("/sync/transcodeQueue", {})
    paths["/sync/transcodeQueue"] = {
        "get": {
            "operationId": "getSyncTranscodeQueue",
            "summary": "Get Sync Transcode Queue",
            "description": "Get sync transcode queue status.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # PUT /sync/refreshSynclists
    paths.setdefault("/sync/refreshSynclists", {})
    paths["/sync/refreshSynclists"] = {
        "put": {
            "operationId": "refreshSyncLists",
            "summary": "Refresh Sync Lists",
            "description": "Force PMS to download new SyncList from plex.tv.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # PUT /sync/refreshContent
    paths.setdefault("/sync/refreshContent", {})
    paths["/sync/refreshContent"] = {
        "put": {
            "operationId": "refreshSyncContent",
            "summary": "Refresh Sync Content",
            "description": "Force PMS to refresh content for known SyncLists.",
            "tags": ["General"],
            "parameters": deepcopy(x),
            "responses": {"200": ok},
        }
    }

    # GET /:/progress
    paths.setdefault("/:/progress", {})
    paths["/:/progress"] = {
        "get": {
            "operationId": "updateProgress",
            "summary": "Update Progress",
            "description": "Updates watch progress for an item.",
            "tags": ["General"],
            "parameters": deepcopy(x)
            + [
                {"name": "key", "in": "query", "required": True, "schema": {"type": "string"}},
                {"name": "identifier", "in": "query", "schema": {"type": "string"}},
                {"name": "time", "in": "query", "schema": {"type": "integer"}},
                {"name": "state", "in": "query", "schema": {"type": "string"}},
            ],
            "responses": {"200": ok},
        }
    }

    print("Added remaining core PMS endpoints")


def main():
    spec = load_spec()
    add_plex_tv_sharing(spec)
    add_core_pms_remaining(spec)
    save_spec(spec)
    print(f"Saved {SPEC_PATH}")


if __name__ == "__main__":
    main()
