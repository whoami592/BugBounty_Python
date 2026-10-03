IMPORTANT_HEADERS = {
    "Strict-Transport-Security": "Enforces HTTPS for supported browsers.",
    "Content-Security-Policy": "Restricts allowed content sources.",
    "X-Content-Type-Options": "Helps prevent MIME-sniffing.",
    "X-Frame-Options": "Controls framing / clickjacking exposure.",
    "Referrer-Policy": "Controls referrer information.",
    "Permissions-Policy": "Restricts powerful browser features.",
}

def analyze_security_headers(headers):
    normalized = {k.lower(): v for k, v in headers.items()}
    present, missing = {}, {}

    for name, purpose in IMPORTANT_HEADERS.items():
        key = name.lower()
        if key in normalized:
            present[name] = normalized[key]
        else:
            missing[name] = purpose

    cookies = headers.get("Set-Cookie", "")
    cookie_flags = {
        "secure": "secure" in cookies.lower(),
        "httponly": "httponly" in cookies.lower(),
        "samesite": "samesite=" in cookies.lower(),
    }

    return {
        "present": present,
        "missing": missing,
        "cookie_flags_observed": cookie_flags,
        "note": "Missing headers are observations, not automatically vulnerabilities.",
    }
