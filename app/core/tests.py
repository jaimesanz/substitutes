"""Serving the app under a URL path prefix (e.g. https://jaimesa.nz/substitutes/)."""

import re
from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import set_script_prefix

PREFIX = "/substitutes"
URL_ATTR = re.compile(r'\b(?:href|src|action)="([^"]*)"')
PUBLIC_PAGES = ["/", "/cuenta/registro/", "/cuenta/registro/profe/", "/cuenta/registro/colegio/"]
# The manifest storage needs collectstatic; plain storage builds the same URLs.
PLAIN_STATIC = {
    **settings.STORAGES,
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


def same_site_paths(html):
    """Every root-relative URL in href/src/action attributes (not //host, anchors or queries)."""
    return [u for u in URL_ATTR.findall(html) if u.startswith("/") and not u.startswith("//")]


@override_settings(
    FORCE_SCRIPT_NAME=PREFIX,
    STATIC_URL=PREFIX + "/static/",
    MEDIA_URL=PREFIX + "/media/",
    SESSION_COOKIE_PATH=PREFIX + "/",
    CSRF_COOKIE_PATH=PREFIX + "/",
    STORAGES=PLAIN_STATIC,
)
class PathPrefixTests(TestCase):
    """The settings config/settings.py derives from DJANGO_SCRIPT_NAME=/substitutes."""

    def setUp(self):
        # Django's WSGI handler sets the URL prefix on every request; the test client doesn't.
        set_script_prefix(PREFIX + "/")
        self.addCleanup(set_script_prefix, "/")

    def test_links_and_assets_stay_under_the_prefix(self):
        for url in PUBLIC_PAGES + ["/cuenta/ingresar/"]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, url)
            outside = [
                u for u in same_site_paths(resp.content.decode()) if not u.startswith(PREFIX + "/")
            ]
            self.assertFalse(outside, (url, outside))

    def test_login_redirect_and_missing_slash_stay_under_the_prefix(self):
        resp = self.client.get("/profe/")
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].startswith(f"{PREFIX}/cuenta/ingresar/"), resp["Location"])
        resp = self.client.get("/cuenta/registro")
        self.assertEqual(resp["Location"], f"{PREFIX}/cuenta/registro/")

    def test_cookies_are_scoped_to_the_prefix(self):
        resp = self.client.get("/cuenta/ingresar/")
        self.assertEqual(resp.cookies["csrftoken"]["path"], PREFIX + "/")


@override_settings(STORAGES=PLAIN_STATIC)
class NoPrefixTests(TestCase):
    def test_urls_are_unchanged_without_a_prefix(self):
        for url in PUBLIC_PAGES:
            html = self.client.get(url).content.decode()
            self.assertFalse([u for u in same_site_paths(html) if u.startswith(PREFIX)], url)
        self.assertIn('href="/cuenta/registro/"', self.client.get("/").content.decode())


class NoLiteralRootLinksTests(TestCase):
    """Literal root links skip Django's URL tools and so ignore the prefix: use {% url %}."""

    def test_templates_have_no_literal_root_links(self):
        literal = re.compile(r"""(?:href|src|action)=["']/(?!/)""")
        app_dir = Path(settings.BASE_DIR)
        found = [
            f"{path.relative_to(app_dir)}:{n}"
            for path in app_dir.rglob("templates/**/*.html")
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if literal.search(line)
        ]
        self.assertFalse(found, found)
