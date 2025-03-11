import os
import shutil
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Get the Downloads directory from the .env file
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR")

if not DOWNLOADS_DIR:
    print(f"{Fore.RED}Error: DOWNLOADS_DIR not set in .env file.{Style.RESET_ALL}")
    exit(1)

# Categorization by extensions (same as before)
FOLDER_MAP = {
    "Images": ["jpg", "jpeg", "png", "gif", "svg", "bmp", "webp"],
    "Documents/PDF": ["pdf"],
    "Documents/Data": ["csv", "tsv", "json", "xml", "sql"],
    "Documents/Word": ["doc", "docx"],
    "Documents/Excel": ["xls", "xlsx"],
    "Documents/PowerPoint": ["ppt", "pptx"],
    "Documents/Note": ["txt", "md", "rst", "mdx", "pub"],
    "Archives": ["zip", "rar", "tar.gz", "tar.bz2", "7z", "gz", "bz2", "aab", "tar", "tgz"],
    "Archives/Apk": ["apk", "xapk"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv"],
    "Music": ["mp3", "wav", "flac"],
    "Others": []
}

DEFAULT_DESTINATION_FOLDER = "Others"


def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": Fore.BLUE,
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW
    }
    color = colors.get(status, Fore.WHITE)
    print(f"{color}{message}{Style.RESET_ALL}")


def get_unique_filename(dest_path, file_name):
    name, ext = os.path.splitext(file_name)
    counter = 0
    new_path = os.path.join(dest_path, file_name)

    while os.path.exists(new_path):
        counter += 1
        new_file_name = f"{name}{counter}{ext}"
        new_path = os.path.join(dest_path, new_file_name)

    return new_path


def get_file_extension(filename):
    parts = filename.lower().split('.')
    if len(parts) > 2 and parts[-2:] == ['tar', 'gz']:
        return 'tar.gz'
    return parts[-1] if len(parts) > 1 else ''


def organise_files():
    if not os.path.exists(DOWNLOADS_DIR) or not os.path.isdir(DOWNLOADS_DIR):
        print_status(f"Error: {DOWNLOADS_DIR} is not a valid directory.", "error")
        return

    print_status(f"Starting organization of {DOWNLOADS_DIR}", "info")
    files_moved = 0
    errors = 0

    for file_name in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, file_name)

        if not os.path.isfile(file_path):
            continue

        try:
            extension = get_file_extension(file_name)
            destination_folder = DEFAULT_DESTINATION_FOLDER

            for folder, extensions in FOLDER_MAP.items():
                if extension in extensions:
                    destination_folder = folder
                    break

            dest_path = os.path.join(DOWNLOADS_DIR, destination_folder)
            os.makedirs(dest_path, exist_ok=True)

            dest_file_path = get_unique_filename(dest_path, file_name)
            shutil.move(file_path, dest_file_path)

            moved_file_name = os.path.basename(dest_file_path)
            print_status(
                f"✓ Moved: {file_name} → {destination_folder}/{moved_file_name}",
                "success"
            )
            files_moved += 1

        except PermissionError:
            print_status(f"✗ Permission denied: Cannot move {file_name}", "error")
            errors += 1
        except OSError as e:
            print_status(f"✗ Error moving {file_name}: {str(e)}", "error")
            errors += 1

    # Print summary
    print("\n" + "=" * 50)
    print_status(f"Organization completed!", "info")
    print_status(f"Files moved successfully: {files_moved}", "success")
    if errors > 0:
        print_status(f"Errors encountered: {errors}", "error")


if __name__ == "__main__":
    print_status("\n📂 File Organization Script", "info")
    print_status("=" * 50, "info")
    organise_files()
