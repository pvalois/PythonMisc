#!/usr/bin/env python3 

import re
import shutil
import filecmp
import os
import argparse
from pathlib import Path
from datetime import datetime

TMP_BASE = Path('/tmp/normalise_yaml')

def get_bak_path_simple(original_path: Path):
    TMP_BASE.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    nouveau_nom = f"{timestamp}-{original_path.name}"
    return TMP_BASE / nouveau_nom

def corriger_yaml_ansible_inplace(fichier_path):
    fichier = str(fichier_path)
    with open(fichier, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    modifications = {
        "maj_name": 0,
        "fqdn": 0,
        "trim_end_line": 0,
        "trim_end_file": 0,
        "yes_to_true": 0,
        "octal_mode": 0,
        "package": 0
    }

    lignes_corrigees = []
    for ligne in lignes:
        ligne_originale = ligne
        ligne = ligne.rstrip()

        if ligne != ligne_originale.rstrip('\n'):
            modifications["trim_end_line"] += 1

        match = re.match(r'(\s*- name\s*:\s*)(.+)', ligne)
        if match:
            prefix, valeur = match.groups()
            if valeur and not valeur[0].isupper():
                valeur = valeur[:1].upper() + valeur[1:]
                modifications["maj_name"] += 1
            ligne = prefix + valeur

        match = re.match(r'(.*:\s)\s*(yes|True)\s*', ligne)
        if match:
            prefix, valeur = match.groups()
            valeur = "true"
            modifications["yes_to_true"] += 1
            ligne = prefix + valeur

        match = re.match(r'(.*:\s)\s*(no|False)\s*', ligne)
        if match:
            prefix, valeur = match.groups()
            valeur = "false"
            modifications["yes_to_true"] += 1
            ligne = prefix + valeur

        match = re.match(r'(^\s*mode):\s*([0-9]+)', ligne)
        if match:
            prefix, valeur = match.groups()
            modifications["octal_mode"] += 1
            ligne = f'{prefix}: "{valeur}"'

        match = re.match(r'^  (.*):(.*)', ligne)
        candidates = [ "command", "shell", "get_url", "lineinfile", "copy", "service", 
                       "dnf", "apt", "yum", "template", "command", "shell", "set_fact"]
        if match:
            prefix, valeur = match.groups()
            if (prefix in candidates):
                prefix=f'ansible.builtin.{prefix}'
                modifications["fqdn"] += 1
                ligne = f"  {prefix}:{valeur}"

        if (any (w in ligne for w in ["ansible.builtin.apt:","ansible.builtin.dnf:","ansible.builtin.yum:"])):
            ligne=ligne.replace("ansible.builtin.apt","ansible.builtin.package")
            ligne=ligne.replace("ansible.builtin.dnf","ansible.builtin.package")
            ligne=ligne.replace("ansible.builtin.yum","ansible.builtin.package")
            modifications["package"]+=1
         
        lignes_corrigees.append(ligne)

    n_lignes_vide = 0
    for ligne in reversed(lignes_corrigees):
        if ligne.strip() == '':
            n_lignes_vide += 1
        else:
            break

    if n_lignes_vide > 0:
        modifications["trim_end_file"] = n_lignes_vide
        lignes_corrigees = lignes_corrigees[:-n_lignes_vide]

    lignes_corrigees.append('')

    contenu_corrige = '\n'.join(lignes_corrigees)

    temp_file = fichier + '.tmp'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(contenu_corrige)

    if not filecmp.cmp(fichier, temp_file, shallow=False):
        bak_path = get_bak_path_simple(fichier_path)
        shutil.copy2(fichier, bak_path)
        shutil.move(temp_file, fichier)

        print(f"[+] {fichier} corrigé, sauvegarde originale sous {bak_path}")
        print(f"    Modifications :")
        print(f"      - Majuscule sur 'name' : {modifications['maj_name']}")
        print(f"      - Espaces en fin de ligne supprimés : {modifications['trim_end_line']}")
        print(f"      - Lignes vides en fin de fichier supprimées : {modifications['trim_end_file']}")
        print(f"      - fqdn : {modifications['fqdn']}")
        print(f"      - yes to true : {modifications['yes_to_true']}")
        print(f"      - use of package instead of apt/yum/dnf : {modifications['package']}")
        print(f"      - octal_mode : {modifications['octal_mode']}")
    else:
        os.remove(temp_file)
        print(f"[=] {fichier} : Pas de modification nécessaire")

def main():
    parser = argparse.ArgumentParser(description="Corrige basiquement les fichiers YAML Ansible (mode inplace avec sauvegarde simple timestampée dans /tmp/normalise_yaml)")
    parser.add_argument('fichiers', nargs='+', type=Path, help="Fichiers YAML à corriger")
    args = parser.parse_args()

    for fichier_path in args.fichiers:
        if fichier_path.is_file():
            corriger_yaml_ansible_inplace(fichier_path)
        else:
            print(f"[!] Fichier non trouvé ou non valide : {fichier_path}")


if __name__ == "__main__":
    main()

