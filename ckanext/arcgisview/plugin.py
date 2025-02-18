# encoding: utf-8
from __future__ import annotations

from ckan.types import Context
from typing import Any
from ckan.common import CKANConfig
import logging

import ckan.plugins as p

log = logging.getLogger(__name__)
ignore_empty = p.toolkit.get_validator('ignore_empty')
unicode_safe = p.toolkit.get_validator('unicode_safe')


class ArcgisView(p.SingletonPlugin):
    '''This plugin makes views of web pages, using an <iframe> tag'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config: CKANConfig):
        p.toolkit.add_template_directory(config, 'templates')

    def info(self) -> dict[str, Any]:
        return {'name': 'arcgis_view',
                'title': p.toolkit._('ArcGIS Authenticated'),
                'schema': {'page_url': [ignore_empty, unicode_safe]},
                'iframed': False,
                'icon': 'link',
                'always_available': True,
                'default_title': p.toolkit._('ArcGIS Authenticated'),
                }

    def can_view(self, data_dict: dict[str, Any]):

        resource = data_dict['resource']
        return (resource.get('format', '').lower() in ['html', 'htm'] or
                resource['url'].split('.')[-1] in ['html', 'htm'])

    def view_template(self, context: Context, data_dict: dict[str, Any]):
        return 'arcgis_view.html'

    def form_template(self, context: Context, data_dict: dict[str, Any]):
        return 'arcgis_form.html'
    
    def get_helpers(self):
        from ckanext.arcgisview.helpers import register_helpers
        return register_helpers()