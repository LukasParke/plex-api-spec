#!/usr/bin/env python3
"""
Synthetic traffic generator for Plex Media Server.
Exercises a broad set of endpoints through the Arbiter proxy to maximize
coverage for the discovery/diff pipeline.
"""

import argparse
import sys
import time
import urllib.request
import urllib.error
import json


def fetch(base: str, path: str, method: str = "GET", headers: dict = None, data: bytes = None):
    """Make a request and return (status, body)."""
    url = f"{base}{path}"
    req = urllib.request.Request(url, method=method, data=data)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except Exception as e:
        return 0, str(e)


def run(base: str, token: str = None):
    headers = {}
    if token:
        headers["X-Plex-Token"] = token

    endpoints = [
        # Core identity & status
        ("GET", "/identity"),
        ("GET", "/"),
        ("GET", "/status"),
        ("GET", "/status/sessions"),
        ("GET", "/status/sessions/history"),
        ("GET", "/status/transcodes/active"),

        # Library
        ("GET", "/library"),
        ("GET", "/library/sections"),
        ("GET", "/library/onDeck"),
        ("GET", "/library/recentlyAdded"),
        ("GET", "/library/search?query=test"),

        # System
        ("GET", "/system/agents"),
        ("GET", "/system/devices"),
        ("GET", "/system/updates"),

        # Accounts & users
        ("GET", "/accounts"),
        ("GET", "/myplex/account"),
        ("GET", "/home/users"),

        # Media providers
        ("GET", "/media/providers"),
        ("GET", "/media/providers/search?query=test"),

        # Hubs
        ("GET", "/hubs"),
        ("GET", "/hubs/home"),
        ("GET", "/hubs/home/recentlyAdded"),
        ("GET", "/hubs/sections/all"),

        # Clients & resources
        ("GET", "/clients"),
        ("GET", "/resources"),
        ("GET", "/servers"),
        ("GET", "/devices"),

        # Channels & plugins
        ("GET", "/channels/all"),
        ("GET", "/channels/recentlyViewed"),

        # Playlists
        ("GET", "/playlists"),

        # Sync
        ("GET", "/sync/items"),
        ("GET", "/sync/transcodeQueue"),

        # Butlers & tasks
        ("GET", "/butler"),
        ("GET", "/butler/tasks"),
        ("GET", "/butler/statistics"),

        # Preferences & settings
        ("GET", "/:/prefs"),
        ("GET", "/:/plugins"),
        ("GET", "/:/prefs?X-Plex-Token=dummy"),

        # Statistics
        ("GET", "/statistics/resources"),
        ("GET", "/statistics/bandwidth"),

        # Services
        ("GET", "/services/browse"),

        # Photo transcoder
        ("GET", "/photo/:/transcode?url=/&width=100&height=100"),

        # Timeline
        ("GET", "/player/timeline/poll"),

        # Diagnostics
        ("GET", "/diagnostics/logs"),
        ("GET", "/diagnostics/sections"),

        # Actions
        ("POST", "/actions/scan"),
        ("POST", "/actions/scan?force=1"),
        ("GET", "/actions/generateMediaIndex"),

        # WebSocket (upgrade only; proxy captures the upgrade)
        # This will 400 without WS upgrade headers but still registers the path
        ("GET", "/:/websockets/notifications"),
    ]

    print(f"[TRAFFIC] Hitting {len(endpoints)} endpoints via {base} ...", file=sys.stderr)
    for method, path in endpoints:
        status, body = fetch(base, path, method=method, headers=headers)
        indicator = "✓" if status == 200 else "○" if status in (401, 403) else "✗"
        print(f"  {indicator} {method} {path} -> {status}", file=sys.stderr)
        time.sleep(0.1)

    print("[TRAFFIC] Done.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Plex traffic")
    parser.add_argument("--base", default="http://localhost:8080", help="Proxy base URL")
    parser.add_argument("--token", default=None, help="X-Plex-Token for authenticated requests")
    args = parser.parse_args()
    run(args.base, args.token)


if __name__ == "__main__":
    main()
