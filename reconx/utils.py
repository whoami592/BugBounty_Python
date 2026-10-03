import re
from urllib.parse import urlparse

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)

def normalize_domain(value: str) -> str:
    value = value.strip().lower()
    if "://" in value:
        value = urlparse(value).hostname or ""
    value = value.strip(".")
    if not DOMAIN_RE.match(value):
        raise ValueError("Invalid domain format")
    return value

def in_scope(hostname: str, root_domain: str) -> bool:
    hostname = (hostname or "").lower().strip(".")
    root_domain = root_domain.lower().strip(".")
    return hostname == root_domain or hostname.endswith("." + root_domain)

def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
