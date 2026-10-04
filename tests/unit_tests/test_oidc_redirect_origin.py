from starlette.requests import Request

from mealie.routes.auth import auth


def build_request(origin: str, *, forwarded_proto: str | None = None) -> Request:
    scheme, host = origin.split("://", maxsplit=1)
    headers = [(b"host", host.encode())]
    if forwarded_proto:
        headers.append((b"x-forwarded-proto", forwarded_proto.encode()))

    return Request(
        {
            "type": "http",
            "scheme": "http" if forwarded_proto else scheme,
            "path": "/api/auth/oauth",
            "raw_path": b"/api/auth/oauth",
            "query_string": b"",
            "server": (host, 443 if scheme == "https" else 80),
            "headers": headers,
        }
    )


def configure_redirects(monkeypatch):
    monkeypatch.setattr(auth.settings, "BASE_URL", "https://catsmeal.duckdns.org")
    monkeypatch.setattr(
        auth.settings,
        "OIDC_REDIRECT_ORIGINS",
        (
            "https://catsmeal.duckdns.org",
            "https://dogsmeal.duckdns.org",
            "https://dogsmeal.duckdns.org:8443",
        ),
    )
    monkeypatch.setattr(
        auth.settings,
        "OIDC_REDIRECT_ORIGIN_MAP",
        {
            "https://catsmeal.duckdns.org:8443": "https://catsmeal.duckdns.org",
        },
    )


def test_oidc_callback_preserves_allowlisted_secondary_origin(monkeypatch):
    configure_redirects(monkeypatch)

    result = auth.oidc_redirect_base(build_request("https://dogsmeal.duckdns.org"))

    assert result == "https://dogsmeal.duckdns.org"


def test_oidc_callback_preserves_canonical_origin(monkeypatch):
    configure_redirects(monkeypatch)

    result = auth.oidc_redirect_base(build_request("https://catsmeal.duckdns.org"))

    assert result == "https://catsmeal.duckdns.org"


def test_oidc_callback_honors_forwarded_https_for_allowlisted_origin(monkeypatch):
    configure_redirects(monkeypatch)

    request = build_request("https://dogsmeal.duckdns.org", forwarded_proto="https")

    assert auth.oidc_redirect_base(request) == "https://dogsmeal.duckdns.org"


def test_oidc_callback_rejects_an_untrusted_host_header(monkeypatch):
    configure_redirects(monkeypatch)

    result = auth.oidc_redirect_base(build_request("https://attacker.example"))

    assert result == "https://catsmeal.duckdns.org"


def test_oidc_callback_maps_an_allowlisted_alternate_port(monkeypatch):
    configure_redirects(monkeypatch)

    result = auth.oidc_redirect_base(build_request("https://dogsmeal.duckdns.org:8443"))

    assert result == "https://dogsmeal.duckdns.org:8443"


def test_oidc_callback_does_not_allow_an_unlisted_port(monkeypatch):
    configure_redirects(monkeypatch)

    result = auth.oidc_redirect_base(build_request("https://dogsmeal.duckdns.org:9443"))

    assert result == "https://catsmeal.duckdns.org"
