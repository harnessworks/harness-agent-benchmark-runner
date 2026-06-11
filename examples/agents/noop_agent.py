#!/usr/bin/env python3
from __future__ import annotations

import os


def main() -> int:
    print(f"noop agent received task: {os.environ.get('BENCHMARK_TASK_ID', 'unknown')}")
    print(f"repo: {os.environ.get('BENCHMARK_REPO', 'unknown')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
