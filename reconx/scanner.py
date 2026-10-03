import time
import requests
from urllib.parse import urlparse

from .utils import normalize_domain, in_scope
from .ct import discover_subdomains
from .httpcheck import check_host
from .headers import analyze_security_headers
from .tlsinfo import inspect_tls
from .crawler import crawl_same_origin
from .report import write_reports

class ReconScanner:
    def __init__(self, target, timeout=8.0, delay=0.75, max_pages=20, use_ct=True):
        self.target = normalize_domain(target)
        self.timeout = timeout
        self.delay = delay
        self.max_pages = max_pages
        self.use_ct = use_ct
        self.ua = {"User-Agent": "BugBounty-Recon-X/1.0"}

    def run(self):
        print(f"[+] Authorized target: {self.target}")

        if self.use_ct:
            print("[*] Discovering in-scope subdomains from Certificate Transparency...")
            hosts = discover_subdomains(self.target, timeout=min(self.timeout + 2, 15))
        else:
            hosts = [self.target]

        # Keep the tool conservative by capping auto-discovered hosts.
        hosts = [h for h in hosts if in_scope(h, self.target)][:50]
        print(f"[+] In-scope hosts queued: {len(hosts)}")

        report = {
            "tool": "BugBounty Recon X",
            "author": "Cyber Security Engineer Mr Sabaz Ali Khan",
            "target": self.target,
            "hosts": [],
        }

        for idx, host in enumerate(hosts, 1):
            print(f"[*] ({idx}/{len(hosts)}) Checking {host}")
            live = check_host(host, self.timeout, self.delay)
            host_data = {"host": host, "http": live}

            if live:
                try:
                    r = requests.get(
                        live["final_url"],
                        headers=self.ua,
                        timeout=self.timeout,
                        allow_redirects=True,
                    )
                    final_host = urlparse(r.url).hostname or ""
                    if in_scope(final_host, self.target):
                        host_data["security_headers"] = analyze_security_headers(r.headers)
                    else:
                        host_data["security_headers"] = {
                            "note": "Skipped after redirect outside authorized root scope."
                        }
                    r.close()
                except requests.RequestException as e:
                    host_data["security_headers"] = {"error": str(e)}

                if live["final_url"].startswith("https://"):
                    host_data["tls"] = inspect_tls(host, self.timeout)

                final_host = urlparse(live["final_url"]).hostname or ""
                if final_host == host and in_scope(final_host, self.target):
                    host_data["crawl"] = crawl_same_origin(
                        live["final_url"],
                        self.target,
                        self.max_pages,
                        self.timeout,
                        self.delay,
                    )
                else:
                    host_data["crawl"] = {"note": "Skipped cross-host redirect."}

            report["hosts"].append(host_data)
            time.sleep(self.delay)

        return write_reports(self.target, report)
