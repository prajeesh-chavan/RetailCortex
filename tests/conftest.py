import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "src" / "schemas"

ENTITY_NAMES = sorted(
    f.stem.replace("_schema", "")
    for f in SCHEMA_DIR.glob("*_schema.py")
    if f.stem != "__init__"
)
