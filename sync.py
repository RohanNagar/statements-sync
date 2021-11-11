import argparse
import os

from statement import Statement
from statementType import StatementType
from pathlib import Path

def move_file(stmt, parsedDate):
  newFilePath = stmt.type.build_new_file_path(parsedDate)

  print('  Moving statement at path ' + stmt.filePath + ' to path ' + newFilePath)
  os.rename(stmt.filePath, newFilePath)

def handle_statement(stmt, dryrun=False):
  date = stmt.type.parse_date(stmt)

  if not dryrun:
    move_file(stmt, date)
  else:
    print('  DRY RUN. Statement ' + stmt.fileName + ' would have been moved to ' + stmt.type.build_new_file_path(date))

def main(search_dir, dryrun=False):
  print('Starting sync of statements from folder ' + search_dir + '...')
  filesMovedCount = 0

  with os.scandir(search_dir) as files:
    for f in files:
        if f.is_file() and f.name.endswith('.pdf'):
          print('\nProcessing PDF file ' + f.name)

          try:
            stmt = Statement(f.name, f.path)
            handle_statement(stmt, dryrun)
            filesMovedCount += 1
          except Exception as exp:
            print('  ' + str(exp))
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
