"""RoboTvar - Font merger for Roboto and TossFace fonts.

This module provides command-line interface for the RoboTvar font creation process.
"""

import argparse
import sys
from pathlib import Path
import traceback





def parse_args():
    parser = argparse.ArgumentParser(
        description="Create RoboTvar fonts by merging Roboto with TossFace or Twemoji emoji fonts"
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download the required fonts without merging",
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Only merge existing fonts without downloading (default: TossFace emoji merge)",
    )
    parser.add_argument(
        "--merge-twemoji",
        action="store_true",
        help="Merge Roboto with Twemoji emoji font instead of TossFace",
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
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete the merged folder and exit",
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all font folders in the fonts directory and exit",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Handle delete/reset actions first
    if args.delete or args.delete_all:
        from .scripts.reset import delete_merged_folder, delete_all_fonts, delete_screenshots_folder
        if args.delete:
            merged_dir = args.output_dir
            delete_merged_folder(merged_dir)
        if args.delete_all:
            fonts_dir = Path(__file__).parent / "fonts"
            screenshots_folder = Path(__file__).parent / "screenshots"
            delete_screenshots_folder(screenshots_folder)
            delete_merged_folder(args.output_dir)
            delete_all_fonts(fonts_dir)
        return
    
    exclusive_args = sum(
        [args.download_only, args.merge_only, args.merge_twemoji, args.test_app, args.compare_fonts]
    )
    if exclusive_args > 1:
        print(
            "Error: Can only specify one of: --download-only, --merge-only, --merge-twemoji, --test-app, --compare-fonts",
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
            if not args.merge_only and not args.merge_twemoji:
                from .scripts.download import download_fonts
                download_fonts()

            if not args.download_only:
                if args.merge_twemoji:
                    from .scripts.merge_robot_and_twemoji import merge_all_fonts as merge_twemoji_fonts
                    merge_twemoji_fonts(output_dir=args.output_dir)
                else:
                    from .scripts.merge import merge_all_fonts as merge_tossface_fonts
                    merge_tossface_fonts(output_dir=args.output_dir)

    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()
        sys.exit(1)



if __name__ == "__main__":
    main()
