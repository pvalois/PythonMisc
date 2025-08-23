#!/usr/bin/env python3

import os
import re
import json
import subprocess
import argparse
import pykakasi

# Initialize pykakasi for romaji conversion
kakasi = pykakasi.kakasi()

# Regex to match Japanese letters (hiragana, katakana, kanji)
JP_LETTERS = re.compile(r'([぀-ゟ゠-ヿ一-鿿]+)')
VIDEO_AUDIO_EXT = ('.mp4', '.webm', '.mkv', '.avi', '.m4a', '.mp3')
DEFAULT_PLAN = 'rename_plan.json'


def kakasi_cli(block: str) -> str:
    """Fallback via kakasi CLI if pykakasi fails."""
    try:
        out = subprocess.run(
            ['kakasi','-Ja','-Ha','-Ka','-Ea','-s'],
            input=block, capture_output=True, text=True, check=True
        ).stdout.strip()
        return out or block
    except Exception:
        return block


def convert_block(block: str) -> str:
    """
    Convert a block: if entirely Japanese letters, convert to romaji;
    otherwise return unchanged (preserve punctuation/symbols).
    """
    if JP_LETTERS.fullmatch(block):
        try:
            conv = kakasi.convert(block)
            romaji = ''.join(item.get('roman','') for item in conv).strip()
            if romaji:
                return romaji
        except Exception:
            pass
        return kakasi_cli(block)
    return block


def filename_to_romaji(name: str) -> str:
    """
    Split name into Japanese vs non-Japanese blocks, convert each,
    reassemble and clean spaces.
    """
    parts = JP_LETTERS.split(name)
    converted = [convert_block(p) for p in parts]
    return re.sub(r'\s+', ' ', ''.join(converted)).strip()


def build_plan(directory: str, plan_file: str):
    """
    Scan directory and build a plan (list of {old, new}).
    Write it as JSON to plan_file.
    """
    plan = []
    for fn in os.listdir(directory):
        if not fn.lower().endswith(VIDEO_AUDIO_EXT):
            continue
        base, ext = os.path.splitext(fn)
        newbase = filename_to_romaji(base)
        newname = f"{newbase}{ext}"
        if newname != fn:
            plan.append({'old': fn, 'new': newname})
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    print(f"Plan saved to {plan_file} ({len(plan)} entries)")


def apply_plan(plan_file: str):
    """
    Apply rename operations from JSON plan.
    """
    if not os.path.exists(plan_file):
        print(f"Plan file {plan_file} not found.")
        return
    with open(plan_file, 'r', encoding='utf-8') as f:
        plan = json.load(f)
    for entry in plan:
        old, new = entry['old'], entry['new']
        if os.path.exists(old):
            os.rename(old, new)
            print(f"Renamed: {old} -> {new}")
        else:
            print(f"Missing source: {old}")
    print("Apply complete.")


def rollback_plan(plan_file: str):
    """
    Roll back rename operations from JSON plan (swap new->old).
    """
    if not os.path.exists(plan_file):
        print(f"Plan file {plan_file} not found.")
        return
    with open(plan_file, 'r', encoding='utf-8') as f:
        plan = json.load(f)
    for entry in reversed(plan):
        old, new = entry['old'], entry['new']
        if os.path.exists(new):
            os.rename(new, old)
            print(f"Rolled back: {new} -> {old}")
        else:
            print(f"Missing target for rollback: {new}")
    print("Rollback complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Romaji rename utility with plan/apply/rollback commands"
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # plan subcommand
    p_plan = subparsers.add_parser('plan', help='Generate rename plan JSON')
    p_plan.add_argument('--plan-file', default=DEFAULT_PLAN, help='Path to plan JSON file')
    p_plan.add_argument('--dir', default='.', help='Directory to scan')

    # apply subcommand
    p_apply = subparsers.add_parser('apply', help='Apply rename plan')
    p_apply.add_argument('--plan-file', default=DEFAULT_PLAN, help='Path to plan JSON file')

    # rollback subcommand
    p_rollback = subparsers.add_parser('rollback', help='Rollback rename plan')
    p_rollback.add_argument('--plan-file', default=DEFAULT_PLAN, help='Path to plan JSON file')

    args = parser.parse_args()
    if args.command == 'plan':
        build_plan(args.dir, args.plan_file)
    elif args.command == 'apply':
        apply_plan(args.plan_file)
    elif args.command == 'rollback':
        rollback_plan(args.plan_file)

if __name__ == '__main__':
    main()

