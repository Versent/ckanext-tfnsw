from .change_org_names import tfnsw_change_org_names


def get_commands():
    return [tfnsw_change_org_names]

def get_helpers():
    from ckanext.theme.helpers import register_helpers
    return register_helpers()