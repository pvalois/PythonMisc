#!/usr/bin/env python3

import sys
import argparse
import email, smtplib, ssl
from email.message import EmailMessage

parser = argparse.ArgumentParser(description="Gestion des toggles")
parser.add_argument('-S', '--server', default="localhost", help='Adresse du serveur SMTP')
parser.add_argument('-f', '--sender', default="user@localhost", help='Expéditeur du mail')
parser.add_argument('-t', '--receiver', default="admin@local.host", help='Destinataire du mail')
parser.add_argument('-s', '--subject', default="Test de mail", help='Sujet du mail')
parser.add_argument('-i', '--input', default=None, help='Fichier texte a envoyer')
parser.add_argument('-N', '--dry-run', default=False, action='store_true', help='dry-run')

args = parser.parse_args()

def send_mail(servername, sender, receiver, subject, body):
    message=EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    print (f"Sending mail to {servername}")
    print (f"  ++ from    : {sender}")
    print (f"  ++ to      : {receiver}")
    print (f"  ++ subject : {subject}")
    print (f"  ++ via     : {servername}")
    print ("")

    print ("#"*30)
    print (body)
    print ("#"*30)

    if (not args.dry_run):
      print ("")
      print ("Sending mail ....")
      server=smtplib.SMTP(servername)
      server.send_message(message)
      server.quit()
      print ("Mail sent !!!")

if args.input:
  try:
    with open(args.input, "r") as f:
      body = f.read().rstrip()
  except FileNotFoundError:
    sys.exit(f"Erreur : fichier '{args.input}' introuvable.")
else:
  body = sys.stdin.read().rstrip()

send_mail(args.server, args.sender, args.receiver, args.subject, body)

