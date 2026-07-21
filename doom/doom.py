#!/usr/bin/env python3
"""
Doom — simple roasting CLI (offline mode only)

Usage:
  python doom/doom.py "target"
  python doom/doom.py "target" --count 3

This script keeps roasts playful and refuses targets that mention protected
categories or look like personal identifiers (emails, handles, long digit strings).
"""
import argparse
import random
import re
import sys

ROAST_TEMPLATES = [
    "{t}, you'd lose a staring contest with a goldfish.",
    "{t}, if brains were taxed you'd get a refund.",
    "{t}, calling you understates how much effort went into mediocrity.",
    "{t}, you have the charisma of a dial tone.",
    "{t}, I'd explain it to you but I left my crayons at home.",
]

PROTECTED_KEYWORDS = [
    "race", "ethnicity", "religion", "gender", "sexual orientation",
    "trans", "disabled", "disability", "age", "nationality",
]

PERSONAL_ID_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",     # SSN-like
    r"\b\d{10,}\b",              # long digit strings
    r"@[\w\-]+",                 # handles
    r"\b[\w\.-]+@[\w\.-]+\.\w+\b", # emails
]
PERSONAL_REGEXES = [re.compile(p, re.I) for p in PERSONAL_ID_PATTERNS]


def contains_protected(text: str) -> bool:
    t = text.lower()
    for k in PROTECTED_KEYWORDS:
        if k in t:
            return True
    return False


def contains_personal_id(text: str) -> bool:
    for r in PERSONAL_REGEXES:
        if r.search(text):
            return True
    return False


def safe_to_roast(target: str):
    problems = []
    if contains_protected(target):
        problems.append("mentions protected categories")
    if contains_personal_id(target):
        problems.append("contains personal identifiers")
    return (len(problems) == 0, problems)


def generate_roasts(target: str, count: int = 1):
    out = []
    for _ in range(max(1, count)):
        tmpl = random.choice(ROAST_TEMPLATES)
        out.append(tmpl.format(t=target))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Doom — simple roasting CLI")
    parser.add_argument("target", help="Who or what to roast (short phrase)")
    parser.add_argument("--count", type=int, default=1, help="Number of roasts")
    args = parser.parse_args(argv)

    target = args.target.strip()
    ok, problems = safe_to_roast(target)
    if not ok:
        print("I won't roast that. Reason:", ", ".join(problems))
        sys.exit(1)

    for line in generate_roasts(target, args.count):
        print(line)


if __name__ == '__main__':
    main()
