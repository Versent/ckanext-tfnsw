import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import requests
import time
import sys
import re
import json
import ckan.plugins as p
from ckan.plugins.toolkit import asbool
from ckan.common import g, request

import logging

log = logging.getLogger(__name__)


class DiscoursePlugin(plugins.SingletonPlugin):
    """
    Insert javascript fragments into package pages and the home page to
    allow users to view and create comments on any package.
    """

    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def configure(self, config):
        """
        Called upon CKAN setup, will pass current configuration dict
        to the plugin to read custom options.
        """
        discourse_url = config.get("discourse.url", None)
        discourse_username = config.get("discourse.username", None)
        discourse_ckan_category = config.get("discourse.ckan_category", None)
        discourse_debug = False  # asbool(config.get('discourse.debug', False))

        if discourse_url is None:
            log.warn(
                "No discourse forum name is set. Please set \
            'discourse.url' in your .ini!"
            )
        else:
            discourse_url = discourse_url.rstrip("/") + "/"

        if discourse_ckan_category is None:
            log.warn(
                "Discourse needs discourse.ckan_category set to work. Please set \
            'discourse.ckan_category' in your .ini!"
            )

        # store these so available to class methods
        self.__class__.discourse_url = discourse_url
        self.__class__.discourse_username = discourse_username
        self.__class__.discourse_ckan_category = discourse_ckan_category

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "discourse")

    @classmethod
    def discourse_comments(cls, canonical_url=""):
        """Adds Discourse comments to the page."""
        c = plugins.toolkit.c

        pkg_dict = c.__getattr__("pkg_dict")
        if not canonical_url:
            embed_url = g.site_url.rstrip("/") + "/dataset/" + pkg_dict["name"]
        else:
            embed_url = canonical_url

        lang_code = request.environ["CKAN_LANG"]

        monolingual_url = re.match("(http://.*?/)(" + lang_code + ")/(.*)$", embed_url)
        if monolingual_url is not None:
            # we strip language code from URL
            embed_url = monolingual_url.group(1) + monolingual_url.group(3)
        else:
            monolingual_url = re.match("(http://.*?/)(..)/(.*)$", embed_url)
            if monolingual_url is not None:
                embed_url = monolingual_url.group(1) + monolingual_url.group(3)

        data = {
            "discourse_embed_url": embed_url,
            "discourse_url": cls.discourse_url,
            "discourse_username": cls.discourse_username,
        }

        comments_snippet = "discourse_comments.html"
        return plugins.toolkit.render_snippet(comments_snippet, data)

    def get_helpers(self):
        return {"discourse_comments": self.discourse_comments}
