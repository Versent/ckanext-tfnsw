from ckan import model

import logging
from ckan.logic.auth.get import organization_show as default_organization_show

log = logging.getLogger(__name__)


def user_list(context, data_dict=None):
    user = context["auth_user_obj"]

    # anonymous user
    if not hasattr(user, "id"):
        return {"success": False}

    if hasattr(user, "sysadmin") and user.sysadmin:
        return {"success": True}

    return {"success": user_is_admin(user.id)}


def org_or_group_list(context, data_dict=None):
    user = context["auth_user_obj"]

    # anonymous user
    if not hasattr(user, "id"):
        return {"success": False}

    if hasattr(user, "sysadmin") and user.sysadmin:
        return {"success": True}

    return {"success": user_is_admin(user.id)}


def user_is_member(user_id, group_id):
    q = (
        model.Session.query(model.Group)
        .join(model.Member, model.Group.id == model.Member.group_id)
        .join(model.User, model.User.id == model.Member.table_id)
        .filter(model.Member.table_name == "user")
        .filter(model.Member.state == "active")
        .filter(model.Group.id == group_id)
        .filter(model.Group.state == "active")
        .filter(model.User.id == user_id)
    )

    count = q.count()
    log.debug(f"User {user_id} is a member of group {group_id}: {bool(count)}")
    return bool(count)


def user_is_admin(user_id):
    q = (
        model.Session.query(model.Group)
        .join(model.Member, model.Group.id == model.Member.group_id)
        .join(model.User, model.User.id == model.Member.table_id)
        .filter(model.Member.table_name == "user")
        .filter(model.Member.state == "active")
        .filter(model.Member.capacity == "admin")
        .filter(model.Group.is_organization == True)
        .filter(model.Group.state == "active")
        .filter(model.User.id == user_id)
    )

    count = q.count()
    log.debug(f"User {user_id} is an admin of {count} organizations")
    return bool(count)
