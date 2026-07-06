#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║              HYPERCRACK v2 — Ultimate Password Mutation Engine      ║
║                                                                      ║
║  Merges: CUPP + Hashcat Rules + Markov Chains + Keyboard Walks      ║
║          + OSINT Profiling + Mask Attacks + Pattern Recognition     ║
║          + Date Math + Phonetic Generation + Combinator Attacks     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import argparse
import hashlib
import itertools
import json
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, date
from typing import Dict, List, Set, Tuple, Optional, Generator
from pathlib import Path

# ============================================================
# SECTION 1: KEYBOARD LAYOUT MATRICES (QWERTY, AZERTY, DVORAK)
# ============================================================

QWERTY_ROWS = [
    list("`1234567890-="),
    list("qwertyuiop[]\\"),
    list("asdfghjkl;'"),
    list("zxcvbnm,./"),
]

QWERTY_SHIFTED = [
    list("~!@#$%^&*()_+"),
    list("QWERTYUIOP{}|"),
    list('ASDFGHJKL:"'),
    list("ZXCVBNM<>?"),
]

AZERTY_ROWS = [
    list("²&é\"'(-è_çà)= "),
    list("azertyuiop^$"),
    list("qsdfghjklmù*"),
    list("wxcvbn,;:!"),
]

DVORAK_ROWS = [
    list("`1234567890[]"),
    list("',.pyfgcrl/="),
    list("aoeuidhtns-\\"),
    list(";qjkxbmwvz"),
]

KEYPAD = [
    list("789"),
    list("456"),
    list("123"),
    list(" 0 "),
]


# ============================================================
# SECTION 2: LEET SPEAK MAPPING (EXTENDED)
# ============================================================

LEET_MAP = {
    'a': ['a', 'A', '@', '4', 'а', 'α', 'Λ', 'λ', '/\\', '/-\\'],
    'b': ['b', 'B', '8', '6', '|3', 'l3', 'ß', 'в', 'Ь'],
    'c': ['c', 'C', '<', '(', '{', '©', '¢', 'с', '⊂'],
    'd': ['d', 'D', '|)', 'Đ', 'đ', 'ď', 'ⅾ'],
    'e': ['e', 'E', '3', '€', 'ë', '£', 'е', '€'],
    'f': ['f', 'F', 'ƒ', '|=', 'ph', 'ғ'],
    'g': ['g', 'G', '9', '6', '&', 'ğ', 'ɢ'],
    'h': ['h', 'H', '#', '|-|', '}{', 'н', 'ħ'],
    'i': ['i', 'I', '1', '!', '|', 'ï', 'ι', '¡', 'ɪ', 'ɨ'],
    'j': ['j', 'J', '_|', 'ĵ', 'ɉ'],
    'k': ['k', 'K', '|<', '|{', 'ķ', 'κ', 'ĸ'],
    'l': ['l', 'L', '1', '|', '£', 'ℓ', 'ł', 'ⅼ'],
    'm': ['m', 'M', '|V|', '^^', '₥', 'м', 'ⅿ'],
    'n': ['n', 'N', '|\\|', '/\\/', 'η', 'и', 'п'],
    'o': ['o', 'O', '0', '()', '[]', '<>', '°', 'ø', 'ö', 'σ'],
    'p': ['p', 'P', '|*', '|>', 'þ', 'ρ', 'р'],
    'q': ['q', 'Q', '0_', '9', 'φ', 'ԛ'],
    'r': ['r', 'R', '|2', '|`', '®', 'г', 'я', 'ʁ'],
    's': ['s', 'S', '5', '$', 'z', '§', 'ş', 'ѕ', '𐑈'],
    't': ['t', 'T', '7', '+', '†', 'ť', 'т', 'τ'],
    'u': ['u', 'U', '|_|', 'µ', 'ü', 'υ', 'ʊ'],
    'v': ['v', 'V', '\\/', '√', '▼', 'ν', 'ѵ'],
    'w': ['w', 'W', '\\/\\/', 'VV', 'ω', 'ш', 'щ'],
    'x': ['x', 'X', '><', '×', 'χ', '✕'],
    'y': ['y', 'Y', '`/', '¥', 'ÿ', 'γ', 'у'],
    'z': ['z', 'Z', '2', '7_', 'ζ', 'z'],
}

# ============================================================
# SECTION 3: COMMON PATTERNS & DATABASES
# ============================================================

COMMON_SUFFIXES = [
    '', '1', '12', '123', '1234', '12345', '123456', '1234567', '12345678',
    '!', '!!', '!@', '!@#', '!@#$', '@', '#', '$', '%', '^', '&', '*',
    '.', '..', '...', '?', '??', '!?', '?!',
    'pass', 'Pass', 'PASS', 'password', 'Password', 'PASSWORD',
    'admin', 'Admin', 'ADMIN',
    'test', 'Test', 'TEST', 'demo',
    '123!', '1234!', '12345!', '123!@#', '1234@#',
    'x', 'X', 'xx', 'XXX',
]

COMMON_PREFIXES = [
    '', '!', '@', '#', '$', '%', '!@', '!@#', '!@#$',
    'pass', 'Pass', 'P@ss', 'P@$$',
    'admin', 'Admin',
    'test', 'Test',
    'super', 'Super', 'SUPER',
    '1', '123',
]

YEARS_SHORT = [str(y)[-2:] for y in range(1970, 2031)]
YEARS_FULL = [str(y) for y in range(1970, 2031)]
YEARS_COMMON = ['2023', '2024', '2025', '2026', '23', '24', '25', '26']

MONTHS = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
]
MONTH_NAMES = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december',
]
DAYS = [str(d).zfill(2) for d in range(1, 32)] + [str(d) for d in range(1, 32)]

SEASONS = ['spring', 'summer', 'fall', 'autumn', 'winter', 'Spring', 'Summer', 'Fall', 'Autumn', 'Winter']
SEASONAL_WORDS = ['christmas', 'xmas', 'easter', 'halloween', 'summer', 'winter', 'thanksgiving',
                  'newyear', 'valentine', 'passover', 'ramadan', 'holiday',
                  'Christmas', 'Xmas', 'Easter', 'Halloween', 'Summer', 'Winter']

SPORTS_COMMON = ['football', 'soccer', 'basketball', 'baseball', 'hockey', 'tennis', 'golf',
                 'cricket', 'rugby', 'swimming', 'sports', 'sport',
                 'Football', 'Soccer', 'Basketball', 'Baseball']

# ============================================================
# SECTION 4: MARKOV CHAIN ENGINE
# ============================================================

