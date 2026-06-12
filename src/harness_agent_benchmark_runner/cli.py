from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import RunnerConfig
from .runner import run_task_with_retries
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
            max_attempts_override=args.max_attempts,
            agent_timeout_override_seconds=args.agent_timeout_override,
            max_agent_timeout_seconds=args.max_agent_timeout,
            agent_stall_timeout_seconds=args.agent_stall_timeout,
            agent_idle_timeout_seconds=args.agent_idle_timeout,
            agent_no_edit_timeout_seconds=args.agent_no_edit_timeout,
            max_cost_usd_override=args.max_cost_usd,
            repo_source_override=args.repo_source,
            repo_ref_override=args.repo_ref,
        )
        results = run_task_with_retries(task, config)
        result = results[-1]
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            scoring = result["scoring"]
            print(f"run_id: {result['run_id']}")
            print(f"attempts: {len(results)}/{result['attempt']['limit']}")
            print(f"success: {scoring.get('success')}")
            print(f"functional_success: {scoring.get('functional_success')}")
            print(f"schema_contract_success: {scoring.get('schema_contract_success')}")
            print(f"workflow_success: {scoring.get('workflow_success')}")
            print(f"strict_success: {scoring.get('strict_success', scoring.get('success'))}")
            print(f"preflight_passed: {scoring.get('preflight_passed')}")
            print(f"verification_passed: {scoring.get('verification_passed')}")
            print(f"agent_stalled: {scoring.get('agent_stalled')}")
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
    run_parser.add_argument(
        "--command-timeout",
        type=positive_int_arg,
        default=300,
        help="timeout in seconds for runner-owned git and verification commands",
    )
    run_parser.add_argument(
        "--max-attempts",
        type=positive_int_arg,
        help="override task max_attempts; each attempt uses a fresh isolated clone",
    )
    run_parser.add_argument(
        "--max-agent-timeout",
        type=positive_int_arg,
        help="cap the task agent timeout in seconds",
    )
    run_parser.add_argument(
        "--agent-timeout-override",
        type=positive_int_arg,
        help="replace the task agent timeout in seconds before applying --max-agent-timeout",
    )
    run_parser.add_argument(
        "--agent-stall-timeout",
        type=positive_int_arg,
        help="shorter pilot watchdog timeout; records agent_stalled when it fires",
    )
    run_parser.add_argument(
        "--agent-idle-timeout",
        type=positive_int_arg,
        help="idle-output watchdog timeout for agent processes; records agent_stalled when it fires",
    )
    run_parser.add_argument(
        "--agent-no-edit-timeout",
        type=positive_int_arg,
        help="no-repository-change watchdog timeout for agent processes; records agent_stalled when it fires",
    )
    run_parser.add_argument(
        "--max-cost-usd",
        type=non_negative_float_arg,
        help="budget hint passed to adapters as BENCHMARK_MAX_COST_USD",
    )
    run_parser.add_argument("--delete-run-dir", action="store_true")
    run_parser.add_argument("--json", action="store_true", help="print full result JSON")

    summary_parser = subparsers.add_parser("summarize", help="summarize JSONL benchmark results")
    summary_parser.add_argument("--results", default="results", help="JSONL file or results directory")
    summary_parser.add_argument("--json", action="store_true", help="print summary JSON")

    return parser


def positive_int_arg(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def non_negative_float_arg(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be greater than or equal to 0")
    return parsed
