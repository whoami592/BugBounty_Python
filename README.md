# BugBounty Recon X

Safe reconnaissance toolkit for **authorized bug bounty scopes only**.

**Coded by Cyber Security Engineer Mr Sabaz Ali Khan**

## Features
- Permission gate before scanning
- Scope enforcement for the target domain
- Subdomain discovery from Certificate Transparency (`crt.sh`)
- Live HTTP/HTTPS host checking
- Security-header inspection
- TLS certificate inspection
- Same-origin URL crawling
- Basic JavaScript endpoint extraction
- JSON + HTML reports
- Conservative delays and request limits

## Not included
This project intentionally does **not** include exploitation, password attacks,
credential stuffing, destructive testing, mass scanning, persistence, malware,
or authentication bypass modules.

## Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Basic scan:

```bash
python main.py --target example.com --i-have-permission
```

Limit crawl depth and pages:

```bash
python main.py --target example.com --i-have-permission --max-pages 25 --delay 0.8
```

Skip Certificate Transparency lookup:

```bash
python main.py --target example.com --i-have-permission --no-ct
```

Reports are written to the `reports/` directory.

## Important
Only scan assets that are explicitly in scope for the bug bounty program or
systems you own/have written permission to test.
