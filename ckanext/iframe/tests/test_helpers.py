"""Tests for helpers.py."""

import ckanext.iframe.helpers as helpers


def test_iframe_hello():
    assert helpers.iframe_hello() == "Hello, iframe!"
