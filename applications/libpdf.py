#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from pdfminer.pdfparser import PDFParser, PDFDocument
import os
import re
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def pdf_resolver(file_name):
    parser = PDFParser(open(file_name, 'rb'))
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)

    doc.initialize()
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for x in layout:
            if isinstance(x, LTTextBox):
                print(x.get_text().strip())

file_path = '/home/friederich/Downloads/'

file_list = os.listdir(file_path)
for file_name in file_list:
    if re.search(r'\.pdf$', file_name, re.I):
        print(file_name)
        pdf_resolver(file_path + file_name)
