from flask import Blueprint


iframe = Blueprint(
    "iframe", __name__)


def page():
    return "Hello, iframe!"


iframe.add_url_rule(
    "/iframe/page", view_func=page)


def get_blueprints():
    return [iframe]
