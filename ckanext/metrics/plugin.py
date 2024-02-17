# -*- coding: utf-8 -*-
from __future__ import annotations

from ckan.types import Action, Context, DataDict, Request
import ckan.plugins as p
from ckan.plugins.toolkit import chained_action
import logging
from typing import Any, cast
import ckan.model as model
from ckan.common import g, session, request

log = logging.getLogger(__name__)


class MetricsPlugin(p.SingletonPlugin):
    p.implements(p.ISignal)
    p.implements(p.IResourceController, inherit=True)

    def get_signal_subscriptions(self):
        return {
            p.toolkit.signals.resource_download: [
                on_resource_download,
            ]
        }

    def after_resource_create(self, context, resource):
        try:
            log_resource_action("create", resource["id"])
        except Exception as e:
            log.error(
                f"Error processing after_resource_create {context}, {resource}: {e}"
            )

    def after_resource_update(self, context, resource):
        try:
            log_resource_action("update", resource["id"])
        except Exception as e:
            log.error(
                f"Error processing after_resource_update {context}, {resource}: {e}"
            )


def on_resource_download(sender, **kwargs):
    try:
        log_resource_action("download", sender)
    except Exception as e:
        log.error(f"Error processing resource_download signal {sender}, {kwargs}: {e}")


def get_resource(resource_id):
    query = (
        model.Session.query(model.Resource)
        .join(model.Package)
        .filter(model.Resource.package_id == model.Package.id)
        .filter(model.Resource.id == resource_id)
    )

    resource = next(iter(query.all()), None)
    return resource


def log_resource_action(action, resource_id):
    user = p.toolkit.current_user

    if user:
        username = user.name
        email = user.email
    else:
        username = "anonymous"
        email = "anonymous"

    resource = get_resource(resource_id)
    log.info(
        f"Resource {action} "
        f"ip: {request.remote_addr}, "
        f"username: {username}, "
        f"email: {email}, "
        f"url: {request.url}, "
        f"resource_name: {resource.name}, "
        f"package_name: {resource.package.name}"
    )
