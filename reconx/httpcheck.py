import requests
import time

def check_host(host: str, timeout: float, delay: float):
    headers = {"User-Agent": "BugBounty-Recon-X/1.0"}
    results = []

    for scheme in ("https", "http"):
        url = f"{scheme}://{host}/"
        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
                stream=True,
            )
            results.append({
                "input_url": url,
                "final_url": r.url,
                "status": r.status_code,
                "server": r.headers.get("Server", ""),
                "content_type": r.headers.get("Content-Type", ""),
            })
            r.close()
            break
        except requests.RequestException:
            pass
        finally:
            time.sleep(delay)

    return results[0] if results else None
