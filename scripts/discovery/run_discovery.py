#!/usr/bin/env python3
"""
Orchestrates the full discovery pipeline using Arbiter as the proxy:
  1. Start Arbiter + PMS via docker-compose
  2. Wait for PMS and Arbiter docs server health
  3. Run synthetic traffic generator
  4. Fetch traffic.jsonl and diff report from Arbiter
  5. Stop services
  6. Run local diff_analyzer on captured traffic
  7. Output report and exit with appropriate code
"""

import os
import subprocess
import sys
import time
import json
import urllib.request

COMPOSE_FILE = os.environ.get("COMPOSE_FILE", "docker-compose.yml")
REPORT_PATH = os.environ.get("REPORT_PATH", "/tmp/diff_report.json")
TRAFFIC_PATH = os.environ.get("TRAFFIC_PATH", "/tmp/traffic.jsonl")
ARBITER_DOCS_URL = "http://localhost:9000"

def run(cmd, check=True):
    print(f"[DISCOVERY] {' '.join(cmd)}", file=sys.stderr)
    return subprocess.run(cmd, check=check)

def wait_for_url(url, timeout=180):
    print(f"[DISCOVERY] Waiting for {url} ...", file=sys.stderr)
    for i in range(timeout):
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                if resp.status == 200:
                    print(f"[DISCOVERY] {url} is up.", file=sys.stderr)
                    return True
        except Exception:
            pass
        time.sleep(1)
    print(f"[DISCOVERY] {url} failed to respond.", file=sys.stderr)
    return False

def fetch_jsonl():
    url = f"{ARBITER_DOCS_URL}/traffic.jsonl"
    print(f"[DISCOVERY] Fetching traffic from {url} ...", file=sys.stderr)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            with open(TRAFFIC_PATH, "wb") as f:
                f.write(resp.read())
        print(f"[DISCOVERY] Traffic saved to {TRAFFIC_PATH}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"[DISCOVERY] Failed to fetch traffic: {e}", file=sys.stderr)
        return False

def fetch_diff():
    url = f"{ARBITER_DOCS_URL}/diff"
    print(f"[DISCOVERY] Fetching diff from {url} ...", file=sys.stderr)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())
        with open(REPORT_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[DISCOVERY] Diff report saved to {REPORT_PATH}", file=sys.stderr)
        return data
    except Exception as e:
        print(f"[DISCOVERY] Failed to fetch diff: {e}", file=sys.stderr)
        return None

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("../..")  # Back to project root

    # 1. Start services
    run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"])

    # 2. Wait for PMS and Arbiter
    pms_ok = wait_for_url("http://localhost:32400/identity")
    arbiter_ok = wait_for_url(f"{ARBITER_DOCS_URL}/openapi.json", timeout=60)

    if not pms_ok:
        run(["docker", "compose", "-f", COMPOSE_FILE, "logs", "pms"])
        run(["docker", "compose", "-f", COMPOSE_FILE, "down"])
        sys.exit(1)

    if not arbiter_ok:
        run(["docker", "compose", "-f", COMPOSE_FILE, "logs", "proxy"])
        run(["docker", "compose", "-f", COMPOSE_FILE, "down"])
        sys.exit(1)

    # 3. Run synthetic traffic generator
    print("[DISCOVERY] Running synthetic traffic generator...", file=sys.stderr)
    result = subprocess.run([
        sys.executable,
        "scripts/discovery/generate_traffic.py",
        "--base", "http://localhost:8080",
    ])
    if result.returncode != 0:
        print("[DISCOVERY] Traffic generation failed, continuing anyway...", file=sys.stderr)

    # 4. Fetch outputs from Arbiter
    fetch_jsonl()
    arbiter_diff = fetch_diff()

    # 5. Stop services
    run(["docker", "compose", "-f", COMPOSE_FILE, "down"])

    # 6. Run local diff analyzer as fallback / cross-check
    print("[DISCOVERY] Running local diff analyzer...", file=sys.stderr)
    result = subprocess.run([sys.executable, "scripts/discovery/diff_analyzer.py"])

    # 7. Output report summary
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH) as f:
            report = json.load(f)
        print(json.dumps(report.get("summary", report), indent=2))
    elif arbiter_diff:
        print(json.dumps(arbiter_diff.get("summary", arbiter_diff), indent=2))

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
