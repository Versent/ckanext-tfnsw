import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic import get_action, get_or_bust, side_effect_free
from ckan.model import user
import ckan.model as model
from ckan.common import config, session, request

import logging

log = logging.getLogger(__name__)


def response(logged_in, data=None):
    resp = {"logged_in": logged_in}

    if data:
        resp = {**resp, **data}

    log.debug(f"Sending response: {resp}")
    return resp


@side_effect_free
def validate_cookie(context, data_dict):
    """
    Validate cookie and return user profile
    """

    if not session:
        log.info("No session cookie")
        return response(False)

    user_id = session.get("_user_id")

    if not user_id:
        log.info("No user in session cookie (not logged in)")
        return response(False)

    user_obj = model.User.get(user_id)

    user = {
        "id": user_id,
        "name": user_obj.name,
        "fullname": user_obj.fullname,
        "last_active": session["last_active"],
        "href": f"/user/{user_obj.name}",
    }

    return response(True, {"user": user})