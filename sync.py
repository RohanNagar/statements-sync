import argparse
import os
import sys

from statement import Statement
from statementType import StatementType
from pathlib import Path

def moveFile(stmt, parsedDate):
  newFilePath = stmt.type.build_new_file_path(parsedDate)

  print('  Moving statement at path ' + stmt.filePath + ' to path ' + newFilePath)
  os.rename(stmt.filePath, newFilePath)

def handleStatement(stmt, dryrun=False):
  date = stmt.type.parse_date(stmt)

  if not dryrun:
    moveFile(stmt, date)
  else:
    print('  DRY RUN MODE, FILE MOVE SKIPPED.')

def main(search_dir, dryrun=False):
  print('Starting sync of statements from folder ' + search_dir + '...\n')
  filesMovedCount = 0

  with os.scandir(search_dir) as files:
    for f in files:
        if f.is_file() and f.name.endswith('.pdf'):
          print('Processing PDF file ' + f.name)

          try:
            stmt = Statement(f.name, f.path)
            handleStatement(stmt, dryrun)
            filesMovedCount += 1
          except Exception as exp:
            print('  ' + str(exp))
            print('  An exception occured while parsing this file, skipping...')
            continue

  print('\nFinished sync of statements. Files moved and renamed: ' + str(filesMovedCount))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Rename and organize financial account statements.')
  parser.add_argument('-s', '--search_dir', required=False, default=str(Path.home() / "Downloads"),
                      help='The directory to search for financial statements')
  parser.add_argument('-d', '--dry_run', required=False, action='store_true',
                      help='Perform a dry run (do not actually rename or move files)')

  args = parser.parse_args()
  main(args.search_dir, args.dry_run)
