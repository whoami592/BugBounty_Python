import socket
import ssl
from datetime import datetime, timezone

def inspect_tls(host: str, timeout: float = 6.0):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                not_after = cert.get("notAfter")
                expiry = None
                days_left = None
                if not_after:
                    expiry_dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                    expiry = expiry_dt.isoformat()
                    days_left = (expiry_dt - datetime.now(timezone.utc)).days

                return {
                    "protocol": ssock.version(),
                    "cipher": cipher[0] if cipher else None,
                    "expiry": expiry,
                    "days_until_expiry": days_left,
                    "subject": cert.get("subject"),
                    "issuer": cert.get("issuer"),
                }
    except Exception as e:
        return {"error": str(e)}
