"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.iframe.logic import validators


def test_iframe_reauired_with_valid_value():
    assert validators.iframe_required("value") == "value"


def test_iframe_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.iframe_required(None)
