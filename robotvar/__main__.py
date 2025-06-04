"""RoboTvar - Font merger for Roboto and TossFace fonts.

This module provides command-line interface for the RoboTvar font creation process.
"""

import argparse
import sys
from pathlib import Path
import traceback



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
        "--compare-fonts",
        action="store_true",
        help="Compare character sets between two fonts",
    )
    parser.add_argument(
        "--font1",
        type=Path,
        help="First font file for comparison",
    )
    parser.add_argument(
        "--font2",
        type=Path,
        help="Second font file for comparison",
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
    exclusive_args = sum(
        [args.download_only, args.merge_only, args.test_app, args.compare_fonts]
    )
    if exclusive_args > 1:
        print(
            "Error: Can only specify one of: --download-only, --merge-only, --test-app, --compare-fonts",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.compare_fonts:
        if not args.font1 or not args.font2:
            print(
                "Error: Both --font1 and --font2 must be specified with --compare-fonts",
                file=sys.stderr,
            )
            sys.exit(1)
        from .scripts.compare_sources import compare_fonts

        compare_fonts(args.font1, args.font2)
        return

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
        print("Error occurred:")
        traceback.print_exc()
        sys.exit(1)



if __name__ == "__main__":
    main()
