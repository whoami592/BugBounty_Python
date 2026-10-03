import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

JS_ENDPOINT_RE = re.compile(
    r"""(?:"|')((?:/|\./|\.\./)[A-Za-z0-9_?&=./\-{}:$%]+)(?:"|')"""
)

def crawl_same_origin(start_url: str, root_domain: str, max_pages: int, timeout: float, delay: float):
    headers = {"User-Agent": "BugBounty-Recon-X/1.0"}
    q = deque([start_url])
    visited = set()
    pages = []
    js_files = set()
    endpoints = set()

    parsed_start = urlparse(start_url)
    start_host = parsed_start.hostname or ""

    while q and len(visited) < max_pages:
        url = q.popleft()
        url, _ = urldefrag(url)
        if url in visited:
            continue

        parsed = urlparse(url)
        if parsed.hostname != start_host:
            continue
        if parsed.scheme not in ("http", "https"):
            continue

        visited.add(url)

        try:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            ctype = r.headers.get("Content-Type", "")
            pages.append({
                "url": r.url,
                "status": r.status_code,
                "content_type": ctype,
                "title": None,
            })

            if "text/html" in ctype:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.string.strip() if soup.title and soup.title.string else None
                pages[-1]["title"] = title

                for tag in soup.find_all("a", href=True):
                    nxt = urljoin(r.url, tag["href"])
                    nxt_parsed = urlparse(nxt)
                    if nxt_parsed.hostname == start_host:
                        q.append(nxt)

                for tag in soup.find_all("script", src=True):
                    src = urljoin(r.url, tag["src"])
                    if urlparse(src).hostname == start_host:
                        js_files.add(src)

            time.sleep(delay)
        except requests.RequestException:
            time.sleep(delay)

    for js in list(js_files)[:20]:
        try:
            r = requests.get(js, headers=headers, timeout=timeout)
            if len(r.content) <= 2_000_000:
                for match in JS_ENDPOINT_RE.findall(r.text):
                    endpoints.add(match)
        except requests.RequestException:
            pass
        finally:
            time.sleep(delay)

    return {
        "pages": pages,
        "javascript_files": sorted(js_files),
        "javascript_endpoint_candidates": sorted(endpoints)[:200],
    }
