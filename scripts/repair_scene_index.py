"""
Rebuild a cram-viz scenes index.json from the bundles actually present on disk.

A hand-maintained or vendored index can drift from the bundles shipped alongside it -
for example a ``default`` naming a bundle that was renamed or removed. This rescans
every bundle directory and repairs both the scene list and an invalid default, so the
deployed viewer can always load something without requiring a ``?scene=`` query param.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def scene_environment(models: list[dict]) -> str | None:
    """
    The name of a scene's environment, or ``None`` for a bench-only scene.
    """
    environment_models = [model["name"] for model in models if not model["robot"]]
    return "+".join(environment_models) if environment_models else None


def scan_scenes(scenes_dir: Path) -> list[dict]:
    """
    Every scene bundle under ``scenes_dir``, with its robot/environment identity.
    """
    entries = []
    for bundle_dir in sorted(scenes_dir.iterdir()):
        scene_path = bundle_dir / "scene.json"
        if not scene_path.is_file():
            continue
        scene = json.loads(scene_path.read_text(encoding="utf-8"))
        entries.append(
            {
                "name": bundle_dir.name,
                "robot": scene["robot"]["name"],
                "environment": scene_environment(scene["models"]),
            }
        )
    return entries


def main() -> None:
    """
    ``repair_scene_index.py <scenes-dir>/index.json`` - rebuild the index in place.
    """
    index_path = Path(sys.argv[1])
    index = json.loads(index_path.read_text(encoding="utf-8"))
    scenes = scan_scenes(index_path.parent)
    index["scenes"] = scenes
    names = [entry["name"] for entry in scenes]
    if names and index.get("default") not in names:
        index["default"] = names[0]
    index_path.write_text(json.dumps(index, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
