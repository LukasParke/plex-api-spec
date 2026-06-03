#!/usr/bin/env python3
"""
Safely extract duplicate inline schemas into reusable components.
Only replaces EXACT full-schema matches, never partial matches inside allOf/oneOf.
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

def find_exact_matches(obj, target, path="", matches=None):
    """Find exact dict matches and return their paths."""
    if matches is None:
        matches = []
    if isinstance(obj, dict):
        if obj == target:
            matches.append(path)
        for k, v in obj.items():
            find_exact_matches(v, target, f"{path}.{k}", matches)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_exact_matches(item, target, f"{path}[{i}]", matches)
    return matches

def set_at_path(obj, path, value):
    """Set a value at a dotted path like paths./users.get.responses.200.content."""
    parts = path.strip(".").split(".")
    current = obj
    for part in parts[:-1]:
        if part.startswith("[") and part.endswith("]"):
            idx = int(part[1:-1])
            current = current[idx]
        else:
            current = current[part]
    last = parts[-1]
    if last.startswith("[") and last.endswith("]"):
        idx = int(last[1:-1])
        current[idx] = value
    else:
        current[last] = value

def main():
    spec = load_spec()
    schemas = spec.setdefault("components", {}).setdefault("schemas", {})

    # 1. Extract the full 401 error response schema
    # Find the first 401 response and use it as the canonical version
    error_401_schema = None
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if "401" in op.get("responses", {}):
                content = op["responses"]["401"].get("content", {})
                if "application/json" in content:
                    error_401_schema = copy.deepcopy(content["application/json"].get("schema"))
                    break
        if error_401_schema:
            break

    if error_401_schema:
        schemas["UnauthorizedErrorResponse"] = error_401_schema
        # Replace all matching 401 response schemas
        for path, methods in spec.get("paths", {}).items():
            for method, op in methods.items():
                if "401" in op.get("responses", {}):
                    content = op["responses"]["401"].get("content", {})
                    if "application/json" in content:
                        if content["application/json"].get("schema") == error_401_schema:
                            content["application/json"]["schema"] = {"$ref": "#/components/schemas/UnauthorizedErrorResponse"}

    # 2. Extract the full 400 error response schema
    error_400_schema = None
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if "400" in op.get("responses", {}):
                content = op["responses"]["400"].get("content", {})
                if "application/json" in content:
                    error_400_schema = copy.deepcopy(content["application/json"].get("schema"))
                    break
        if error_400_schema:
            break

    if error_400_schema:
        schemas["BadRequestErrorResponse"] = error_400_schema
        for path, methods in spec.get("paths", {}).items():
            for method, op in methods.items():
                if "400" in op.get("responses", {}):
                    content = op["responses"]["400"].get("content", {})
                    if "application/json" in content:
                        if content["application/json"].get("schema") == error_400_schema:
                            content["application/json"]["schema"] = {"$ref": "#/components/schemas/BadRequestErrorResponse"}

    # 3. Extract the full 200 response schema for /livetv/dvrs endpoints
    # These all have the same MediaContainerWithStatus + DVR wrapper
    dvr_response_schema = None
    dvr_endpoints = [
        ("/livetv/dvrs", "get"),
        ("/livetv/dvrs/{dvrId}", "get"),
        ("/livetv/dvrs/{dvrId}/lineups", "delete"),
        ("/livetv/dvrs/{dvrId}/lineups", "put"),
        ("/livetv/dvrs/{dvrId}/prefs", "put"),
        ("/livetv/dvrs/{dvrId}/lineups", "post"),
        ("/livetv/dvrs/{dvrId}/prefs", "get"),
        ("/livetv/dvrs/{dvrId}/refresh", "get"),
    ]
    for path, method in dvr_endpoints:
        if path in spec.get("paths", {}) and method in spec["paths"][path]:
            content = spec["paths"][path][method].get("responses", {}).get("200", {}).get("content", {})
            if "application/json" in content:
                dvr_response_schema = copy.deepcopy(content["application/json"].get("schema"))
                break

    if dvr_response_schema:
        schemas["DVRResponse"] = dvr_response_schema
        for path, method in dvr_endpoints:
            if path in spec.get("paths", {}) and method in spec["paths"][path]:
                content = spec["paths"][path][method].get("responses", {}).get("200", {}).get("content", {})
                if "application/json" in content:
                    if content["application/json"].get("schema") == dvr_response_schema:
                        content["application/json"]["schema"] = {"$ref": "#/components/schemas/DVRResponse"}

    # 4. Extract Channel response schema
    channel_response_schema = None
    for path in ["/livetv/epg/channels", "/livetv/epg/lineupchannels"]:
        if path in spec.get("paths", {}):
            content = spec["paths"][path].get("get", {}).get("responses", {}).get("200", {}).get("content", {})
            if "application/json" in content:
                channel_response_schema = copy.deepcopy(content["application/json"].get("schema"))
                break

    if channel_response_schema:
        schemas["ChannelResponse"] = channel_response_schema
        for path in ["/livetv/epg/channels", "/livetv/epg/lineupchannels"]:
            if path in spec.get("paths", {}):
                content = spec["paths"][path].get("get", {}).get("responses", {}).get("200", {}).get("content", {})
                if "application/json" in content:
                    if content["application/json"].get("schema") == channel_response_schema:
                        content["application/json"]["schema"] = {"$ref": "#/components/schemas/ChannelResponse"}

    save_spec(spec)
    print(f"Total schemas: {len(schemas)}")
    print("Done. Run prettier and speakeasy lint to validate.")

if __name__ == "__main__":
    main()
