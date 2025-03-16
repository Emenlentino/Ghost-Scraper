# tests/test_compliance.py
import pytest
from myproject.compliance import is_allowed

def test_is_allowed_known_site(monkeypatch):
    # Fake a robots parser that allows fetching.
    class FakeRobotFileParser:
        def set_url(self, url):
            pass
        def read(self):
            pass
        def can_fetch(self, user_agent, url):
            return True
    monkeypatch.setattr("urllib.robotparser.RobotFileParser", lambda: FakeRobotFileParser())
    assert is_allowed("https://example.com/some_page") is True

def test_is_disallowed(monkeypatch):
    # Fake a robots parser that disallows fetching.
    class FakeRobotFileParser:
        def set_url(self, url):
            pass
        def read(self):
            pass
        def can_fetch(self, user_agent, url):
            return False
    monkeypatch.setattr("urllib.robotparser.RobotFileParser", lambda: FakeRobotFileParser())
    assert is_allowed("https://example.com/some_page") is False
