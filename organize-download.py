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
    "Documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
    "Documents/PDF": ["pdf"],
    "Documents/Word": ["doc", "docx"],
    "Documents/Excel": ["xls", "xlsx"],
    "Documents/PowerPoint": ["ppt", "pptx"],
    "Documents/NOTE": ["txt"],
    "Archives": ["zip", "rar", "tar.gz", "tar.bz2", "7z", "gz", "bz2"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv"],
    "Music": ["mp3", "wav", "flac"],
    "Others": []
}

# Function to organize files
def organise_files():
    # Check if the Downloads directory exists
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"Error: {DOWNLOADS_DIR} does not exist.")
        return

    # Iterate over all files in the directory
    for file_name in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, file_name)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Find the category for the file
        file_extension = file_name.split(".")[-1].lower()
        destination_folder = None
        for folder, extensions in FOLDER_MAP.items():
            if file_extension in extensions:
                destination_folder = folder
                break
        else:
            destination_folder = "Others"

        # Create the destination folder if it doesn't exist
        dest_path = os.path.join(DOWNLOADS_DIR, destination_folder)
        os.makedirs(dest_path, exist_ok=True)

        # Move the file
        shutil.move(file_path, dest_path)
        print(f"Moved: {file_name} -> {destination_folder}")

# Run the script
if __name__ == "__main__":
    organise_files()
    print("Organizing completed!")
