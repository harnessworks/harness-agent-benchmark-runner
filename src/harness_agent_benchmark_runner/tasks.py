from __future__ import annotations

import json
from pathlib import Path

from .models import TaskSpec


def load_task(path: str | Path) -> TaskSpec:
    task_path = Path(path).expanduser().resolve()
    if task_path.suffix.lower() != ".json":
        raise ValueError(
            f"unsupported task file extension {task_path.suffix!r}; "
            "the initial runner supports JSON task specs"
        )

    data = json.loads(task_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("task spec must be a JSON object")
    return TaskSpec.from_dict(data, source_path=task_path)
