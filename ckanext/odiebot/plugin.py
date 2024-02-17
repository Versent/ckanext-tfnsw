import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class OdieBotPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "public")

        self.__class__.token = config.get("odiebot.token", None)

    @classmethod
    def get_odiebot_token(cls):
        return cls.token

    def get_helpers(self):
        return {"get_odiebot_token": self.get_odiebot_token}
