#!/usr/bin/env python3
"""
Diff Analyzer — Compare captured traffic against the OpenAPI spec.
Produces a structured gap report (JSON) of missing endpoints, methods, and query params.
"""

import json
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
import yaml

SPEC_PATH = os.environ.get("SPEC_PATH", "plex-api-spec.yaml")
TRAFFIC_PATH = os.environ.get("TRAFFIC_PATH", "/tmp/traffic.jsonl")
REPORT_PATH = os.environ.get("REPORT_PATH", "/tmp/diff_report.json")


def load_spec(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def normalize_path(path):
    """Normalize URL path by replacing dynamic segments with placeholders."""
    # Collapse consecutive digits or UUID-like segments into {id}
    # Plex uses numeric IDs, GUIDs, and string keys as path params
    segments = []
    for seg in path.strip("/").split("/"):
        if re.match(r"^\d+$", seg):
            segments.append("{id}")
        elif re.match(r"^[0-9a-fA-F-]{20,}$", seg):
            segments.append("{guid}")
        elif re.match(r"^[0-9a-zA-Z_-]{30,}$", seg):
            # Likely a token or key
            segments.append("{key}")
        else:
            segments.append(seg)
    return "/" + "/".join(segments)


def extract_spec_paths(spec):
    """Extract set of (normalized_path, method) from spec."""
    paths = spec.get("paths", {})
    spec_set = set()
    for path, methods in paths.items():
        norm = normalize_path(path)
        for method in methods:
            if method.lower() in ("get", "post", "put", "delete", "patch", "options"):
                spec_set.add((norm, method.upper()))
    return spec_set


def extract_traffic_paths(traffic_path):
    """Extract set of (normalized_path, method) from captured traffic."""
    traffic_set = set()
    path_methods = defaultdict(set)
    path_params = defaultdict(set)
    with open(traffic_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            raw_path = urlparse(entry["path"]).path
            norm = normalize_path(raw_path)
            method = entry["method"].upper()
            traffic_set.add((norm, method))
            path_methods[norm].add(method)

            # Track query params
            qs = parse_qs(urlparse(entry["path"]).query)
            for key in qs:
                path_params[(norm, method)].add(key)
    return traffic_set, path_methods, path_params


def build_report(spec_set, traffic_set, path_methods, path_params, spec):
    missing_in_spec = traffic_set - spec_set
    # Also check for methods on known paths that are missing
    missing_methods = []
    for (norm_path, method) in missing_in_spec:
        missing_methods.append({
            "path": norm_path,
            "method": method,
            "query_params_seen": sorted(path_params.get((norm_path, method), [])),
        })

    # Identify paths in spec never hit during capture (potential dead code or untested)
    spec_only = spec_set - traffic_set

    # Query param gaps: for paths+methods present in both, which query params are missing from spec?
    spec_paths_obj = spec.get("paths", {})
    param_gaps = []
    for (norm_path, method) in (spec_set & traffic_set):
        # Find the actual spec path that matches norm_path
        spec_entry = None
        for spath, smethods in spec_paths_obj.items():
            if normalize_path(spath) == norm_path and method.lower() in smethods:
                spec_entry = smethods[method.lower()]
                break
        if not spec_entry:
            continue
        spec_params = set()
        for p in spec_entry.get("parameters", []):
            if p.get("in") == "query":
                spec_params.add(p.get("name"))
        seen_params = path_params.get((norm_path, method), set())
        missing_params = seen_params - spec_params
        if missing_params:
            param_gaps.append({
                "path": norm_path,
                "method": method,
                "missing_query_params": sorted(missing_params),
            })

    return {
        "summary": {
            "endpoints_in_spec": len(spec_set),
            "endpoints_captured": len(traffic_set),
            "missing_from_spec": len(missing_methods),
            "untested_in_spec": len(spec_only),
            "query_param_gaps": len(param_gaps),
        },
        "missing_endpoints": sorted(missing_methods, key=lambda x: (x["path"], x["method"])),
        "untested_endpoints": sorted([{"path": p, "method": m} for p, m in spec_only], key=lambda x: (x["path"], x["method"])),
        "query_param_gaps": sorted(param_gaps, key=lambda x: (x["path"], x["method"])),
    }


def main():
    if not os.path.exists(TRAFFIC_PATH):
        print(f"Traffic file not found: {TRAFFIC_PATH}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(SPEC_PATH):
        print(f"Spec file not found: {SPEC_PATH}", file=sys.stderr)
        sys.exit(1)

    spec = load_spec(SPEC_PATH)
    spec_set = extract_spec_paths(spec)
    traffic_set, path_methods, path_params = extract_traffic_paths(TRAFFIC_PATH)

    report = build_report(spec_set, traffic_set, path_methods, path_params, spec)

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report["summary"], indent=2))
    missing = report["summary"]["missing_from_spec"]
    print(f"\nDiff report written to {REPORT_PATH}")
    if missing > 0:
        print(f"WARNING: {missing} captured endpoint(s) missing from spec.")
        sys.exit(2)
    else:
        print("All captured endpoints are documented in the spec.")


if __name__ == "__main__":
    main()
