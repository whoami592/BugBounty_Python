#!/usr/bin/env python3
import argparse
import sys
from reconx.scanner import ReconScanner
from reconx.banner import print_banner

def parse_args():
    p = argparse.ArgumentParser(
        description="BugBounty Recon X - safe authorized recon toolkit"
    )
    p.add_argument("--target", required=True, help="Root target domain, e.g. example.com")
    p.add_argument(
        "--i-have-permission",
        action="store_true",
        help="Confirm you are authorized to test this target",
    )
    p.add_argument("--max-pages", type=int, default=20, help="Max same-origin pages per host")
    p.add_argument("--delay", type=float, default=0.75, help="Delay between requests in seconds")
    p.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout")
    p.add_argument("--no-ct", action="store_true", help="Disable crt.sh subdomain discovery")
    return p.parse_args()

def main():
    print_banner()
    args = parse_args()

    if not args.i_have_permission:
        print("[!] Refusing to scan without explicit authorization confirmation.")
        print("    Re-run with: --i-have-permission")
        sys.exit(2)

    if args.max_pages < 1 or args.max_pages > 100:
        print("[!] --max-pages must be between 1 and 100")
        sys.exit(2)

    if args.delay < 0.2:
        print("[!] Minimum delay is 0.2 seconds.")
        sys.exit(2)

    scanner = ReconScanner(
        target=args.target,
        timeout=args.timeout,
        delay=args.delay,
        max_pages=args.max_pages,
        use_ct=not args.no_ct,
    )
    report_paths = scanner.run()
    print("\n[+] Finished.")
    for p in report_paths:
        print(f"[+] Report: {p}")

if __name__ == "__main__":
    main()
