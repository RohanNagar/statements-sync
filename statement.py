import pypdf

from pdfminer import high_level
from statementType import StatementType

class Statement:
  def __init__(self, fileName, filePath):
    self.fileName = fileName
    self.filePath = filePath
    self.text = self.__read_pdf_text()
    self.type = self.__determine_type()

  def __read_pdf_text(self):
    pdfFile = open(self.filePath, 'rb')
    pdfReader = pypdf.PdfReader(pdfFile)

    if pdfReader.is_encrypted:
      pdfReader.decrypt('')

    text = pdfReader.pages[0].extract_text()

    # Fallback for special cases
    if text.isspace() or ('eStmt' in self.filePath) or ('Discover' in self.filePath):
      text = high_level.extract_text(self.filePath, "", [0])

    # For certain accounts (Charles Schwab/Vanguard) we need more pages of the PDF
    if 'Box Inc.' in text or 'Schwab One' in text or 'Vanguard Brokerage Services' in text:
      text = text + pdfReader.pages[1].extract_text() + pdfReader.pages[2].extract_text()

    pdfFile.close()
    return text

  def __determine_type(self):
    if 'BarclaysView' in self.text:
      return StatementType.BARCLAYS_VIEW
    elif 'statements-1595' in self.filePath:
      return StatementType.CSR
    elif 'statements-5226' in self.filePath:
      return StatementType.PRIME_VISA
    elif 'statements-2729' in self.filePath:
      return StatementType.FREEDOM_FLEX
    elif 'statements-9176' in self.filePath:
      return StatementType.FREEDOM_UNLIMIED
    elif 'BlueCashEveryday' in self.text:
      return StatementType.AMEX_BCE
    elif 'U.S. Bank Altitude® Go' in self.text:
      return StatementType.ALTITUDE_GO
    elif 'Discover-Statement' in self.filePath:
      return StatementType.DISCOVER_IT
    elif 'Ally Bank' in self.text:
      return StatementType.ALLY
    elif 'HealthEquity' in self.text:
      return StatementType.HEALTH_EQUITY_HSA
    elif 'Adv Plus Banking' in self.text:
      return StatementType.BOFA_CHECKING
    elif 'Account# 4400' in self.text:
      return StatementType.BOFA_CUSTOMIZED_CASH
    elif 'Box Inc.' in self.text and 'Quarterly Activity' in self.text:
      return StatementType.SCHWAB_QUARTERLY
    elif 'Box Inc. Employee Stock Purchase Plan' in self.text:
      return StatementType.SCHWAB_ESPP
    elif 'Box Inc.' in self.text and 'Restricted Stock Activity' in self.text:
      return StatementType.SCHWAB_RSU
    elif 'Schwab One® Account' in self.text:
      return StatementType.SCHWAB_INDIVIDUAL
    elif 'Fidelity Brokerage Services' in self.text and 'INDIVIDUAL TOD' in self.text:
      return StatementType.FIDELITY_INDIVIDUAL
    elif 'Fidelity Brokerage Services' in self.text and 'HEALTH SAVINGS' in self.text:
      return StatementType.FIDELITY_HSA
    elif 'Vanguard Brokerage Services' in self.text and 'Roth IRA' in self.text:
      return StatementType.VANGUARD_ROTH
    elif 'Vanguard Brokerage Services' in self.text and 'Traditional IRA' in self.text:
      return StatementType.VANGUARD_TRAD
    else:
      print(f' {self.text}')
      raise Exception('Unknown Statement Type')

