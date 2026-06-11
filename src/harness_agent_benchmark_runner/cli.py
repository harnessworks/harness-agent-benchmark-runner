from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import RunnerConfig
from .runner import run_task
from .summary import format_summary, load_results, summarize_results
from .tasks import load_task


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        task = load_task(args.task)
        config = RunnerConfig(
            agent_command=args.agent_command,
            workspace_root=Path(args.workspace),
            results_dir=Path(args.results),
            keep_runs=not args.delete_run_dir,
            default_command_timeout_seconds=args.command_timeout,
            repo_source_override=args.repo_source,
            repo_ref_override=args.repo_ref,
        )
        result = run_task(task, config)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            scoring = result["scoring"]
            print(f"run_id: {result['run_id']}")
            print(f"success: {scoring.get('success')}")
            print(f"verification_passed: {scoring.get('verification_passed')}")
            print(f"wrong_file_edits: {scoring.get('wrong_file_edits')}")
            print(f"forbidden_file_edits: {scoring.get('forbidden_file_edits')}")
        return 0 if result["scoring"].get("success") is True else 1

    if args.command == "summarize":
        records = load_results(args.results)
        summary = summarize_results(records)
        if args.json:
            print(json.dumps(summary, indent=2, sort_keys=True))
        else:
            print(format_summary(summary))
        return 0

    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness-agent-benchmark",
        description="Run isolated coding-agent benchmark tasks and summarize results.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run one benchmark task")
    run_parser.add_argument("--task", required=True, help="path to JSON task spec")
    run_parser.add_argument(
        "--agent-command",
        required=True,
        help="shell command to execute as the agent inside the isolated clone",
    )
    run_parser.add_argument("--workspace", default="runs", help="directory for isolated run workspaces")
    run_parser.add_argument("--results", default="results", help="directory for JSONL result files")
    run_parser.add_argument("--repo-source", help="override task repo.source")
    run_parser.add_argument("--repo-ref", help="override task repo.ref")
    run_parser.add_argument("--command-timeout", type=int, default=300)
    run_parser.add_argument("--delete-run-dir", action="store_true")
    run_parser.add_argument("--json", action="store_true", help="print full result JSON")

    summary_parser = subparsers.add_parser("summarize", help="summarize JSONL benchmark results")
    summary_parser.add_argument("--results", default="results", help="JSONL file or results directory")
    summary_parser.add_argument("--json", action="store_true", help="print summary JSON")

    return parser
