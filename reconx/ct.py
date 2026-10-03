import requests
from .utils import in_scope

def discover_subdomains(domain: str, timeout: float = 10.0):
    url = "https://crt.sh/"
    params = {"q": f"%.{domain}", "output": "json"}
    headers = {"User-Agent": "BugBounty-Recon-X/1.0"}
    found = {domain}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        for item in data:
            names = str(item.get("name_value", "")).splitlines()
            for name in names:
                name = name.strip().lower().lstrip("*.")
                if name and in_scope(name, domain):
                    found.add(name)
    except Exception:
        pass

    return sorted(found)
