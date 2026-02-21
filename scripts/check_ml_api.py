#!/usr/bin/env python3
"""
Check that the ML API is running and can serve recommendations for any user.
Run from project root: python scripts/check_ml_api.py [base_url]
Default base_url: http://127.0.0.1:8000
"""
import sys
import urllib.request
import urllib.error
import json

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"


def get(path: str) -> dict:
    req = urllib.request.Request(f"{BASE}{path}")
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())


def main():
    print(f"Checking ML API at {BASE}")
    errors = []

    # 1. Health
    try:
        r = get("/health")
        assert r.get("status") == "ok"
        print("  /health OK")
    except Exception as e:
        errors.append(f"/health failed: {e}")
        print(f"  /health FAIL: {e}")
        sys.exit(1)

    # 2. Ready (model loaded, user range)
    try:
        r = get("/ready")
        assert r.get("status") == "ready" and r.get("model_loaded") is True
        num_users = r.get("num_users")
        print(f"  /ready OK (num_users={num_users})")
    except urllib.error.HTTPError as e:
        if e.code == 503:
            errors.append("/ready 503 (model not loaded?)")
        else:
            errors.append(f"/ready {e.code}: {e.read().decode()}")
        print(f"  /ready FAIL: {errors[-1]}")
        sys.exit(1)
    except Exception as e:
        errors.append(f"/ready failed: {e}")
        print(f"  /ready FAIL: {e}")
        sys.exit(1)

    # 3. Recommend for user 1 and for last user
    for uid in [1, num_users]:
        try:
            r = get(f"/recommend?user_id={uid}&top_k=5")
            ids = r.get("movie_ids", [])
            assert isinstance(ids, list) and len(ids) <= 5
            print(f"  /recommend user_id={uid} OK (got {len(ids)} movies)")
        except Exception as e:
            errors.append(f"/recommend user_id={uid}: {e}")
            print(f"  /recommend user_id={uid} FAIL: {e}")

    # 4. Invalid user should 400
    try:
        urllib.request.urlopen(urllib.request.Request(f"{BASE}/recommend?user_id=9999"), timeout=5)
        errors.append("Expected 400 for user_id=9999")
        print("  /recommend user_id=9999 FAIL (expected 400)")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("  /recommend user_id=9999 correctly returns 400")
        else:
            errors.append(f"user_id=9999 got {e.code} instead of 400")

    if errors:
        print("\nErrors:", errors)
        sys.exit(1)
    print("\nAll checks passed. Laravel can connect for any user 1–{}.".format(num_users))


if __name__ == "__main__":
    main()
