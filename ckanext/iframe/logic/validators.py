import ckan.plugins.toolkit as tk


def iframe_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "iframe_required": iframe_required,
    }
