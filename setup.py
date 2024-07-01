# -*- coding: utf-8 -*-
from os.path import dirname, realpath, exists
from setuptools import setup, find_packages

import sys

name = 'ckanext-tfnsw'
sys.path.insert(0, realpath(dirname(__file__))+"/" + "/".join(name.split("-")))


setup(
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_dir={name: name},
    namespace_packages=['ckanext'],
    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
    install_requires=[
        "Babel>=2.8.0",
    ],

    entry_points='''
    [ckan.plugins]
    tfnsw_theme=ckanext.theme.plugin:ThemePlugin
    tfnsw_customauth=ckanext.customauth.plugin:CustomAuthPlugin
    tfnsw_discourse=ckanext.discourse.plugin:DiscoursePlugin
    tfnsw_openapiview=ckanext.openapiview.plugin:OpenApiViewPlugin
    tfnsw_s3view=ckanext.s3view.plugin:S3ViewPlugin
    tfnsw_subscriptions=ckanext.subscriptions.plugin:SubscriptionsPlugin
    tfnsw_metrics=ckanext.metrics.plugin:MetricsPlugin
    tfnsw_odiebot=ckanext.odiebot.plugin:OdieBotPlugin
    tfnsw_userreg=ckanext.userreg.plugin:UserRegPlugin
    tfnsw_iframe=ckanext.iframe.plugin:IframePlugin
    '''
)
