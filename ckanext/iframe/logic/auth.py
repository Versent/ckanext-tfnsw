import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def iframe_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "iframe_get_sum": iframe_get_sum,
    }
