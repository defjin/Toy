from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.layout import LAParams
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.layout import LTTextBoxHorizontal
from googletrans import Translator
import re
import sys

# writing file
file = open('bb.txt', 'w')

#open a PDF file
document = open('mypdf2.pdf', 'rb')

#Create a PDF resource manager object that stores shared resources
rsrcmgr = PDFResourceManager()
# set parameter for analysis
laparams = LAParams()
#Crate PDF page aggregator object
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

count = 0

for page in PDFPage.get_pages(document):
    translator = Translator()
    count += 1
    if count < 3:
        continue
    if count > 4:
        break

    interpreter.process_page(page)
    layout = device.get_result()
    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            text = element.get_text()
            print(text)
            textparsers = re.findall('[\s\S]+?[.]', text)
            print(textparsers)
            translation = translator.translate('the friends of mine', dest='ko')
            print(translation.text)
            for parse in textparsers:
                print(parse)
                if '\n' in parse:
                    replace = parse.replace('\n', '')
                    translation = translator.translate(replace, dest='ko', src='en')
                    file.write(translation.origin + '->' + translation.text)
                    file.write('\n')
                else:
                    translation = translator.translate(parse, dest='ko', src='en')
                    file.write(translation.origin + '->' + translation.text)
                    file.wirte('\n')

file.close()







