# ckanext/iframe/plugin.py
import ckan.plugins as p
from ckan.plugins import toolkit as tk

class IframePlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        tk.add_template_directory(config, 'templates')

    def get_helpers(self):
        from ckanext.iframe.helpers import register_helpers
        return register_helpers()
