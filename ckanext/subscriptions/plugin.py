import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import ungettext, ugettext, config
from ckanext.activity.email_notifications import (
    get_notifications,
    send_notification,
    string_to_timedelta,
)
import ckan.model as model
import ckan.lib.api_token as api_token
from ckan.lib.dictization import model_dictize
from typing import Any, cast
import datetime

import ckan.model as model
from ckan.logic import get_action
from ckan.types import Context
import logging

log = logging.getLogger(__name__)


def get_notifications_for_user(user):
    # Parse the email_notifications_since config setting, email notifications
    # from longer ago than this time will not be sent.
    email_notifications_since = config.get("ckan.email_notifications_since")
    email_notifications_since = string_to_timedelta(email_notifications_since)
    email_notifications_since = datetime.datetime.utcnow() - email_notifications_since

    user_id = user["id"]
    dash = model.Dashboard.get(user_id)
    email_last_sent = dash.email_last_sent
    activity_stream_last_viewed = dash.activity_stream_last_viewed
    since = max(email_notifications_since, email_last_sent, activity_stream_last_viewed)

    notifications = get_notifications(user, since)
    log.info(f"User: {user_id} notifications: {len(notifications)} since: {since}")

    return notifications


def send_notifications_for_user(user, notifications):
    for notification in notifications:
        send_notification(user, notification)

    dash = model.Dashboard.get(user["id"])
    dash.email_last_sent = datetime.datetime.utcnow()
    model.repo.commit()


def get_and_send_notifications_for_users(users):
    context = cast(
        Context,
        {
            "model": model,
            "session": model.Session,
            "ignore_auth": True,
            "keep_email": True,
        },
    )

    for user in users:
        try:
            user_dict = model_dictize.user_dictize(user, context)
            notifications = get_notifications_for_user(user_dict)

            if len(notifications) > 0:
                send_notifications_for_user(user_dict, notifications)

        except Exception as e:
            log.error(f"Error sending notifcation to user: {user.id} {e}")


def get_and_send_notifications_for_all_users():
    query = model.Session.query(model.User).filter(model.User.state == "active")

    users = query.all()
    batch_size = 100

    log.info(f"Sending notifications to {len(users)} users. Batch size = {batch_size}")

    for i in range(0, len(users), batch_size):
        users_batch = users[i : i + batch_size]
        log.info(f"Enqueuing notification job {i}")
        toolkit.enqueue_job(get_and_send_notifications_for_users, [users_batch])


# run this in 2 steps
# 1. create job that fetches all users
# 2. job 1 creates batches of users and creates jobs for each batch
def enqueue_email_notifications(context, data_dict):
    user_obj = context["auth_user_obj"]
    if not hasattr(user_obj, "sysadmin") or not user_obj.sysadmin:
        raise toolkit.NotAuthorized("Only sysadmin allowed")

    toolkit.enqueue_job(get_and_send_notifications_for_all_users)

    return "OK"


class SubscriptionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)

    # IActions
    def get_actions(self):
        return {"enqueue_email_notifications": enqueue_email_notifications}
