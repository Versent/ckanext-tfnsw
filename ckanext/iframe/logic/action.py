import ckan.plugins.toolkit as tk
import ckanext.iframe.logic.schema as schema


@tk.side_effect_free
def iframe_get_sum(context, data_dict):
    tk.check_access(
        "iframe_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.iframe_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'iframe_get_sum': iframe_get_sum,
    }
