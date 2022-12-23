class Configs:
    def __init__(self):
        self.home_directory = 'C:\\Users\\SLL125\\ZohoToCSV'
        self.pytesseract_directory = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    @property
    def get_home_directory(self):
        return self.home_directory

    @property
    def get_pytesseract_directory(self):
        return self.pytesseract_directory


