import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import re


log = __import__("logging").getLogger(__name__)


def parse_url(url):
    """
    Parse s3 url and return region, bucket and prefix
    """

    if url is None:
        return None

    # url is supposed to be to a s3 directory and end with /
    if not url.endswith("/"):
        url += "/"

    url_pattern_path_style = (
        r"https://s3\.([a-zA-Z0-9\-_]+)\.amazonaws\.com/([a-zA-Z0-9\-_\.]+)/(.*)"
    )
    m = re.match(url_pattern_path_style, url)

    if m:
        return [m[1], m[2], m[3]]

    url_pattern_host_style = (
        r"https://([a-zA-Z0-9\-_]+)\.s3\.([a-zA-Z0-9\-_]+)\.amazonaws\.com/(.*)"
    )
    m = re.match(url_pattern_host_style, url)
    if m:
        return [m[2], m[1], m[3]]

    return None


class S3ViewPlugin(plugins.SingletonPlugin):
    view_type = "s3_view"

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True)

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")

    def info(self):
        return {
            "name": self.view_type,
            "title": "File Browser",
            "icon": "file",
            "default_title": toolkit._("File Browser"),
        }

    def can_view(self, data_dict):
        resource = data_dict["resource"]
        url = resource.get("url")
        format_lower = resource.get("format", "").lower()

        if format_lower == "s3" and parse_url(url):
            return True

        return False

    def view_template(self, context, data_dict):
        return "resource_view.html"

    def setup_template_variables(self, context, data_dict):
        resource = data_dict["resource"]
        url = resource.get("url")

        # view available only if url is valid
        [region, bucket, prefix] = parse_url(url)

        data = {
            "s3view_region": region,
            "s3view_bucket": bucket,
            "s3view_prefix": prefix,
        }
        return {**data_dict, **data}

    # IResourceController

    def after_resource_update(self, context, resource):
        self.add_default_views(context, resource)

    def after_resource_create(self, context, resource):
        self.add_default_views(context, resource)

    def has_view_already(self, context, resource):
        if "id" in resource:
            params = {"id": resource["id"]}
            resource_views = toolkit.get_action("resource_view_list")(context, params)
            for resource_view in resource_views:
                if (
                    "view_type" in resource_view
                    and resource_view["view_type"] == self.view_type
                ):
                    return True

        return False

    def add_default_views(self, context, resource):
        if (
            "id" in resource
            and self.can_view({"resource": resource})
            and not self.has_view_already(context, resource)
        ):
            view = {
                "title": "File Browser",
                "description": "",
                "resource_id": resource["id"],
                "view_type": self.view_type,
            }
            toolkit.get_action("resource_view_create")(context, view)
