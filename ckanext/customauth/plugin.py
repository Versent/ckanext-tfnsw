import ckan.plugins as plugins
from .apikeys import validate_api_key
from .cookies import validate_cookie

from .auth_functions import user_list, org_or_group_list

import logging

log = logging.getLogger(__name__)


class CustomAuthPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions, inherit=True)

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, "templates")

    def get_actions(self):
        return {
            "validate_cookie": validate_cookie,
            "validate_api_key": validate_api_key,
        }

    def get_auth_functions(self):
        auth_functions = {
            "user_list": user_list,
            "organization_list": org_or_group_list,
            "group_list": org_or_group_list,
        }
        return auth_functions
