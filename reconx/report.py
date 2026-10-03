import json
from pathlib import Path
from datetime import datetime, timezone
from html import escape

def write_reports(target: str, data: dict):
    out = Path("reports")
    out.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    base = out / f"{target}_{stamp}"

    json_path = base.with_suffix(".json")
    html_path = base.with_suffix(".html")

    json_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    rows = []
    for host in data.get("hosts", []):
        live = host.get("http", {}) or {}
        missing = ", ".join((host.get("security_headers", {}) or {}).get("missing", {}).keys())
        rows.append(
            "<tr>"
            f"<td>{escape(host.get('host',''))}</td>"
            f"<td>{escape(str(live.get('status','')))}</td>"
            f"<td>{escape(live.get('final_url',''))}</td>"
            f"<td>{escape(missing)}</td>"
            "</tr>"
        )

    html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>BugBounty Recon X - {escape(target)}</title>
<style>
body{{font-family:Arial,sans-serif;margin:40px;line-height:1.5}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top}}
th{{background:#eee}}
code,pre{{background:#f6f6f6;padding:2px 4px}}
.small{{color:#666}}
</style>
</head>
<body>
<h1>BugBounty Recon X</h1>
<p><b>Target:</b> {escape(target)}</p>
<p><b>Coded by Cyber Security Engineer Mr Sabaz Ali Khan</b></p>
<p class="small">Authorized security testing only. Observations require manual validation.</p>
<h2>Host Summary</h2>
<table>
<tr><th>Host</th><th>Status</th><th>Final URL</th><th>Missing Security Headers</th></tr>
{''.join(rows)}
</table>
<h2>Full JSON</h2>
<pre>{escape(json.dumps(data, indent=2, default=str))}</pre>
</body>
</html>"""
    html_path.write_text(html, encoding="utf-8")
    return [str(json_path), str(html_path)]
