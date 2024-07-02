import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from .cli import get_commands

class ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IClick)

    def get_commands(self):
        return get_commands()

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "theme")

    def get_helpers(self):
        from ckanext.theme.helpers import register_helpers
        return register_helpers()