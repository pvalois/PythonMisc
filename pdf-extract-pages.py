#!/usr/bin/env python3

from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Page extractor")
    parser.add_argument('-i', '--input', type=str, required=True, help='Toggle OFF')
    parser.add_argument('-p', '--pages', action='append', type=str, required=True, help='Ajouter une page ou serie de pages')
    args = parser.parse_args()

    filename = args.input
    serie = ",".join(args.pages)
    pages = set([i for part in serie.split(',') for i in (range(int(part.split('-')[0]), int(part.split('-')[1]) + 1) if '-' in part else [int(part)])])

    pdf_reader = PdfFileReader(open(filename, 'rb'))
    pdf_writer = PdfFileWriter()

    for p in pages:
      print ("page",int(p))
      page = pdf_reader.getPage(int(p)-1)
      pdf_writer.addPage(page)

    with open("selected_pages.pdf",'wb') as out:
      pdf_writer.write(out)