class MarkovChain:
    """Nth-order Markov chain for password generation."""
    
    def __init__(self, order: int = 3, max_gen_length: int = 32):
        self.order = order
        self.max_gen_length = max_gen_length
        self.chain: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_counts: Dict[str, int] = defaultdict(int)
        self.trained = False
    
    def train(self, passwords: List[str]):
        """Train Markov model on a list of passwords."""
        for pwd in passwords:
            if len(pwd) < self.order + 1:
                continue
            padded = '\x02' * self.order + pwd + '\x03'
            for i in range(len(padded) - self.order):
                state = padded[i:i + self.order]
                next_char = padded[i + self.order]
                self.chain[state][next_char] += 1
                self.total_counts[state] += 1
        self.trained = True
    
    def train_from_file(self, filepath: str):
        """Train from a wordlist file (one password per line)."""
        passwords = []
        with open(filepath, 'r', errors='ignore') as f:
            for line in f:
                pwd = line.strip()
                if pwd and len(pwd) >= 4:
                    passwords.append(pwd)
        self.train(passwords)
        print(f"[Markov] Trained on {len(passwords)} passwords")
    
    def generate(self, seed: Optional[str] = None) -> str:
        """Generate a password using the Markov chain."""
        if not self.trained:
            return ""
        
        if seed:
            state = seed[-self.order:].lower() if len(seed) >= self.order else seed + '\x02' * (self.order - len(seed))
        else:
            state = '\x02' * self.order
        
        result = []
        for _ in range(self.max_gen_length):
            if state not in self.chain or self.total_counts[state] == 0:
                break
            
            choices = list(self.chain[state].keys())
            weights = [self.chain[state][c] for c in choices]
            
            try:
                next_char = random.choices(choices, weights=weights, k=1)[0]
            except:
                break
            
            if next_char == '\x03':
                break
            
            result.append(next_char)
            state = (state + next_char)[-self.order:]
        
        return ''.join(result)
    
    def generate_bulk(self, count: int, seeds: Optional[List[str]] = None) -> List[str]:
        """Generate multiple passwords."""
        passwords = []
        for i in range(count):
            if seeds:
                seed = random.choice(seeds)
                pwd = self.generate(seed)
            else:
                pwd = self.generate()
            if pwd and len(pwd) >= 4:
                passwords.append(pwd)
        return passwords


# ============================================================
# SECTION 5: KEYBOARD WALK GENERATOR
# ============================================================

def build_keyboard_graph(layout_rows: List[List[str]]) -> Dict[str, List[Tuple[str, int, int]]]:
    """Build adjacency graph from keyboard layout."""
    graph = {}
    rows = len(layout_rows)
    
    for r in range(rows):
        for c in range(len(layout_rows[r])):
            key = layout_rows[r][c]
            if key == ' ':
                continue
            neighbors = []
            # Adjacent positions (including diagonals)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < len(layout_rows[nr]):
                        neighbor = layout_rows[nr][nc]
                        if neighbor != ' ':
                            neighbors.append((neighbor, dr, dc))
            graph[key] = neighbors
    return graph


