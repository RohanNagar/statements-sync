# Statements Sync

A python script used to rename and organize downloaded financial statements. All PDF files
in the Downloads folder are parsed, renamed to the closing date of the statement in `YYYY-MM-DD`
format, and moved into an organized structure within Google Drive.

## Usage

1. Install required dependencies

```bash
$ pip3 install -r requirements.txt
```

2. Run the script

```
usage: sync.py [-h] [-s SEARCH_DIR] [-d]

Rename and organize financial account statements.

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH_DIR, --search_dir SEARCH_DIR
                        The directory to search for financial statements
  -d, --dry_run         Perform a dry run (do not actually rename or move files)
```