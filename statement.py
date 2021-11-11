import PyPDF2

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
    pdfReader = PyPDF2.PdfFileReader(pdfFile)

    if pdfReader.isEncrypted:
      pdfReader.decrypt('')

    text = pdfReader.getPage(0).extractText()

    # Fallback for special cases
    if text.isspace() or ('eStmt' in self.filePath) or ('Discover' in self.filePath):
      print('  Using Fallback PDF text extractor')
      text = high_level.extract_text(self.filePath, "", [0])

    # debug
    #if 'eStmt' in self.filePath:
    #  print(text)

    pdfFile.close()
    return text

  def __determine_type(self):
    if 'BarclaysView' in self.text:
      return StatementType.BARCLAYS_VIEW
    elif 'statements-1595' in self.filePath:
      return StatementType.CSR
    elif 'statements-5226' in self.filePath:
      return StatementType.PRIME_VISA
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
    elif 'Account# 4400 6662 4070 2916' in self.text:
      return StatementType.BOFA_CUSTOMIZED_CASH
    else:
      print(' ' + self.text)
      raise Exception('Unknown Statement Type')