def generate_keyboard_walks(
    length: int = 8,
    layout_rows: List[List[str]] = QWERTY_ROWS,
    shift_layout: List[List[str]] = QWERTY_SHIFTED,
    include_shifted: bool = True,
    max_walks: int = 1000
) -> List[str]:
    """Generate keyboard walk passwords."""
    graph = build_keyboard_graph(layout_rows)
    all_keys = list(graph.keys())
    walks = set()
    
    for start_key in random.sample(all_keys, min(len(all_keys), 50)):
        for _ in range(max(1, max_walks // len(all_keys))):
            walk_chars = [start_key]
            current = start_key
            direction = None
            
            for _ in range(length - 1):
                neighbors = graph.get(current, [])
                if not neighbors:
                    break
                
                # Prefer continuing same direction
                if direction:
                    same_dir = [n for n in neighbors if n[1] == direction[0] and n[2] == direction[1]]
                    if same_dir:
                        chosen = random.choice(same_dir)
                    else:
                        chosen = random.choice(neighbors)
                else:
                    chosen = random.choice(neighbors)
                
                walk_chars.append(chosen[0])
                direction = (chosen[1], chosen[2])
                current = chosen[0]
            
            walk = ''.join(walk_chars)
            if len(walk) == length:
                walks.add(walk.lower())
                
                if include_shifted:
                    shifted_walk = ''
                    for i, ch in enumerate(walk.lower()):
                        # Randomly shift some characters
                        if random.random() < 0.3:
                            for sr in range(len(shift_layout)):
                                for sc in range(len(shift_layout[sr])):
                                    if layout_rows[sr][sc].lower() == ch:
                                        shifted_walk += shift_layout[sr][sc]
                                        break
                                else:
                                    continue
                                break
                            else:
                                shifted_walk += ch.upper()
                        else:
                            shifted_walk += ch
                    if shifted_walk:
                        walks.add(shifted_walk)
    
    return list(walks)[:max_walks]


def generate_known_keyboard_patterns() -> List[str]:
    """Generate known common keyboard walk patterns."""
    patterns = [
        # QWERTY horizontal
        'qwerty', 'qwertyuiop', 'qwertyuiop[]', 'asdfghjkl', 'zxcvbnm',
        'qwerty12345', 'qwerty!@#$%', 'qwerty1', 'qwerty123',
        'asdfgh', 'asdfghjkl;', 'zxcvbn', 'zxcvbnm,.',
        # QWERTY vertical/diagonal
        '1qaz', '1qaz2wsx', '1qazxsw2', '1qaz@wsx',
        '2wsx', '3edc', '4rfv', '5tgb', '6yhn',
        '7ujm', '8ik,', '9ol.', '0p;/',
        'zaq1', 'xsw2', 'cde3', 'vfr4', 'bgt5', 'nhy6', 'mju7',
        # QWERTY reverse
        'rewq', 'poiuytrewq', 'lkjhgfdsa', 'mnbvcxz',
        'trewq', 'ytrewq',
        # Common combos
        '1qazxsw2', 'qazwsx', 'qazwsxedc', 'qweasdzxc',
        '1q2w3e', '1q2w3e4r', 'q1w2e3', 'q1w2e3r4',
        '12qwaszx', 'zaq!xsw@cde#',
        # Numbers + letters
        '123qwe', 'qwe123', '1234qwer', 'qwer1234',
        '1q2w3e4r', 'q1w2e3r4t5',
        # Phone keypad patterns
        '123456', '123456789', '12369874', '1478963', '159357',
        # Repeated patterns
        'qwertyqwerty', 'asdfasdf', 'qwertyuiopqwertyuiop',
        # Circle patterns
        '1qaz2wsx3edc', 'zaq1xsw2cde3',
        'qazwsxedcrfvtgb', 'zaq!xsw@cde#vfr$',
        # Shifts
        'QAZWSXEDC', '!QAZ@WSX#EDC', 'ZAQ!XSW@CDE#',
        '!@#$%^&*()', '~!@#$%^&*',
    ]
    return list(set(patterns))


# ============================================================
# SECTION 6: DATE & BIRTHDAY GENERATOR
# ============================================================

def generate_date_variations(
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    range_years: Tuple[int, int] = (1950, 2010),
    include_relative: bool = True
) -> List[str]:
    """Generate all possible date format permutations."""
    dates = set()
    
    if day and month and year:
        date_combos = [(day, month, year)]
    else:
        date_combos = []
        # Generate all dates in range
        for y in range(range_years[0], range_years[1] + 1):
            for m in range(1, 13):
                for d in range(1, 29):  # Avoid invalid dates
                    date_combos.append((d, m, y))
        # Limit if too many
        if len(date_combos) > 10000:
            date_combos = random.sample(date_combos, 10000)
    
    for d, m, y in date_combos:
        d_str = str(d)
        d_zfill = str(d).zfill(2)
        m_str = str(m)
        m_zfill = str(m).zfill(2)
        y_full = str(y)
        y_short = str(y)[-2:]
        
        formats = [
            f"{d_zfill}{m_zfill}{y_full}",      # DDMMYYYY
            f"{d_zfill}{m_zfill}{y_short}",      # DDMMYY
            f"{m_zfill}{d_zfill}{y_full}",       # MMDDYYYY
            f"{m_zfill}{d_zfill}{y_short}",      # MMDDYY
            f"{y_full}{m_zfill}{d_zfill}",       # YYYYMMDD
            f"{y_short}{m_zfill}{d_zfill}",      # YYMMDD
            f"{y_full}{d_zfill}{m_zfill}",       # YYYYDDMM
            f"{d_zfill}{m_zfill}",               # DDMM
            f"{m_zfill}{d_zfill}",               # MMDD
            f"{d_zfill}{m_str}{y_full}",         # D M YYYY
            f"{d_str}{m_zfill}{y_full}",         # D MM YYYY
            f"{d_zfill}{y_full}",                # DDYYYY
            f"{d_str}{y_full}",                  # DYYYY
            f"{d_zfill}.{m_zfill}.{y_full}",     # DD.MM.YYYY
            f"{d_zfill}/{m_zfill}/{y_full}",     # DD/MM/YYYY
            f"{d_zfill}-{m_zfill}-{y_full}",     # DD-MM-YYYY
            f"{y_full}{d_zfill}{m_zfill}",       # YYYYDDMM
        ]
        dates.update(formats)
    
    # Add relative dates
    if include_relative:
        today = date.today()
        for days_offset in [0, -1, -365, -730, -3650]:
            d = today + timedelta(days=days_offset)
            for fmt_d, fmt_m, fmt_y in [
                (d.day, d.month, d.year),
                (d.month, d.day, d.year),  # US format
            ]:
                dates.add(f"{fmt_d}{fmt_m}{fmt_y}")
                dates.add(f"{str(fmt_d).zfill(2)}{str(fmt_m).zfill(2)}{str(fmt_y)[-2:]}")
    
    return list(dates)


# ============================================================
# SECTION 7: HASHCAT RULE ENGINE (188+ RULES)
# ============================================================

class HashcatRuleEngine:
    """Implementation of Hashcat's rule-based attack engine."""
    
    @staticmethod
    def apply_rule(word: str, rule: str) -> Optional[str]:
        """Apply a single hashcat rule to a word. Returns None if rule rejects the word."""
        if not word:
            return None
        
        # Work on a mutable list
        chars = list(word)
        orig = word
        
        i = 0
        while i < len(rule):
            cmd = rule[i]
            i += 1
            
            if cmd == ':':  # No-op
                continue
            
            elif cmd == 'l':  # Lowercase all
                chars = [c.lower() for c in chars]
            
            elif cmd == 'u':  # Uppercase all
                chars = [c.upper() for c in chars]
            
            elif cmd == 'c':  # Capitalize first letter, lowercase rest
                if chars:
                    chars[0] = chars[0].upper()
                    for j in range(1, len(chars)):
                        chars[j] = chars[j].lower()
            
            elif cmd == 'C':  # Lowercase first, uppercase rest
                if chars:
                    chars[0] = chars[0].lower()
                    for j in range(1, len(chars)):
                        chars[j] = chars[j].upper()
            
            elif cmd == 't':  # Toggle case all characters
                for j in range(len(chars)):
                    chars[j] = chars[j].swapcase()
            
            elif cmd == 'T':  # Toggle case at position N
                if i < len(rule):
                    pos = int(rule[i])
                    i += 1
                    if pos < len(chars):
                        chars[pos] = chars[pos].swapcase()
            
            elif cmd == 'r':  # Reverse
                chars = chars[::-1]
            
            elif cmd == 'd':  # Duplicate
                chars = chars + chars[:]
            
            elif cmd == 'D':  # Duplicate N times
                if i < len(rule):
                    n = int(rule[i])
                    i += 1
                    chars = chars * (n + 1)
            
            elif cmd == 'p':  # Duplicate prepend (add lowercase to front)
                if i < len(rule):
                    n = int(rule[i])
                    i += 1
                    chars = chars[-n:] + chars
            
            elif cmd == 'P':  # Duplicate prepend (add uppercase to front)
                if i < len(rule):
                    n = int(rule[i])
                    i += 1
                    prefix = ''.join(chars[-n:]).upper()
                    chars = list(prefix) + chars
            
            elif cmd == 'f':  # Rotate left
                if chars:
                    chars = chars[1:] + [chars[0]]
            
            elif cmd == 'F':  # Rotate right
                if chars:
                    chars = [chars[-1]] + chars[:-1]
            
            elif cmd == '{':  # Shift left (first to end)
                if chars:
                    chars = chars[1:] + [chars[0]]
            
            elif cmd == '}':  # Shift right (last to front)
                if chars:
                    chars = [chars[-1]] + chars[:-1]
            
            elif cmd == '$':  # Append character
                if i < len(rule):
                    chars.append(rule[i])
                    i += 1
            
            elif cmd == '^':  # Prepend character
                if i < len(rule):
                    chars.insert(0, rule[i])
                    i += 1
            
            elif cmd == '[':  # Truncate first character
                if chars:
                    chars = chars[1:]
            
            elif cmd == ']':  # Truncate last character
                if chars:
                    chars = chars[:-1]
            
            elif cmd == 'k':  # Swap first two
                if len(chars) >= 2:
                    chars[0], chars[1] = chars[1], chars[0]
            
            elif cmd == 'K':  # Swap last two
                if len(chars) >= 2:
                    chars[-1], chars[-2] = chars[-2], chars[-1]
            
            elif cmd == 'x':  # Extract: xNM - extract N chars from position M
                if i + 1 < len(rule):
                    n = int(rule[i]); i += 1
                    m = int(rule[i]); i += 1
                    if m < len(chars):
                        chars = chars[m:m+n]
                    else:
                        return None
            
            elif cmd == 'i':  # Insert: iNP - insert at N from position P
                if i + 1 < len(rule):
                    n = int(rule[i]); i += 1
                    p = int(rule[i]); i += 1
                    if p < len(chars) and n < len(chars):
                        inserted = chars[n]
                        chars = chars[:p] + [inserted] + chars[p:]
            
            elif cmd == 'o':  # Overwrite: oNC - overwrite at N with character
                if i + 1 < len(rule):
                    n = int(rule[i]); i += 1
                    c = rule[i]; i += 1
                    if n < len(chars):
                        chars[n] = c
            
            elif cmd == "s":  # Substitute: sXY - replace X with Y
                if i + 1 < len(rule):
                    x = rule[i]; i += 1
                    y = rule[i]; i += 1
                    chars = [y if c == x else c for c in chars]
            
            elif cmd == '@':  # Purge: @X - remove all X
                if i < len(rule):
                    x = rule[i]; i += 1
                    chars = [c for c in chars if c != x]
            
            elif cmd == '!':  # Purge at position: !N - remove char at position N
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    if n < len(chars):
                        chars = chars[:n] + chars[n+1:]
            
            elif cmd == "'":  # Truncate at N: 'N - keep first N chars
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars[:n]
            
            elif cmd == 'q':  # Duplicate prepend N times to front
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = (chars[:n] * 2) + chars[n:]
            
            elif cmd == 'E':  # Lowercase all after position N
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    for j in range(n, len(chars)):
                        chars[j] = chars[j].lower()
            
            elif cmd == 'e':  # Uppercase all after position N
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    for j in range(n, len(chars)):
                        chars[j] = chars[j].upper()
            
            elif cmd == 'I':  # Insert at position N
                if i + 1 < len(rule):
                    n = int(rule[i]); i += 1
                    c = rule[i]; i += 1
                    if n <= len(chars):
                        chars.insert(n, c)
            
            elif cmd == 'V':  # Duplicate entire word N times
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars * n
            
            elif cmd == 'Z':  # Duplicate first N characters and append
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars + chars[:n]
            
            elif cmd == 'z':  # Duplicate last N characters and prepend
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars[-n:] + chars
            
            elif cmd == '_':  # Mirror (word + reversed)
                chars = chars + chars[::-1]
            
            elif cmd == '+':  # Append (same as $ but reads just 1 char)
                if i < len(rule):
                    chars.append(rule[i])
                    i += 1
            
            elif cmd == '-':  # Prepend (same as ^ but reads just 1 char)
                if i < len(rule):
                    chars.insert(0, rule[i])
                    i += 1
            
            elif cmd == '.':  # Append new char from ascii shift
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    if n < len(chars):
                        chars.append(chr((ord(chars[n]) + 1) % 128))
            
            elif cmd == ',':  # Prepend new char from ascii shift
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    if n < len(chars):
                        chars.insert(0, chr((ord(chars[n]) + 1) % 128))
            
            elif cmd == 'y':  # Duplicate first N chars and prepend
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars[:n] + chars
            
            elif cmd == 'Y':  # Duplicate last N chars and append
                if i < len(rule):
                    n = int(rule[i]); i += 1
                    chars = chars + chars[-n:]
            
            elif cmd == 'L':  # Lowercase all and append to self
                lower = [c.lower() for c in chars]
                chars = chars + lower
            
            elif cmd == 'u':  # Uppercase all and append to self (already handled)
                pass
            
            elif cmd == 'C':  # Already handled above
                pass
        
        result = ''.join(chars)
        return result if result else None
    
    @staticmethod
    def apply_rule_to_list(words: List[str], rule: str) -> List[str]:
        """Apply a rule to all words."""
        results = []
        for word in words:
            mutated = HashcatRuleEngine.apply_rule(word, rule)
            if mutated and mutated != word:
                results.append(mutated)
        return results
    
    @staticmethod
    def get_builtin_rules() -> List[str]:
        """Return a comprehensive set of hashcat-like rules."""
        rules = [
            # No change
            ':',
            # Case mutations
            'l', 'u', 'c', 'C', 't',
            # Reverse
            'r',
            # Duplicate
            'd',
            # Rotate
            'f', 'F',
            # Swap first/last two
            'k', 'K',
            # Append single chars
            '$1', '$2', '$3', '$4', '$5', '$6', '$7', '$8', '$9', '$0',
            '$!', '$@', '$#', '$$', '$%', '$^', '$&', '$*',
            # Prepend single chars
            '^1', '^2', '^3', '^4', '^5', '^6', '^7', '^8', '^9', '^0',
            '^!', '^@', '^#', '^$', '^%',
            # Toggle at positions
            'T0', 'T1', 'T2', 'T3',
            # Substitute common
            'ss$', 'sS5', 'sa@', 'sa4', 'se3', 'sl1', 'so0', 'si1', 'st7',
            # Combinations
            'u $1', 'l $1', 'c $1', 'u $!', 'l $!', 'c $!',
            'u $123', 'l $123', 'c $123', 'u $1234', 'c $1234',
            'u $2024', 'l $2024', 'c $2024', 'c $2025', 'c $2026',
            'u $!@#', 'l $!@#', 'c $!@#',
            '^! u', '^! l', '^! c',
            '^@ u', '^@ l', '^@ c',
            '^# u', '^# l', '^# c',
            'r $1', 'r $!', 'r $123',
            'u r $1', 'c r $1', 'l r $1',
            'd $1', 'd $!', 'd $123',
            'u d', 'c d', 'l d',
            'k r', 'K r',
            # Mirror
            '_', 'u _', 'c _', 'l _',
            # Truncate + append
            "'1 $1", "'2 $1", "'3 $1", "'4 $1",
            "'1 $!", "'2 $!", "'3 $!",
            # Year combo
            'u $2023', 'u $2024', 'u $2025', 'u $2026',
            'c $2023', 'c $2024', 'c $2025', 'c $2026',
            'l $2023', 'l $2024', 'l $2025', 'l $2026',
            '^2023 u', '^2024 u', '^2025 u', '^2026 u',
            '^20 u', '^20 l', '^20 c',
        ]
        return rules


# ============================================================
# SECTION 8: OSINT PROFILER (CUPP-STYLE INTERACTIVE)
# ============================================================

class TargetProfile:
    """Store target information for OSINT-based password generation."""
    
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.nickname = ""
        self.birthday = None  # (day, month, year)
        self.maiden_name = ""
        self.spouse_name = ""
        self.spouse_birthday = None
        self.pet_names: List[str] = []
        self.children_names: List[str] = []
        self.company = ""
        self.department = ""
        self.town_city = ""
        self.street = ""
        self.postcode = ""
        self.hobby: List[str] = []
        self.sport: List[str] = []
        self.movie_or_show: List[str] = []
        self.music_band: List[str] = []
        self.food: List[str] = []
        self.car_model: List[str] = []
        self.phone_number = ""
        self.email_addresses: List[str] = []
        self.usernames: List[str] = []
        self.keywords: List[str] = []
        self.other_info: List[str] = []
    
    def to_keywords(self) -> List[str]:
        """Convert profile to list of keywords for password generation."""
        keywords = []
        # Names
        for name in [self.first_name, self.last_name, self.nickname, 
                      self.maiden_name, self.spouse_name]:
            if name:
                keywords.append(name)
        
        # Pet and children names
        keywords.extend(self.pet_names)
        keywords.extend(self.children_names)
        
        # Locations
        for loc in [self.town_city, self.street]:
            if loc:
                keywords.append(loc)
        
        # Company
        if self.company:
            keywords.append(self.company)
            # Company abbreviations
            for abbr in re.findall(r'\b[A-Z]\b', self.company):
                keywords.append(abbr)
        
        # Interests
        keywords.extend(self.hobby)
        keywords.extend(self.sport)
        keywords.extend(self.movie_or_show)
        keywords.extend(self.music_band)
        keywords.extend(self.food)
        keywords.extend(self.car_model)
        keywords.extend(self.keywords)
        keywords.extend(self.other_info)
        
        # Email/username components
        for email in self.email_addresses:
            local = email.split('@')[0]
            keywords.append(local)
            # Split on separators
            for part in re.split(r'[._\-@+]', local):
                if part and len(part) >= 2:
                    keywords.append(part)
        
        for username in self.usernames:
            keywords.append(username)
        
        # Phone number
        if self.phone_number:
            phone = re.sub(r'[^0-9]', '', self.phone_number)
            if len(phone) >= 4:
                keywords.append(phone[-4:])
            if len(phone) >= 6:
                keywords.append(phone[-6:])
            if len(phone) >= 8:
                keywords.append(phone[-8:])
        
        return list(set(keywords))
    
    def get_birthday_dates(self) -> List[Tuple[int, int, int]]:
        """Get birthday date tuples."""
        dates = []
        if self.birthday:
            dates.append(self.birthday)
        if self.spouse_birthday:
            dates.append(self.spouse_birthday)
        return dates


def interactive_profile() -> TargetProfile:
    """Interactive profile collection (CUPP-style)."""
    profile = TargetProfile()
    
    print("\n" + "=" * 60)
    print("  HYPERCRACK PROFILER — Interactive Target Profiling")
    print("=" * 60)
    print("  Answer as many questions as possible. Press Enter to skip.\n")
    
    profile.first_name = input("[?] First name: ").strip()
    profile.last_name = input("[?] Last name: ").strip()
    profile.nickname = input("[?] Nickname: ").strip()
    
    dob = input("[?] Date of birth (DD/MM/YYYY or DDMMYYYY): ").strip()
    if dob:
        dob_clean = re.sub(r'[^0-9]', '', dob)
        if len(dob_clean) == 8:
            profile.birthday = (int(dob_clean[0:2]), int(dob_clean[2:4]), int(dob_clean[4:8]))
    
    profile.maiden_name = input("[?] Maiden name: ").strip()
    profile.spouse_name = input("[?] Partner's name: ").strip()
    
    spouse_dob = input("[?] Partner's DOB (DD/MM/YYYY): ").strip()
    if spouse_dob:
        sd_clean = re.sub(r'[^0-9]', '', spouse_dob)
        if len(sd_clean) == 8:
            profile.spouse_birthday = (int(sd_clean[0:2]), int(sd_clean[2:4]), int(sd_clean[4:8]))
    
    pets = input("[?] Pet name(s) (comma separated): ").strip()
    if pets:
        profile.pet_names = [p.strip() for p in pets.split(',') if p.strip()]
    
    children = input("[?] Children's name(s) (comma separated): ").strip()
    if children:
        profile.children_names = [c.strip() for c in children.split(',') if c.strip()]
    
    profile.company = input("[?] Company name: ").strip()
    profile.department = input("[?] Department: ").strip()
    profile.town_city = input("[?] City/Town: ").strip()
    profile.street = input("[?] Street name: ").strip()
    
    hobbies = input("[?] Hobbies (comma separated): ").strip()
    if hobbies:
        profile.hobby = [h.strip() for h in hobbies.split(',') if h.strip()]
    
    sports = input("[?] Favorite sports/teams (comma separated): ").strip()
    if sports:
        profile.sport = [s.strip() for s in sports.split(',') if s.strip()]
    
    movies = input("[?] Movies/TV shows (comma separated): ").strip()
    if movies:
        profile.movie_or_show = [m.strip() for m in movies.split(',') if m.strip()]
    
    music = input("[?] Bands/Musicians (comma separated): ").strip()
    if music:
        profile.music_band = [m.strip() for m in music.split(',') if m.strip()]
    
    food = input("[?] Favorite food/drink (comma separated): ").strip()
    if food:
        profile.food = [f.strip() for f in food.split(',') if f.strip()]
    
    car = input("[?] Car model(s) (comma separated): ").strip()
    if car:
        profile.car_model = [c.strip() for c in car.split(',') if c.strip()]
    
    profile.phone_number = input("[?] Phone number: ").strip()
    
    emails = input("[?] Email(s) (comma separated): ").strip()
    if emails:
        profile.email_addresses = [e.strip() for e in emails.split(',') if e.strip()]
    
    usernames = input("[?] Username(s) (comma separated): ").strip()
    if usernames:
        profile.usernames = [u.strip() for u in usernames.split(',') if u.strip()]
    
    extra = input("[?] Other keywords (comma separated): ").strip()
    if extra:
        profile.keywords = [k.strip() for k in extra.split(',') if k.strip()]
    
    return profile


# ============================================================
# SECTION 9: PASSWORD MUTATION ENGINE (CORE)
# ============================================================

class HyperCrackEngine:
    """The main mutation engine combining all techniques."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.markov = MarkovChain(order=self.config.get('markov_order', 3))
        self.rule_engine = HashcatRuleEngine()
        self.profile: Optional[TargetProfile] = None
        self.passwords: Set[str] = set()
        self.stats = {
            'base_words': 0,
            'case_variants': 0,
            'leet_variants': 0,
            'date_variants': 0,
            'keyboard_variants': 0,
            'rule_mutations': 0,
            'markov_generated': 0,
            'seasonal': 0,
            'total_generated': 0,
        }
    
    def set_profile(self, profile: TargetProfile):
        """Set the target profile."""
        self.profile = profile
    
    def load_markov_wordlist(self, filepath: str):
        """Load a wordlist for Markov training."""
        if os.path.exists(filepath):
            self.markov.train_from_file(filepath)
    
    # --------------------------------------------------------
    # Core generators
    # --------------------------------------------------------
    
    def generate_case_variations(self, word: str) -> List[str]:
        """Generate all case variations."""
        variations = set()
        if not word:
            return []
        
        variations.add(word)
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.capitalize())
        variations.add(word.title())
        
        # Toggle each position (for short words, do all; for long, sample)
        if len(word) <= 8:
            # Full enumeration of case
            for mask in range(1, 1 << len(word)):
                mutated = ''
                for j in range(len(word)):
                    if mask & (1 << j):
                        mutated += word[j].upper()
                    else:
                        mutated += word[j].lower()
                variations.add(mutated)
        else:
            # Random sampling of case patterns
            for _ in range(500):
                mutated = ''.join(
                    c.upper() if random.random() < 0.3 else c.lower()
                    for c in word
                )
                variations.add(mutated)
        
        # First letter uppercase rest lowercase
        if len(word) > 1:
            variations.add(word[0].upper() + word[1:].lower())
            variations.add(word[0].lower() + word[1:].upper())
        
        return list(variations)
    
    def generate_leet_variations(self, word: str, max_per_word: int = 500) -> List[str]:
        """Generate leet speak variations."""
        results = set()
        word_lower = word.lower()
        
        # For each character position, try substitutions
        positions_to_sub = []
        for i, ch in enumerate(word_lower):
            if ch in LEET_MAP:
                positions_to_sub.append((i, LEET_MAP[ch]))
        
        if not positions_to_sub:
            return []
        
        # If many positions, limit
        if len(positions_to_sub) > 4:
            positions_to_sub = random.sample(positions_to_sub, 4)
        
        # Generate combinations
        for r in range(1, len(positions_to_sub) + 1):
            for combo in itertools.combinations(positions_to_sub, r):
                # For each selected position, pick a leet variant
                if len(results) >= max_per_word:
                    break
                
                # Generate a few specific substitutions
                for _ in range(3):  # Try 3 random variants per combo
                    char_list = list(word)
                    for pos, leet_options in combo:
                        char_list[pos] = random.choice(leet_options)
                    variant = ''.join(char_list)
                    if variant != word:
                        results.add(variant)
        
        return list(results)[:max_per_word]
    
    def generate_suffix_prefix_variations(self, word: str) -> List[str]:
        """Append/prepend common suffixes and prefixes."""
        results = set()
        
        for suffix in COMMON_SUFFIXES:
            if suffix:
                results.add(word + suffix)
                results.add(word.lower() + suffix)
                results.add(word.upper() + suffix)
                results.add(word.capitalize() + suffix)
        
        for prefix in COMMON_PREFIXES:
            if prefix:
                results.add(prefix + word)
                results.add(prefix + word.lower())
                results.add(prefix + word.upper())
                results.add(prefix + word.capitalize())
        
        return list(results)
    
    def generate_year_variations(self, word: str) -> List[str]:
        """Add year prefixes and suffixes."""
        results = set()
        for year in YEARS_COMMON + YEARS_FULL[-20:] + YEARS_SHORT[-20:]:
            results.add(word + year)
            results.add(year + word)
            results.add(word.lower() + year)
            results.add(year + word.lower())
            results.add(word.upper() + year)
            results.add(year + word.upper())
            results.add(word.capitalize() + year)
            results.add(year + word.capitalize())
        return list(results)
    
    def generate_combinator(self, word1: str, word2: str) -> List[str]:
        """Combine two words in various ways."""
        results = set()
        if not word1 or not word2:
            return []
        
        # Direct combination
        results.add(word1 + word2)
        results.add(word2 + word1)
        
        # With separators
        for sep in ['.', '_', '-', '@', '#', '!']:
            results.add(word1 + sep + word2)
            results.add(word2 + sep + word1)
        
        # First initial + second word
        results.add(word1[0] + word2)
        results.add(word2[0] + word1)
        
        # Truncated combos
        if len(word1) >= 3 and len(word2) >= 3:
            results.add(word1[:3] + word2[:3])
            results.add(word1[:4] + word2[:4])
        
        return list(results)
    
    def generate_from_keywords(self, keywords: List[str]) -> List[str]:
        """Generate passwords from a list of keywords using all techniques."""
        passwords = set()
        
        for kw in keywords:
            if len(kw) < 2:
                continue
            
            kw = kw.strip()
            
            # Base: the keyword itself
            self.stats['base_words'] += 1
            
            # Case variations
            case_vars = self.generate_case_variations(kw)
            passwords.update(case_vars)
            self.stats['case_variants'] += len(case_vars)
            
            # Leet variations
            leet_vars = self.generate_leet_variations(kw)
            passwords.update(leet_vars)
            self.stats['leet_variants'] += len(leet_vars)
            
            # Suffix/Prefix
            sp_vars = self.generate_suffix_prefix_variations(kw)
            passwords.update(sp_vars)
            
            # Year variations
            yr_vars = self.generate_year_variations(kw)
            passwords.update(yr_vars)
            self.stats['date_variants'] += len(yr_vars)
            
            # Reverse variations
            rev = kw[::-1]
            passwords.add(rev)
            passwords.add(rev.lower())
            passwords.add(rev.upper())
            passwords.add(rev.capitalize())
            
            # Duplicate
            passwords.add(kw * 2)
            passwords.add(kw.lower() * 2)
            
            # Apply hashcat rules
            for rule in HashcatRuleEngine.get_builtin_rules()[:50]:  # Use top 50 rules
                result = HashcatRuleEngine.apply_rule(kw, rule)
                if result and result != kw and len(result) <= 64:
                    passwords.add(result)
                    self.stats['rule_mutations'] += 1
        
        return list(passwords)
    
    def generate_seasonal_patterns(self) -> List[str]:
        """Generate seasonal password patterns."""
        results = set()
        
        for season in SEASONS:
            for year in YEARS_COMMON:
                results.add(f"{season}{year}")
                results.add(f"{season.lower()}{year}")
                results.add(f"{season.upper()}{year}")
                results.add(f"{season}{year}!")
                results.add(f"{season}{year}123")
                results.add(f"!{season}{year}")
                results.add(f"{season}.{year}")
        
        for holiday in SEASONAL_WORDS:
            for year in YEARS_COMMON:
                results.add(f"{holiday}{year}")
                results.add(f"{holiday.lower()}{year}")
        
        self.stats['seasonal'] += len(results)
        return list(results)
    
    def generate_phone_patterns(self, phone: str) -> List[str]:
        """Generate patterns from phone number."""
        results = set()
        clean = re.sub(r'[^0-9]', '', phone)
        
        if len(clean) < 4:
            return []
        
        # Last 4, 6, 8 digits
        for length in [4, 5, 6, 7, 8]:
            if len(clean) >= length:
                results.add(clean[-length:])
        
        # Common phone-to-password patterns
        results.add(clean)
        results.add(f"phone{clean[-4:]}")
        results.add(f"tel{clean[-4:]}")
        results.add(f"mobile{clean[-4:]}")
        results.add(f"cell{clean[-4:]}")
        results.add(f"0{clean}")
        results.add(f"+1{clean}")
        
        return list(results)
    
    def generate_markov_passwords(self, count: int = 1000, seeds: Optional[List[str]] = None) -> List[str]:
        """Generate Markov chain passwords."""
        if not self.markov.trained:
            return []
        passwords = self.markov.generate_bulk(count, seeds)
        self.stats['markov_generated'] += len(passwords)
        return passwords
    
    # --------------------------------------------------------
    # Main generation method
    # --------------------------------------------------------
    
    def generate_all(
        self,
        keywords: Optional[List[str]] = None,
        max_output: int = 10000000,
        enable_markov: bool = True,
        enable_keyboard: bool = True,
        enable_seasonal: bool = True,
        enable_dates: bool = True,
        enable_combinator: bool = True,
        markov_count: int = 2000,
        keyboard_count: int = 500,
        verbose: bool = True
    ) -> List[str]:
        """Generate all passwords using every available technique."""
        
        all_passwords = set()
        start_time = time.time()
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"  HYPERCRACK v2 — Generating passwords...")
            print(f"{'='*60}\n")
        
        # ---- Phase 1: Keyword-based generation ----
        if keywords:
            if verbose:
                print(f"[Phase 1] Keyword mutation ({len(keywords)} keywords)...")
            
            kw_passwords = self.generate_from_keywords(keywords)
            all_passwords.update(kw_passwords)
            
            if verbose:
                print(f"         → {len(kw_passwords):,} passwords")
        
        # ---- Phase 2: Combinator (word pairs) ----
        if enable_combinator and keywords and len(keywords) >= 2:
            if verbose:
                print(f"[Phase 2] Combinator attacks...")
            
            combo_count = 0
            # Only combine top keywords, limit combos
            top_keywords = [k for k in keywords if len(k) >= 3][:30]
            for i in range(len(top_keywords)):
                for j in range(i+1, len(top_keywords)):
                    combos = self.generate_combinator(top_keywords[i], top_keywords[j])
                    for c in combos:
                        if c not in all_passwords:
                            all_passwords.add(c)
                            combo_count += 1
                    
                    # Also add variations with suffixes
                    for c in list(combos)[:5]:
                        for suffix in ['1', '123', '!', '2024', '2025', '2026']:
                            all_passwords.add(c + suffix)
                            combo_count += 1
            
            if verbose:
                print(f"         → {combo_count:,} passwords")
        
        # ---- Phase 3: Keyboard walks ----
        if enable_keyboard:
            if verbose:
                print(f"[Phase 3] Keyboard walks...")
            
            # Known patterns
            known_patterns = generate_known_keyboard_patterns()
            for pattern in known_patterns:
                all_passwords.add(pattern)
                all_passwords.add(pattern + '123')
                all_passwords.add(pattern + '!')
                for year in ['2024', '2025', '2026']:
                    all_passwords.add(pattern + year)
            
            # Generated walks
            for length in [6, 7, 8, 9, 10, 12]:
                walks = generate_keyboard_walks(
                    length=length,
                    max_walks=keyboard_count // 6
                )
                all_passwords.update(walks)
                # Add some mutations
                for w in walks[:50]:
                    for suffix in ['123', '!', '1234']:
                        all_passwords.add(w + suffix)
            
            self.stats['keyboard_variants'] = len([p for p in all_passwords if len(p) >= 6])
            
            if verbose:
                print(f"         → {self.stats['keyboard_variants']:,} passwords")
        
        # ---- Phase 4: Seasonal & common patterns ----
        if enable_seasonal:
            if verbose:
                print(f"[Phase 4] Seasonal/holiday patterns...")
            
            seasonal = self.generate_seasonal_patterns()
            all_passwords.update(seasonal)
            
            if verbose:
                print(f"         → {len(seasonal):,} passwords")
        
        # ---- Phase 5: Date patterns ----
        if enable_dates:
            if verbose:
                print(f"[Phase 5] Date patterns...")
            
            if self.profile:
                for bd in self.profile.get_birthday_dates():
                    date_vars = generate_date_variations(bd[0], bd[1], bd[2])
                    all_passwords.update(date_vars)
            
            # Also add common date patterns
            common_dates = generate_date_variations(range_years=(1970, 2005))
            all_passwords.update(common_dates[:2000])  # Sample from huge set
            
            self.stats['date_variants'] = len(date_vars) if self.profile else 2000
            
            if verbose:
                print(f"         → {self.stats['date_variants']:,} passwords")
        
        # ---- Phase 6: Markov chain generation ----
        if enable_markov and self.markov.trained:
            if verbose:
                print(f"[Phase 6] Markov chain generation...")
            
            seeds = keywords[:50] if keywords else None
            markov_pwds = self.generate_markov_passwords(markov_count, seeds)
            all_passwords.update(markov_pwds)
            
            if verbose:
                print(f"         → {len(markov_pwds):,} passwords")
        
        # ---- Phase 7: Apply hashcat rule engine to entire set (sampled) ----
        if verbose:
            print(f"[Phase 7] Applying hashcat rule engine...")
        
        rule_engine = HashcatRuleEngine()
        rules = rule_engine.get_builtin_rules()
        
        # Sample a subset of current passwords to apply rules
        sample = random.sample(list(all_passwords), min(500, len(all_passwords)))
        rule_count = 0
        for pwd in sample:
            for rule in rules:
                mutated = rule_engine.apply_rule(pwd, rule)
                if mutated and mutated != pwd and len(mutated) <= 64:
                    all_passwords.add(mutated)
                    rule_count += 1
        
        if verbose:
            print(f"         → {rule_count:,} passwords")
        
        # ---- Phase 8: Common weak passwords ----
        if verbose:
            print(f"[Phase 8] Adding common weak passwords...")
        
        common_weak = self.get_common_weak_passwords()
        all_passwords.update(common_weak)
        
        if verbose:
            print(f"         → {len(common_weak):,} passwords")
        
        # Final dedup and sort
        result = sorted(all_passwords)
        self.stats['total_generated'] = len(result)
        
        elapsed = time.time() - start_time
        if verbose:
            print(f"\n{'='*60}")
            print(f"  DONE — {len(result):,} unique passwords generated")
            print(f"  Time: {elapsed:.1f}s")
            print(f"{'='*60}")
        
        return result
    
    @staticmethod
    def get_common_weak_passwords() -> List[str]:
        """Return a set of the most common weak passwords."""
        return [
            'password', '123456', '12345678', '123456789', '1234567890',
            '1234567', '12345', '1234', '123', '12', '1',
            'qwerty', 'qwerty123', 'qwerty12345', 'qwertyuiop',
            'asdfgh', 'asdfghjkl', 'zxcvbnm',
            'abc123', 'abcd1234', 'abcdef',
            'iloveyou', 'iloveu', 'love', 'princess', 'sunshine',
            'admin', 'administrator', 'root', 'toor',
            'welcome', 'welcome123', 'passw0rd', 'pass123',
            'monkey', 'dragon', 'master', 'master123',
            'letmein', 'letmein123', 'trustno1',
            'login', 'hello', 'hello123', 'shadow',
            'football', 'baseball', 'basketball', 'hockey', 'soccer',
            'charlie', 'chocolate', 'cookie', 'cheese', 'pepper',
            'sunshine', 'butterfly', 'diamond', 'thunder', 'phoenix',
            'starwars', 'solo', 'r2d2', 'c3po', 'yoda',
            'naruto', 'goku', 'pokemon', 'pikachu',
            'batman', 'superman', 'spiderman', 'ironman',
            'wolverine', 'magneto', 'avengers',
            'jordan', 'michael', 'miller', 'smith', 'jones', 'jackson',
            '!@#$%', '!@#$%^', '!@#$%^&', '!@#$%^&*',
            'changeme', 'default', 'guest', 'temp', 'temporary',
            'secret', 'summer2024', 'summer2025', 'winter2024',
            'password123', 'password1', 'password!', 'Password1',
            'P@ssw0rd', 'P@$$w0rd', 'Passw0rd', 'p@ssw0rd',
            'admin123', 'admin1234', 'Admin123', 'Admin@123',
            'Welcome1', 'Welcome123', 'Welcome@123',
            'Company123', 'Company2024', 'Company@123',
        ]
    
    def export_stats(self) -> dict:
        """Return generation statistics."""
        return self.stats


# ============================================================
# SECTION 10: OUTPUT FORMATTERS
# ============================================================

def write_output(passwords: List[str], output_file: str, format_type: str = 'plain'):
    """Write passwords to file in various formats."""
    output_path = Path(output_file)
    
    if format_type == 'plain':
        with open(output_path, 'w') as f:
            f.write('\n'.join(passwords) + '\n')
    
    elif format_type == 'hashcat':
        # Hashcat format: one hex-encoded hash per line (just passwords here)
        with open(output_path, 'w') as f:
            for pwd in passwords:
                f.write(f"{pwd}\n")
    
    elif format_type == 'json':
        with open(output_path, 'w') as f:
            json.dump({
                'generated_at': str(datetime.now()),
                'total_count': len(passwords),
                'passwords': passwords,
            }, f, indent=2)
    
    elif format_type == 'rules':
        # Output as hashcat rule file
        rules = HashcatRuleEngine.get_builtin_rules()
        with open(output_path, 'w') as f:
            for rule in rules:
                f.write(rule + '\n')
        print(f"[+] Exported {len(rules)} hashcat rules to {output_path}")
        return
    
    elif format_type == 'stats':
        counts = Counter()
        for pwd in passwords:
            counts[len(pwd)] += 1
        with open(output_path, 'w') as f:
            f.write(f"Total passwords: {len(passwords)}\n")
            f.write(f"Min length: {min(len(p) for p in passwords)}\n")
            f.write(f"Max length: {max(len(p) for p in passwords)}\n")
            f.write(f"Avg length: {sum(len(p) for p in passwords) / len(passwords):.1f}\n")
            f.write(f"\nLength distribution:\n")
            for length in sorted(counts):
                f.write(f"  {length}: {counts[length]} ({counts[length]/len(passwords)*100:.1f}%)\n")
        print(f"[+] Statistics written to {output_path}")
        return
    
    print(f"[+] Wrote {len(passwords):,} passwords to {output_path}")


# ============================================================
# SECTION 11: CLI & MAIN
# ============================================================

def main():
    banner = r"""
╔══════════════════════════════════════════════════════════════╗
║     ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗      ║
║     ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝      ║
║     ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║            ║
║     ██╔══██║  ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║            ║
║     ██║  ██║   ██║   ██║  ██║███████╗██║  ██║╚██████╗      ║
║     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝      ║
║                                        v2 — ULTIMATE EDITION ║
$$
╚══════════════════════════════════════════════════════════════╝
    """
    parser = argparse.ArgumentParser(
        description="HYPERCRACK v2 — Ultimate Password Mutation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive profiling (CUPP-style)
  python hypercrack.py --interactive -o wordlist.txt

  # Single username/keyword
  python hypercrack.py -k "johndoe" -o passwords.txt

  # Multiple keywords
  python hypercrack.py -k "john,doe,company,petname" -o passwords.txt --stats

  # Bulk from file
  python hypercrack.py -f names.txt -o wordlist.txt --combinator --keyboard

  # Markov chain only (needs training file)
  python hypercrack.py --markov-only --train rockyou.txt -o markov.txt -c 10000

  # Keyboard walks only
  python hypercrack.py --keyboard-only --keyboard-length 8 -o walks.txt

  # Export hashcat rules
  python hypercrack.py --export-rules rules.txt

  # Generate from username with all techniques, limit output
  python hypercrack.py -k "sanjidaakter8152" -o sanjida.txt --max 50000 --stats
        """
    )

    # Core input
    parser.add_argument('-k', '--keywords', help='Keywords/username (comma separated)')
    parser.add_argument('-f', '--file', help='File with keywords (one per line)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive profiling mode (CUPP-style)')
    parser.add_argument('-o', '--output', default='hypercrack_output.txt',
                        help='Output file (default: hypercrack_output.txt)')
    parser.add_argument('--format', choices=['plain', 'json', 'hashcat', 'stats', 'rules'],
                        default='plain', help='Output format')
    parser.add_argument('-c', '--count', type=int, default=10000000,
                        help='Max passwords to generate')

    # Toggle modules
    parser.add_argument('--no-markov', action='store_true', help='Disable Markov chain')
    parser.add_argument('--no-keyboard', action='store_true', help='Disable keyboard walks')
    parser.add_argument('--no-seasonal', action='store_true', help='Disable seasonal patterns')
    parser.add_argument('--no-dates', action='store_true', help='Disable date patterns')
    parser.add_argument('--no-combinator', action='store_true', help='Disable combinator attacks')
    parser.add_argument('--no-leet', action='store_true', help='Disable leet speak')
    parser.add_argument('--no-rules', action='store_true', help='Disable hashcat rules')

    # Special modes
    parser.add_argument('--markov-only', action='store_true',
                        help='Generate only Markov chain passwords')
    parser.add_argument('--keyboard-only', action='store_true',
                        help='Generate only keyboard walks')
    parser.add_argument('--export-rules', metavar='FILE',
                        help='Export hashcat rules to file and exit')
    parser.add_argument('--train', help='Wordlist file for Markov training')

    # Keyboard settings
    parser.add_argument('--keyboard-length', type=int, default=8,
                        help='Keyboard walk length (default: 8)')
    parser.add_argument('--keyboard-count', type=int, default=1000,
                        help='Number of keyboard walks to generate (default: 1000)')

    # Markov settings
    parser.add_argument('--markov-order', type=int, default=3,
                        help='Markov chain order (default: 3)')
    parser.add_argument('--markov-count', type=int, default=2000,
                        help='Markov passwords to generate (default: 2000)')

    # Misc
    parser.add_argument('--max', type=int, default=10000000,
                        help='Max unique passwords in output (default: 10M)')
    parser.add_argument('--stats', action='store_true', help='Show generation statistics')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')

    args = parser.parse_args()

    # Handle special modes
    if args.export_rules:
        rules = HashcatRuleEngine.get_builtin_rules()
        with open(args.export_rules, 'w') as f:
            for rule in rules:
                f.write(rule + '\n')
        print(f"[+] Exported {len(rules)} hashcat rules to {args.export_rules}")
        return

    if args.keyboard_only:
        print(f"[*] Generating keyboard walks (length={args.keyboard_length})...")
        walks = generate_keyboard_walks(
            length=args.keyboard_length,
            max_walks=args.keyboard_count
        )
        known = generate_known_keyboard_patterns()
        all_walks = sorted(set(walks + known))
        write_output(all_walks, args.output, args.format)
        print(f"[+] {len(all_walks):,} keyboard walk passwords generated")
        return

    # Initialize engine
    engine = HyperCrackEngine({'markov_order': args.markov_order})

    # Load Markov training data if provided
    if args.train:
        if os.path.exists(args.train):
            engine.load_markov_wordlist(args.train)
        else:
            print(f"[!] Training file not found: {args.train}")

    # Collect keywords
    keywords = []

    if args.interactive:
        profile = interactive_profile()
        engine.set_profile(profile)
        keywords = profile.to_keywords()
        print(f"[+] Profile extracted {len(keywords)} keywords")

        # Process birthdays
        if profile.get_birthday_dates():
            print(f"[+] Birthday data will be used for date patterns")

    if args.keywords:
        kw_list = [k.strip() for k in args.keywords.split(',') if k.strip()]
        keywords.extend(kw_list)

    if args.file:
        if os.path.exists(args.file):
            with open(args.file, 'r') as f:
                file_kw = [line.strip() for line in f if line.strip()]
            keywords.extend(file_kw)
            print(f"[+] Loaded {len(file_kw)} keywords from {args.file}")
        else:
            print(f"[!] File not found: {args.file}")
            sys.exit(1)

    keywords = list(set(keywords))

    if not keywords:
        print("[!] No keywords provided. Use -k, -f, or --interactive")
        parser.print_help()
        sys.exit(1)

    print(f"[+] Total unique keywords: {len(keywords)}")
    if not args.quiet:
        print(f"[+] Keywords: {', '.join(keywords[:20])}{'...' if len(keywords) > 20 else ''}")

    # Generate passwords
    passwords = engine.generate_all(
        keywords=keywords,
        max_output=args.max,
        enable_markov=not args.no_markov and not args.markov_only,
        enable_keyboard=not args.no_keyboard,
        enable_seasonal=not args.no_seasonal,
        enable_dates=not args.no_dates,
        enable_combinator=not args.no_combinator,
        markov_count=args.markov_count,
        keyboard_count=args.keyboard_count,
        verbose=not args.quiet
    )

    # Apply max limit
    if len(passwords) > args.max:
        print(f"[!] Limiting output to {args.max:,} passwords (random sample)")
        passwords = random.sample(passwords, args.max)
        passwords.sort()

    # Write output
    write_output(passwords, args.output, args.format)

    # Show stats
    if args.stats or not args.quiet:
        print(f"\n{'='*60}")
        print(f"  GENERATION SUMMARY")
        print(f"{'='*60}")
        print(f"  Total passwords     : {len(passwords):,}")
        if passwords:
            print(f"  Min length          : {min(len(p) for p in passwords)}")
            print(f"  Max length          : {max(len(p) for p in passwords)}")
            print(f"  Avg length          : {sum(len(p) for p in passwords) / len(passwords):.1f}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
