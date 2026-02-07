#!/usr/bin/env python3
"""
Organise files in a folder by moving them into subfolders according to their type.
- Define categories of extensions.
- List all files in the target folder.
- For each file, determine its extension and thus its category.
- Create the category folder if it does not exist.
- Move the file to that folder.
"""

import os
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Define categories of extensions (e.g. images, documents, etc.)
# ---------------------------------------------------------------------------

images = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff", ".tif"]
videos = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg"]
documents = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf",
             ".odt", ".ods", ".odp", ".csv", ".md", ".tex"]
audio = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus"]
archives = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"]
executables = [".exe", ".msi", ".bat", ".cmd", ".sh", ".app", ".dmg"]
code = [".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yaml", ".yml",
        ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs", ".rb", ".php"]

# Category name (folder name) → list of extensions
CATEGORIES = {
    "Images": images,
    "Videos": videos,
    "Documents": documents,
    "Audio": audio,
    "Archives": archives,
    "Executables": executables,
    "Code": code,
}

# Build extension (with dot) → category. If an extension appears in several
# categories or none, the file goes to "Others".
OTHERS = "Others"
_ext_to_categories: dict[str, list[str]] = {}
for category_name, extensions in CATEGORIES.items():
    for ext in extensions:
        ext_lower = ext.lower()
        _ext_to_categories.setdefault(ext_lower, []).append(category_name)

EXTENSION_TO_CATEGORY = {
    ext: cats[0] if len(cats) == 1 else OTHERS
    for ext, cats in _ext_to_categories.items()
}


def get_category_for_file(file_path: Path) -> str:
    """file.suffix gives the extension (with dot). Look it up in our map; if not there, "Others"."""
    ext = file_path.suffix.lower()
    return EXTENSION_TO_CATEGORY.get(ext, OTHERS)


def organise_folder(
    folder_path: str | Path,
    *,
    dry_run: bool = False,
    skip_existing: bool = True,
) -> None:
    """
    Organise files in folder_path into subfolders by type.
    - List all files in the target folder.
    - For each file, determine its extension and thus its category.
    - Create the category folder if it does not exist.
    - Move the file to that folder.
    """
    root = Path(folder_path).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    # ---------------------------------------------------------------------------
    # 2. List all files in the target folder (ignore subfolders)
    # ---------------------------------------------------------------------------
    all_files = [f for f in root.iterdir() if f.is_file()]
    if not all_files:
        print(f"No files to organise in: {root}")
        return

    if dry_run:
        print("[DRY RUN] No changes will be made.\n")

    # ---------------------------------------------------------------------------
    # 3. For each file: determine its extension and thus its category
    # 4. Create the category folder if it does not exist
    # 5. Move the file to that folder
    # ---------------------------------------------------------------------------
    for filepath in all_files:
        category = get_category_for_file(filepath)
        target_dir = root / category
        dest = target_dir / filepath.name

        if dry_run:
            print(f"  {filepath.name}  →  {category}/")
            continue

        # Create the folder if it doesn't exist (mkdir(exist_ok=True) doesn't fail if it already exists)
        target_dir.mkdir(exist_ok=True)

        if dest.exists() and skip_existing:
            print(f"Skip (exists): {filepath.name} → {category}/")
            continue

        # Path.rename() does not overwrite on most OSes; remove destination when overwriting
        if dest.exists():
            dest.unlink()

        try:
            filepath.rename(dest)  # moves the file to the new path (like mv/rename)
            print(f"Move: {filepath.name} → {category}/")
        except OSError as e:
            print(f"Error moving {filepath.name}: {e}")

    if not dry_run:
        print(f"\nDone. Files organised under: {root}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organise files in a folder into subfolders by type (Images, Videos, Documents, etc.)."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=os.path.expanduser("~/Downloads"),
        help="Folder to organise (default: ~/Downloads)",
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Only show what would be done; do not create folders or move files",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing file in target if same name (default: skip)",
    )
    args = parser.parse_args()

    organise_folder(
        args.folder,
        dry_run=args.dry_run,
        skip_existing=not args.overwrite,
    )


if __name__ == "__main__":
    main()
