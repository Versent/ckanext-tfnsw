import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .validators import user_password_validator, email_validator


class UserRegPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")

    def get_validators(self):
        return {
            "user_password_validator": user_password_validator,
            "email_validator": email_validator,
        }
