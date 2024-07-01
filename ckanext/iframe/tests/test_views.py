"""Tests for views.py."""

import pytest

import ckanext.iframe.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "iframe")
@pytest.mark.usefixtures("with_plugins")
def test_iframe_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("iframe.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, iframe!"
