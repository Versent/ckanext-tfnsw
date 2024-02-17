import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic import get_action, get_or_bust
from ckan.model import core, user
import ckan.lib.api_token as api_token

import ckan.model as model
from ckan.common import config

import logging

log = logging.getLogger(__name__)


def lookup_dataset(api_id):
    """
    Lookup dataset based on API identifier
    """

    # For now, it is assumed that datasets are given the same name as api_id
    # If this changes, implement the following so that dataset id is looked up based on some mapping

    dataset = model.Package.get(api_id)
    return dataset


def decode_api_key(api_key):
    """
    Decode the api_key and extract the token_id.
    A legacy api_key is not encoded in a JWT and is basically the token_id
    In this case, is_legacy flag is set
    """

    token_id = None
    decoded = None
    is_legacy = False

    if len(api_key.split('.')) == 3:
        decoded = api_token.decode(api_key)

    # This is a legacy token
    if decoded == None:
        token_id = api_key
        is_legacy = True
    else:
        token_id = decoded.get("jti")

    return token_id, is_legacy


def get_dataset_groups(dataset_id):
    query = (
        model.Session.query(model.Group)
        .join(model.Member)
        .filter(model.Member.table_name == "package")
        .filter(model.Member.table_id == dataset_id)
        .filter(model.Member.state == "active")
        .filter(model.Group.state == "active")
    )

    groups = [{"id": g.id, "name": g.name} for g in query.all()]

    # unique groups
    return list({g["id"]: g for g in groups}.values())


def get_user_groups(user_id):
    # need to include both groups and orgs so not filtering on Group.type
    query = (
        model.Session.query(model.Group)
        .join(model.Member)
        .filter(model.Member.table_name == "user")
        .filter(model.Member.table_id == user_id)
        .filter(model.Member.state == "active")
        .filter(model.Group.state == "active")
    )

    groups = [{"id": g.id, "name": g.name} for g in query.all()]

    # unique groups
    return list({g["id"]: g for g in groups}.values())


def get_usage_plans():
    """
    Get usage plans defined in the system
    A group per usage plan is created and plan details (quota, rate) are defined as metadata
    """

    # This config MUST have valid groups
    usage_plan_groups = config.get(
        f"ckan.apikeys.api_usage_plan_groups",
        [
            "api-internal-users",
            "api-platinum-users",
            "api-gold-users",
            "api-silver-users",
            "api-bronze-users",
        ],
    )

    admin_context = {"user": "ckan_admin"}
    params = {
        "include_extras": True,
        "include_datasets": False,
        "include_dataset_count": False,
        "include_users": False,
        "include_groups": False,
        "include_tags": False,
        "include_followers": False,
    }

    usage_plans = {}
    i = 1
    for g in usage_plan_groups:
        group = get_action("group_show")(admin_context, {"id": g, **params})
        extras = {kv["key"]: kv["value"] for kv in group["extras"]}
        try:
            plan = {
                "name": extras.get("api-usage-plan-name", g),
                "rate": int(extras.get("api-usage-plan-rate", 10)),
                "quota": int(extras.get("api-usage-plan-quota", 10000)),
                "priority": int(extras.get("api-usage-plan-priority", i)),
            }
        # Catch if a plan has some bad input and give it the default values
        except ValueError:
            log.error(u"Unexpected values for plan: %s. Assigning it default values", g)
            plan = {
                "name": g,
                "rate": 10,
                "quota": 10000,
                "priority": i
            }

        i += 1
        usage_plans[group["name"]] = plan

    return usage_plans


def get_usage_plan(dataset, user):
    user_groups = get_user_groups(user.id)
    log.debug(f"User is in groups: {user_groups}")

    # If this is a private Dataset, user and dataset has to belong to the same group
    if dataset.private:
        dataset_groups = get_dataset_groups(dataset.id)
        log.debug(f"Dataset is in groups: {dataset_groups}")
        user_group_ids = set([g["id"] for g in user_groups])
        dataset_group_ids = set([g["id"] for g in dataset_groups])

        # Check both user and dataset are in the same group(s)
        if len(user_group_ids.intersection(dataset_group_ids)) == 0:
            return None

    usage_plans = get_usage_plans()

    selected_plan = max(usage_plans.values(), key=lambda x: x["priority"])

    # If user is in multiple groups pick the best one
    for ug in user_groups:
        plan = usage_plans.get(ug["name"])
        if not plan:
            continue

        if plan["priority"] < selected_plan["priority"]:
            selected_plan = plan

    return selected_plan


def response(authorized, message, data=None):
    resp = {"authorized": authorized, "message": message}

    if data:
        resp = {**resp, **data}

    log.debug(f"Sending response: {resp}")
    return resp


def validate_api_key(context, data_dict):
    """
    Validate api_key and api_id against users permissions.
    Return usage_plan if validated
    """

    # Only sysadmin allowed to invoke this action
    # Throwing NotAuthorized is fine here as we are validating the caller
    user_obj = context["auth_user_obj"]
    if not hasattr(user_obj, "sysadmin") or not user_obj.sysadmin:
        raise toolkit.NotAuthorized("Only sysadmin allowed")

    api_id = get_or_bust(data_dict, "api_id")
    api_key = get_or_bust(data_dict, "api_key")

    token_id, is_legacy = decode_api_key(api_key)

    token = model.ApiToken.get(token_id)
    if token is None:
        return response(False, "Invalid token")

    dataset = lookup_dataset(api_id)
    if dataset is None:
        return response(False, "Invalid api_id")

    user_id = token.user_id
    user = model.User.get(user_id)
    name = token.name

    log.debug(
        f"Validating api key for user: {user_id}, api_id: {api_id}, dataset_id: {dataset.id}"
    )

    # Check if user can view the API dataset
    try:
        toolkit.check_access("package_show", {"user": user.name}, {"id": dataset.id})
    except toolkit.NotAuthorized:
        return response(False, f"User {user.name} not allowed to access {dataset.id}")

    usage_plan = get_usage_plan(dataset, user)
    if usage_plan is None:
        return response(False, "No usage plan available")

    return response(True, "Authorized", {"usage_plan": usage_plan, "app_name": name})
