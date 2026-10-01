from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from .command_rail import compile_command_rail, write_datapack
from .contracts import run_contracts
from .master import load_master_events
from .registry import InstrumentRegistry
from .validate import validate_generated_pack, validate_repo


def _report_validation(report) -> int:
    print(
        json.dumps(
            {
                "ok": report.ok,
                "checks": report.checks,
                "errors": report.errors,
                "warnings": report.warnings,
                "contracts": report.contract_summary,
            },
            indent=2,
        )
    )
    return 0 if report.ok else 1


def cmd_compile(args) -> int:
    repo = Path(args.repo_root).resolve()
    master_path = Path(args.master)
    if not master_path.is_absolute():
        master_path = repo / master_path

    _, events = load_master_events(master_path)
    registry = InstrumentRegistry.load(repo, args.profile)
    compilation = compile_command_rail(
        events,
        registry,
        qpm=args.qpm,
        tps=args.tps,
        pulse_ticks=args.pulse_ticks,
        busy_window_ticks=args.busy_window_ticks,
        instrument_gap=args.instrument_gap,
        profile=args.profile,
    )

    out = Path(args.output).resolve()
    write_datapack(
        compilation,
        registry,
        out,
        namespace=args.namespace,
        title=args.title,
        required_tps=args.tps,
    )
    validation = validate_generated_pack(out)
    if not validation.ok:
        print(json.dumps({"errors": validation.errors}, indent=2), file=sys.stderr)
        return 1

    zip_path = None
    if args.zip:
        zip_base = str(out)
        zip_path = Path(shutil.make_archive(zip_base, "zip", root_dir=out))

    print(
        json.dumps(
            {
                "output": str(out),
                "zip": str(zip_path) if zip_path else None,
                "metrics": compilation.metrics,
                "validation_checks": validation.checks,
            },
            indent=2,
        )
    )
    return 0


def cmd_validate_repo(args) -> int:
    report = validate_repo(
        Path(args.root),
        minimum_semantic_contracts=args.minimum_semantic_contracts,
    )
    return _report_validation(report)


def cmd_validate_pack(args) -> int:
    return _report_validation(validate_generated_pack(Path(args.path)))


def cmd_contracts(args) -> int:
    results = run_contracts(Path(args.root).resolve())
    payload = [
        {
            "test_id": x.test_id,
            "path": x.path,
            "status": x.status,
            "checks": x.checks,
            "failures": x.failures,
            "note": x.note,
        }
        for x in results
    ]
    print(json.dumps(payload, indent=2))
    return 1 if any(x.status == "FAIL" for x in results) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="blockscore")
    sub = parser.add_subparsers(dest="command", required=True)

    compile_p = sub.add_parser(
        "compile-command-rail",
        help="Compile existing Minecraft Master events into a physical Command Rail datapack.",
    )
    compile_p.add_argument("master")
    compile_p.add_argument("--repo-root", default=".")
    compile_p.add_argument("--profile", default="java-26.2")
    compile_p.add_argument("--qpm", type=int, required=True)
    compile_p.add_argument("--tps", type=int, default=20)
    compile_p.add_argument("--pulse-ticks", type=int, default=1)
    compile_p.add_argument("--busy-window-ticks", type=int, default=2)
    compile_p.add_argument("--instrument-gap", type=int, default=1)
    compile_p.add_argument("--namespace", default="blockscore_generated")
    compile_p.add_argument("--title", default="Generated Song")
    compile_p.add_argument("--output", required=True)
    compile_p.add_argument("--zip", action="store_true")
    compile_p.set_defaults(func=cmd_compile)

    validate_p = sub.add_parser("validate-repo")
    validate_p.add_argument("root", nargs="?", default=".")
    validate_p.add_argument("--minimum-semantic-contracts", type=int, default=12)
    validate_p.set_defaults(func=cmd_validate_repo)

    pack_p = sub.add_parser("validate-pack")
    pack_p.add_argument("path")
    pack_p.set_defaults(func=cmd_validate_pack)

    contract_p = sub.add_parser("contracts")
    contract_p.add_argument("root", nargs="?", default=".")
    contract_p.set_defaults(func=cmd_contracts)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

