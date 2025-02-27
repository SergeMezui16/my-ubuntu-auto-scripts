import os
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Downloads directory from the .env file
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR")

if not DOWNLOADS_DIR:
    print("Error: DOWNLOADS_DIR not set in .env file.")
    exit(1)

# Categorization by extensions
FOLDER_MAP = {
    "Images": ["jpg", "jpeg", "png", "gif", "svg", "bmp"],
    "Documents/PDF": ["pdf"],
    "Documents/Data": ["csv", "tsv", "json", "xml", "sql"],
    "Documents/Word": ["doc", "docx"],
    "Documents/Excel": ["xls", "xlsx"],
    "Documents/PowerPoint": ["ppt", "pptx"],
    "Documents/Note": ["txt", "md", "rst", "mdx"],
    "Archives": ["zip", "rar", "tar.gz", "tar.bz2", "7z", "gz", "bz2", "aab", "tar", "tgz"],
    "Archives/Apk": ["apk", "xapk"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv"],
    "Music": ["mp3", "wav", "flac"],
    "Others": []
}

DEFAULT_DESTINATION_FOLDER = "Others"

def get_unique_filename(dest_path, file_name):
    # Split filename into name and extension
    name, ext = os.path.splitext(file_name)
    counter = 0
    new_path = os.path.join(dest_path, file_name)

    # Keep checking until we find a filename that doesn't exist
    while os.path.exists(new_path):
        counter += 1
        new_file_name = f"{name}{counter}{ext}"
        new_path = os.path.join(dest_path, new_file_name)

    return new_path

def get_file_extension(filename):
    # Handle multipart extensions and no extensions
    parts = filename.lower().split('.')
    if len(parts) > 2 and parts[-2:] == ['tar', 'gz']:
        return 'tar.gz'
    return parts[-1] if len(parts) > 1 else ''

# Function to organize files
def organise_files():
    if not os.path.exists(DOWNLOADS_DIR) or not os.path.isdir(DOWNLOADS_DIR):
        print(f"Error: {DOWNLOADS_DIR} is not a valid directory.")
        return

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
            print(f"Moved: {file_name} -> {destination_folder}/{moved_file_name}")

        except PermissionError:
            print(f"Permission denied: Cannot move {file_name}")
        except OSError as e:
            print(f"Error moving {file_name}: {str(e)}")

# Run the script
if __name__ == "__main__":
    organise_files()
    print("Organizing completed!")
