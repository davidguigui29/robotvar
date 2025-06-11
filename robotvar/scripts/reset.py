import shutil
from pathlib import Path

def delete_merged_folder(merged_dir: Path):
    if merged_dir.exists() and merged_dir.is_dir():
        print(f"Deleting merged folder: {merged_dir}")
        shutil.rmtree(merged_dir)
        print("Merged folder deleted.")
    else:
        print("Merged folder does not exist.")

def delete_all_fonts(fonts_dir: Path):
    if fonts_dir.exists() and fonts_dir.is_dir():
        print(f"Deleting all font folders in: {fonts_dir}")
        for child in fonts_dir.iterdir():
            if child.is_dir():
                print(f"Deleting: {child}")
                shutil.rmtree(child)
        print("All font folders deleted.")
    else:
        print("Fonts directory does not exist.")

# Delete all files in the screenshots folder if it exists except .gitkeep
def delete_screenshots_folder_content(screenshots_dir: Path):
    if screenshots_dir.exists() and screenshots_dir.is_dir():
        print(f"Deleting screenshots folder content: {screenshots_dir}")
        for child in screenshots_dir.iterdir():
            if child.is_file() and child.name != ".gitkeep":
                print(f"Deleting: {child}")
                child.unlink()
        print("Screenshots folder content cleaned (except .gitkeep).")
    else:
        print("Screenshots folder does not exist.")