# HyperCrack
Ultimate Password enumeration
# HyperCrack v2
### Ultimate Password Mutation Engine

> A modular Python password candidate generation framework combining multiple mutation techniques into a single extensible engine.

> **For security research, password auditing, defensive testing, and educational purposes only.**

---

# Overview

HyperCrack v2 is an advanced password mutation engine inspired by several well-known password generation techniques.

Instead of relying on a single strategy, HyperCrack combines:

- Keyword mutations
- Case permutations
- Leetspeak transformations
- Date generation
- Keyboard walk generation
- Markov-chain password generation
- Hashcat-style rule mutations
- Combinator attacks
- Seasonal patterns
- Interactive OSINT-style profiling

The engine is modular, allowing every generation module to be enabled or disabled independently.

---

# Features

## Keyword Mutation

Generate thousands of variations from one or more keywords.

Example

```
john
John
JOHN
jOhN
john123
john2025
John!
```

---

## Extended Leetspeak Engine

Supports a large substitution database.

Examples

```
password
p@ssword
P4$$w0rd
pa55w0rd
```

---

## Case Mutation

Generates

- lowercase
- UPPERCASE
- Capitalized
- Mixed case
- Randomized case

---

## Date Generator

Creates common password date patterns.

Examples

```
01011990
19900101
01-01-1990
010190
```

Supports

- birthdays
- current years
- relative dates
- multiple formats

---

## Keyboard Walk Generator

Produces realistic keyboard patterns.

Examples

```
qwerty
asdfgh
1qaz2wsx
qazwsxedc
123456
```

Supports

- QWERTY
- AZERTY
- DVORAK
- keypad layouts

---

## Hashcat Rule Engine

Built-in implementation of common Hashcat mutation rules.

Examples

- uppercase
- lowercase
- reverse
- duplicate
- append
- prepend
- substitutions

Over 180+ rule combinations included.

---

## Markov Chain Generator

Train a probabilistic language model using an existing wordlist.

Example

```
python hypercrack.py \
    --train rockyou.txt \
    --markov-only \
    -c 10000
```

---

## Combinator Attack

Combines multiple keywords automatically.

Example

Input

```
john
smith
```

Output

```
johnsmith
smithjohn
john_smith
john123smith
```

---

## Seasonal Password Generator

Creates realistic seasonal passwords.

Examples

```
Summer2025
Winter2024
Christmas2025
Halloween123
```

---

## Interactive Profiling

Collect target information similar to CUPP.

Supports

- names
- nicknames
- birthdays
- pets
- children
- company
- hobbies
- sports
- favorite movies
- usernames
- emails
- phone numbers

Automatically converts profile information into password candidates.

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/hypercrack.git

cd hypercrack
```

Python 3.10+

No external dependencies are required.

Run

```bash
python hypercrack.py --help
```

---

# Usage

## Interactive Mode

```bash
python hypercrack.py --interactive \
    -o wordlist.txt
```

---

## Single Keyword

```bash
python hypercrack.py \
    -k john
```

---

## Multiple Keywords

```bash
python hypercrack.py \
    -k "john,smith,dog,company"
```

---

## Import Keywords From File

```bash
python hypercrack.py \
    -f keywords.txt
```

---

## Keyboard Walk Generation

```bash
python hypercrack.py \
    --keyboard-only
```

---

## Markov Generation

```bash
python hypercrack.py \
    --markov-only \
    --train rockyou.txt
```

---

## Export Rules

```bash
python hypercrack.py \
    --export-rules rules.txt
```

---

## Statistics

```bash
python hypercrack.py \
    --stats
```

---

# Command Line Options

| Option | Description |
|---------|-------------|
| -k | Keywords |
| -f | Import keywords file |
| -i | Interactive profile |
| -o | Output filename |
| --format | Output format |
| --count | Maximum generation count |
| --markov-only | Markov mode |
| --keyboard-only | Keyboard walk mode |
| --train | Markov training wordlist |
| --export-rules | Export built-in rules |
| --stats | Show statistics |
| --quiet | Minimal output |

---

# Output Formats

Supported formats

```
plain
json
hashcat
stats
rules
```

---

# Architecture

```
                Keywords
                    │
                    ▼
          Keyword Mutation Engine
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Case        Leetspeak       Date Engine
      ▼             ▼             ▼
      └──────► Password Pool ◄────┘
                    │
                    ▼
         Hashcat Rule Engine
                    │
                    ▼
          Keyboard Walk Engine
                    │
                    ▼
           Markov Generator
                    │
                    ▼
          Duplicate Removal
                    │
                    ▼
            Output Formatter
```

---

# Project Structure

```
hypercrack.py

├── Keyboard layouts
├── Leetspeak engine
├── Markov chain
├── Keyboard walks
├── Date generator
├── Hashcat rule engine
├── Interactive profiler
├── Password engine
├── Output formatter
└── CLI
```

---

# Example

Generate a wordlist from one username

```bash
python hypercrack.py \
-k sanjidaakter8152 \
-o passwords.txt \
--stats
```

Output

```
Total generated:

82,000+

Average length:

11.8

Output:

passwords.txt
```

---

# Performance

Typical generation speeds

| Keywords | Generated |
|----------|-----------|
| 1 | 40k–100k |
| 5 | 200k–600k |
| 20 | 1M+ |

Generation depends on enabled modules.

---

# Future Improvements

- GPU-assisted mutations
- PCFG generator
- Neural language models
- Password scoring
- Bloom filter deduplication
- Distributed generation
- Plugin system
- Additional keyboard layouts
- Rule optimization

---

# Disclaimer

This software is intended **only** for:

- security research
- defensive password auditing
- penetration testing performed with explicit authorization
- educational use

Do **not** use this software against systems, accounts, or data without permission. Users are solely responsible for complying with applicable laws and organizational policies.

---

# License

MIT License

---

# Author

HyperCrack v2

Ultimate Password Mutation Engine

Python • Security Research • Password Analysis
