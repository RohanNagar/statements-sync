from datetime import datetime
from enum import Enum

'''
Formats a given datetime object into a string of the form YYYY-MM-DD.
'''
def format_date(parsedDate):
  yearStr = parsedDate.year
  monthStr = str(parsedDate.month) if parsedDate.month >= 10 else '0' + str(parsedDate.month)
  dayStr = str(parsedDate.day) if parsedDate.day >= 10 else '0' + str(parsedDate.day)

  return '{0}-{1}-{2}'.format(parsedDate.year, monthStr, dayStr)

'''
Parses a date contained within the given pdfText based on the
indicatorText and the offset parameters. The date is returned in the form
YYYY-MM-DD.
'''
def parse(pdfText, indicatorText, startOffset, endOffset, dateFormat):
  periodIndex = pdfText.find(indicatorText)
  date = pdfText[periodIndex+startOffset:periodIndex+endOffset]
  parsedDate = datetime.strptime(date, dateFormat)
  return format_date(parsedDate)

def parse_barclays_date(statement):
  return parse(statement.text, 'StatementPeriod', 25, 33, "%m/%d/%y")

def parse_chase_date(statement):
  return parse(statement.text, 'Closing Date', 23, 31, "%m/%d/%y")

def parse_amex_date(statement):
  return parse(statement.text, 'ClosingDate', 11, 19, "%m/%d/%y")

def parse_usbank_date(statement):
  return parse(statement.text, 'Closing Date', 13, 23, "%m/%d/%Y")

def parse_ally_date(statement):
  return parse(statement.text, 'Statement Date', 14, 24, "%m/%d/%Y")

def parse_health_equity_date(statement):
  return parse(statement.text, 'Period:', 25, 33, "%m/%d/%y")

def parse_bofa_date(statement):
  return statement.fileName.removeprefix('eStmt_').removesuffix('.pdf')

def parse_discover_date(statement):
  return parse(statement.text, 'Account Summary', 30, 40, "%m/%d/%Y")

class StatementType(Enum):
  def __init__(self, accountType, accountName, parseDateMethod):
    self.accountType = accountType
    self.accountName = accountName
    self.parseDateMethod = parseDateMethod

  def parse_date(self, statement):
    print('  Parsing Date for ' + self.accountName + ' statement...')
    return self.parseDateMethod(statement)

  def build_new_file_path(self, date):
    year = datetime.strptime(date, "%Y-%m-%d").year
    return '/Users/rohannagar/Google Drive/My Drive/Finance/' + str(year) + '/' + self.accountType + '/' + self.accountName + '/' + date + ".pdf"

  # Credit Cards
  BARCLAYS_VIEW = 'Credit', 'Uber Barclaycard', parse_barclays_date
  CSR = 'Credit', 'CSR', parse_chase_date
  FREEDOM_UNLIMIED = 'Credit', 'Freedom Unlimited', parse_chase_date
  PRIME_VISA = 'Credit', 'Prime Visa', parse_chase_date
  AMEX_BCE = 'Credit', 'American Express', parse_amex_date
  ALTITUDE_GO = 'Credit', 'US Bank', parse_usbank_date
  BOFA_CUSTOMIZED_CASH = 'Credit', 'Bank of America', parse_bofa_date
  DISCOVER_IT = 'Credit', 'Discover', parse_discover_date

  # Bank Accounts
  ALLY = 'Banking', 'Ally', parse_ally_date
  BOFA_CHECKING = 'Banking', 'Bank of America', parse_bofa_date

  # Investment Accounts
  HEALTH_EQUITY_HSA = 'Investments', 'HealthEquity', parse_health_equity_date
