import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import re

log = logging.getLogger('s3browse')
log.setLevel(logging.DEBUG)

def parse_url(url):
    """
    Parse URL and return Cloudfront FQDN and Prefix.  Example:
      https://d392man4o595lv.cloudfront.net/ROAM
      https://opendata-tpa.np.tfnsw.com.au/ROAM
    """

    if url is None:
        return None

        # r"https://([a-z0-9]+\.cloudfront\.net)/(.*)"
    url_pattern = (
        r"https://([^/]+)/(.*)"
    )
    m = re.match(url_pattern, url)

    if m:
        return [m[1], m[2]]

    return None


class S3BrowsePlugin(plugins.SingletonPlugin):

    view_type = 's3browse'

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True)

    def update_config(self, config):
        log.info("S3BrowsePlugin has been loaded and is being configured!")
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")

    def info(self):
        log.info("S3BrowsePlugin: info() method is being called")
        return {
            "name": self.view_type,
            "title": "S3 File Browser",
            "icon": "file",
            "default_title": toolkit._("File Browser"),
        }

    def can_view(self, data_dict):
        log.info(data_dict)
        resource = data_dict['resource']
        format = resource.get('format', '').lower()
        log.info(f"S3BrowsePlugin: Checking if we can view format: {format}")
        return format == 's3'

    def view_template(self, context, data_dict):
        log.info("S3BrowsePlugin: Rendering the view template")
        return 'resource_view.html'

    def setup_template_variables(self, context, data_dict):
        # Set up the variables to be passed to your template
        resource = data_dict['resource']
        url = resource.get("url")

        [cloudfront_fqdn, prefix] = parse_url(url)

        log.info(f"S3BrowsePlugin: url={url}")
        log.info(f"S3BrowsePlugin: cloudfront_fqdn={cloudfront_fqdn}")
        log.info(f"S3BrowsePlugin: prefix={prefix}")

        data = {
            "cloudfront_fqdn": cloudfront_fqdn,
            "prefix": prefix,
        }
        return {**data_dict, **data}
