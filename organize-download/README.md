# [Organize Download](./organize-download.py) (21/01/2025)

This Python script automatically organizes files in the downloads directory based on their extension.

## Prerequisites

- Python 3.x
- `python3-dotenv` library

## Installation

1. Clone this repository or download the files.
2. Install the necessary dependencies using pip:
```sh
pip install python3-dotenv
```

## Configuration

Create a file named [.env](http://_vscodecontentref_/0) in the same directory as the script and add the path to your downloads directory:

```dotenv
DOWNLOADS_DIR="/your/path/to/Downloads"
```

## How to use it

Execute the script by using the command :
```sh
python3 organize-download/main.py 
```

If you want to create a cronjob, execute :
```bash
crontab -e
0 20 * * * python3 /path/to/file/organize-download/main.py # execute everyday at 8pm
```