#!/usr/bin/env python3
"""Cliente mínimo para la API v2 de GoHighLevel (LeadConnector).

Uso:
    python3 scripts/ghl.py GET /locations/search limit=100
    python3 scripts/ghl.py POST /contacts/ --json '{"locationId":"...","email":"a@b.com"}'
    python3 scripts/ghl.py --client ACME GET /contacts/ limit=20   # token de subcuenta

Tokens por cliente en .env:  GHL_CLIENT_<ALIAS>_PIT  y  GHL_CLIENT_<ALIAS>_LOCATION
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env():
    env = {}
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    env.update({k: v for k, v in os.environ.items() if k.startswith("GHL_")})
    return env


ENV = load_env()
BASE = ENV.get("GHL_API_BASE", "https://services.leadconnectorhq.com")
VERSION = ENV.get("GHL_API_VERSION", "2021-07-28")
TOKEN = ENV.get("GHL_PIT")


def request(method, path, params=None, body=None, token=None):
    url = BASE.rstrip("/") + "/" + path.lstrip("/")
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + (token or TOKEN))
    req.add_header("Version", VERSION)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "kaizen-ghl-client/1.0")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"raw": raw}


def paginate(path, params=None, key=None, limit=100):
    """Recorre endpoints paginados por skip/limit y devuelve la lista completa."""
    params = dict(params or {})
    out, skip = [], 0
    while True:
        params.update({"limit": limit, "skip": skip})
        status, body = request("GET", path, params)
        if status >= 400:
            raise RuntimeError(f"{status} {body}")
        k = key or next(k for k, v in body.items() if isinstance(v, list))
        batch = body.get(k) or []
        out.extend(batch)
        if len(batch) < limit:
            return out
        skip += limit


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    argv = list(argv)
    token = None
    if argv[1] == "--client":
        alias = argv[2].upper()
        token = ENV.get(f"GHL_CLIENT_{alias}_PIT")
        if not token:
            print(f"Falta GHL_CLIENT_{alias}_PIT en .env")
            return 1
        loc = ENV.get(f"GHL_CLIENT_{alias}_LOCATION")
        argv = [argv[0]] + argv[3:]
    else:
        loc = None
    method, path = argv[1].upper(), argv[2]
    params, body = {}, None
    rest = argv[3:]
    while rest:
        arg = rest.pop(0)
        if arg == "--json":
            body = json.loads(rest.pop(0))
        elif "=" in arg:
            k, v = arg.split("=", 1)
            params[k] = v
    if loc and method == "GET" and "locationId" not in params:
        params["locationId"] = loc
    status, data = request(method, path, params, body, token=token)
    print(f"HTTP {status}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0 if status < 400 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
