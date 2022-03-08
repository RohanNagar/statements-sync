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

def parse_schwab_espp_date(statement):
  return parse(statement.text, 'Purchase Date', 14, 22, "%m/%d/%y")

def parse_schwab_individual_date(statement):
  return parse(statement.text, 'Ending Value on', 16, 26, "%m/%d/%Y")

def parse_schwab_quarterly_date(statement):
  return parse(statement.text, 'StatementPeriod:', 26, 34, "%m/%d/%y")

def parse_schwab_rsu_date(statement):
  return parse(statement.text, 'Tax Treatment', 13, 21, "%m/%d/%y")

def parse_fidelity_date(statement):
  return parse(statement.fileName, 'Statement', 9, 17, "%m%d%Y")

def parse_vanguard_date(statement):
  return parse(statement.text[:statement.text.find(', quarter-to-date')], '800-662-2739', 12, 100, "%B %d, %Y")

class StatementType(Enum):
  def __init__(self, accountType, accountName, parseDateMethod, suffix=''):
    self.accountType = accountType
    self.accountName = accountName
    self.parseDateMethod = parseDateMethod
    self.suffix = '-' + suffix if suffix != '' else ''

  def parse_date(self, statement):
    print('  Parsing Date for ' + self.accountName + ' statement...')
    return self.parseDateMethod(statement)

  def build_new_file_path(self, date):
    year = datetime.strptime(date, "%Y-%m-%d").year
    return '/Users/rohannagar/Google Drive/My Drive/Finance/' + str(year) + '/' + self.accountType + '/' + self.accountName + '/' + date + self.suffix + ".pdf"

  # Credit Cards
  ALTITUDE_GO = 'Credit', 'US Bank', parse_usbank_date
  AMEX_BCE = 'Credit', 'American Express', parse_amex_date
  BARCLAYS_VIEW = 'Credit', 'Uber Barclaycard', parse_barclays_date
  BOFA_CUSTOMIZED_CASH = 'Credit', 'Bank of America', parse_bofa_date
  CSR = 'Credit', 'CSR', parse_chase_date
  DISCOVER_IT = 'Credit', 'Discover', parse_discover_date
  FREEDOM_FLEX = 'Credit', 'Freedom Flex', parse_chase_date
  FREEDOM_UNLIMIED = 'Credit', 'Freedom Unlimited', parse_chase_date
  PRIME_VISA = 'Credit', 'Prime Visa', parse_chase_date

  # Bank Accounts
  ALLY = 'Banking', 'Ally', parse_ally_date
  BOFA_CHECKING = 'Banking', 'Bank of America', parse_bofa_date

  # Investment Accounts
  FIDELITY_HSA = 'Investments', 'Fidelity', parse_fidelity_date, 'HSA'
  FIDELITY_INDIVIDUAL = 'Investments', 'Fidelity', parse_fidelity_date
  HEALTH_EQUITY_HSA = 'Investments', 'HealthEquity', parse_health_equity_date
  SCHWAB_ESPP = 'Investments', 'CharlesSchwab', parse_schwab_espp_date, 'ESPP-Purchase'
  SCHWAB_INDIVIDUAL = 'Investments', 'CharlesSchwab', parse_schwab_individual_date
  SCHWAB_QUARTERLY = 'Investments', 'CharlesSchwab', parse_schwab_quarterly_date, 'Quarterly'
  SCHWAB_RSU = 'Investments', 'CharlesSchwab', parse_schwab_rsu_date, 'RSULapse'
  VANGUARD_ROTH = 'Investments', 'Vanguard', parse_vanguard_date, 'Roth'
