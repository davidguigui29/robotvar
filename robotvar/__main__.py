"""RoboTvar - Font merger for Roboto and TossFace fonts.

This module provides command-line interface for the RoboTvar font creation process.
"""

import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create RoboTvar fonts by merging Roboto with TossFace emoji font"
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download the required fonts without merging",
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Only merge existing fonts without downloading",
    )
    parser.add_argument(
        "--test-app",
        action="store_true",
        help="Run Kivy test application to preview the fonts",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Custom output directory for merged fonts",
        default=Path(__file__).parent / "merged",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate arguments
    exclusive_args = sum([args.download_only, args.merge_only, args.test_app])
    if exclusive_args > 1:
        print(
            "Error: Can only specify one of: --download-only, --merge-only, --test-app",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if args.test_app:
            from .scripts.test_app import run_test_app

            run_test_app(font_dir=args.output_dir)
        else:
            if not args.merge_only:
                from .scripts.download import download_fonts

                download_fonts()

            if not args.download_only:
                from .scripts.merge import merge_all_fonts

                merge_all_fonts(output_dir=args.output_dir)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
