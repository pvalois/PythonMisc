#!/usr/bin/env python3

from PyPDF2 import PdfReader, PdfWriter
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Page extractor")
    parser.add_argument('-i', '--input', type=str, required=True, help='Toggle OFF')
    parser.add_argument('-p', '--pages', action='append', type=str, required=True, help='Ajouter une page ou serie de pages')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, help='Ne fais rien')
    args = parser.parse_args()

    filename = args.input
    serie = ",".join(args.pages)
    pages = sorted(set([i 
                        for part in serie.split(',') 
                        for i in (range(int(part.split('-')[0]), int(part.split('-')[1]) + 1) 
                        if '-' in part 
                        else [int(part)])]))

    if (not args.dry_run):
      pdf_reader = PdfReader(open(filename, 'rb'))
      pdf_writer = PdfWriter()

    for p in pages:
      print ("page",int(p))
      if (not args.dry_run):
        page = pdf_reader.pages[int(p)-1]
        pdf_writer.add_page(page)

    if  (not args.dry_run):
      with open("selected_pages.pdf",'wb') as out:
        pdf_writer.write(out)

