#!/usr/bin/env python3
"""Iron Ledger CLI — Import bodybuilding routines into Hevy."""

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict

from iron_ledger.utils.logger import setup_logger
from iron_ledger.importer.validator import validate_program, ValidationError
from iron_ledger.exceptions import ApiError, MappingError, IronLedgerError

logger = setup_logger()

DEFAULT_WORKOUT = Path(__file__).parent / "iron_ledger" / "workouts" / "periodizacao_ab.py"


def load_program(filepath: str) -> Dict[str, Any]:
    """Dynamically load a PROGRAM dict from a Python file."""
    path = Path(filepath).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"Workout file not found: {path}")

    spec = importlib.util.spec_from_file_location("workout_module", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    program = getattr(module, "PROGRAM", None)
    if program is None:
        raise ValueError(f"File does not define a PROGRAM dict: {path}")

    return program


def cmd_upload(args: argparse.Namespace) -> None:
    filepath = args.path or str(DEFAULT_WORKOUT)

    logger.info(f"Loading program from {filepath}")
    program = load_program(filepath)

    if args.dry_run:
        logger.info("Dry-run mode — validation only")
        errors = validate_program(program, raise_on_error=False)
        if errors:
            logger.error(f"Validation failed with {len(errors)} error(s):")
            for e in errors:
                logger.error(f"  • {e}")
            sys.exit(1)
        else:
            logger.info("✓ Validation passed. Program is ready for upload.")
        return

    # Full import
    from iron_ledger.config import load_config
    from iron_ledger.importer.importer import ProgramImporter

    config = load_config()
    importer = ProgramImporter(config)
    result = importer.import_program(program, folder_name=args.folder)

    if result.warnings:
        logger.warning("Warnings:")
        for w in result.warnings:
            logger.warning(f"  • {w}")

    logger.info(
        f"Done. {result.workouts_created} routine(s), "
        f"{result.exercises_mapped} exercise(s) imported."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="iron-ledger",
        description="Iron Ledger — Every set. Every rep. Accounted for.",
    )
    subparsers = parser.add_subparsers(dest="command")

    upload_parser = subparsers.add_parser("upload", help="Upload a workout program to Hevy")
    upload_parser.add_argument("path", nargs="?", help="Path to workout file (default: periodizacao_ab.py)")
    upload_parser.add_argument("--dry-run", action="store_true", help="Validate without uploading")
    upload_parser.add_argument("--folder", type=str, default=None, help="Hevy folder name for routines")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "upload":
            cmd_upload(args)
    except (FileNotFoundError, ImportError, ValueError) as e:
        logger.error(str(e))
        sys.exit(1)
    except ValidationError as e:
        logger.error(str(e))
        sys.exit(1)
    except ApiError as e:
        logger.error(f"API error: {e}")
        if e.response:
            logger.error(f"Response: {e.response}")
        sys.exit(1)
    except IronLedgerError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted.")
        sys.exit(130)


if __name__ == "__main__":
    main()
