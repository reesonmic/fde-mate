"""
Export OpenAPI Spec from `api/` service to `shared-protos/openapi/api.json`.

Used by:
- Local devs: regenerate after adding/modifying routers
- CI: verify FE types are in sync with BE schema

Usage:
    # 1) Make sure the api/ service can import (have deps installed)
    cd workspace/api && poetry install   # or pip install -r requirements.txt

    # 2) Run the exporter
    cd workspace
    python scripts/export_openapi.py

    # 3) Regenerate FE types
    cd web && npm run gen:types
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent  # workspace/
API_SRC = REPO_ROOT / "api"
OUTPUT = REPO_ROOT / "shared-protos" / "openapi" / "api.json"


def main() -> int:
    sys.path.insert(0, str(API_SRC))

    try:
        # Lazy import so the script fails with a clear hint when api/ deps are missing
        from app.main import app  # type: ignore  # noqa: PLC0415
    except ImportError as exc:
        print(f"[export_openapi] Failed to import api app: {exc}", file=sys.stderr)
        print(
            "[export_openapi] Hint: install api/ deps first "
            "(cd workspace/api && pip install -r requirements.txt)",
            file=sys.stderr,
        )
        return 1

    spec = app.openapi()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2, sort_keys=True)

    routes_count = len(spec.get("paths", {}))
    schemas_count = len(spec.get("components", {}).get("schemas", {}))
    print(
        f"[export_openapi] OK -> {OUTPUT.relative_to(REPO_ROOT)} "
        f"({routes_count} routes, {schemas_count} schemas)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
