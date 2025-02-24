"""Font downloader for RoboTvar.

Downloads Roboto and TossFace fonts from their respective GitHub repositories.
"""

import asyncio
from pathlib import Path
import httpx

# Convert GitHub URLs to raw content URLs
ROBOTO_BASE_URL = (
    "https://raw.githubusercontent.com/googlefonts/roboto-2/main/src/hinted"
)
ROBOTO_FONTS = {
    "Roboto-Regular.ttf": f"{ROBOTO_BASE_URL}/Roboto-Regular.ttf",
    "Roboto-Bold.ttf": f"{ROBOTO_BASE_URL}/Roboto-Bold.ttf",
    "Roboto-BoldItalic.ttf": f"{ROBOTO_BASE_URL}/Roboto-BoldItalic.ttf",
    "Roboto-Italic.ttf": f"{ROBOTO_BASE_URL}/Roboto-Italic.ttf",
}

TOSSFACE_URL = (
    "https://raw.githubusercontent.com/toss/tossface/main/dist/TossFaceFontWeb.otf"
)


async def download_font(client: httpx.AsyncClient, url: str, output_path: Path) -> None:
    """Download a font file from the given URL.

    Args:
        client: Async HTTP client
        url: URL to download from
        output_path: Where to save the downloaded font
    """
    try:
        response = await client.get(url)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        print(f"Downloaded: {output_path.name}")
    except httpx.HTTPError as e:
        print(f"Failed to download {output_path.name}: {e}")
        raise


async def download_all_fonts() -> None:
    """Download all required fonts asynchronously."""
    # Create necessary directories
    fonts_dir = Path(__file__).parent.parent / "fonts"
    roboto_dir = fonts_dir / "roboto"
    tossface_dir = fonts_dir / "tossface"

    for directory in [fonts_dir, roboto_dir, tossface_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as client:
        # Download Roboto fonts
        roboto_tasks = [
            download_font(client, url, roboto_dir / filename)
            for filename, url in ROBOTO_FONTS.items()
        ]

        # Download TossFace font
        tossface_task = download_font(
            client, TOSSFACE_URL, tossface_dir / "TossFaceFontWeb.otf"
        )

        # Wait for all downloads to complete
        await asyncio.gather(tossface_task, *roboto_tasks)


def download_fonts() -> None:
    """Entry point for font downloading."""
    try:
        asyncio.run(download_all_fonts())
        print("All fonts downloaded successfully!")
    except Exception as e:
        print(f"Error downloading fonts: {e}")
        raise
