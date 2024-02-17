# tfnsw_customauth plugin

This plugin provides custom user authentication/authorization to CA Gateway and Drupal by adding new actions:

- `validate_api_token`
- `validate_cookie`

## `validate_api_token`

This action has the following signature:

```
POST /api/3/action/validate_api_key
Authorization: <admin_token>
{
    "api_key": "<api_key>",
    "api_id": "<api_id>"
}
```

where,

- `<admin_token>`: This is an Admin token to authenticate against the CKAN API
- `<api_key>`: This is the API key used by CA Gateway clients. It can be a CKAN API token or a key imported from legacy DKAN system
- `<api_id>`: This is the API identifier e.g. `car-park-api`, `traffic-hazards-api`

The response of the action is a [standard CKAN API response](https://docs.ckan.org/en/2.9/api/) with the `result` field containing the authorization status and `usage_plan` available to the user. E.g.

```
    ...
    "result": {
        "authorized": true,
        "message": "Authorized",
        "usage_plan": {
            "plan": "silver",
            "rate": 10,
            "quota": 300000
        }
    }
```

If user is not authorized, no `usage_plan` will be returned. E.g.

```
    "result": {
        "authorized": false,
        "message": "Invalid token"
    }
```



### Configuration

1. This extension is expected to be used by CA Gateway by invoking CKAN REST API. This requires a API Token generated for an Admin account (see `<admin_token>` above)

2. Legacy API keys from DKAN needs to be imported to CKAN database. Example insert statement:

```
INSERT INTO public.api_token
   (id, "name", user_id, created_at, last_access, plugin_extras)
VALUES
   (<token>, <token_name>, <user_id>, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '{}');
```

where,

- `<token>`: This is the legacy API key
- `<token_name>`: This is a name given to a key. It's recommended to add `legacy:` prefix for imported keys
- `<user_id>`: This is the user ID (Primary Key of `public.User` table) of the user this key belongs to

3. To map an API in CA Gateway to CKAN, a corresponding Dataset needs to be created in CKAN. The Dataset name is expected to be the same as `api_id`. If this needs to be configurable, a lookup mechanism needs to be implemented.

4. User's permission to access an API is determined by following rules

- User should have permissions to view the corresponding API Dataset in CKAN. CKAN's existing permission controls (e.g. Organization membership) are used for this.
- If the API Dataset is not `private`, user is authorized to access the API and a usage plan is assigned as described below
- If the API Dataset is `private`, the API Dataset and user have to be in the same Group to be authorized. If they are, a usage plan is assigned. It is possible to create a Group per API or multiple APIs based on the level of permission segregation needed.

Example: Consider there are 3 APIs which are mapped to 3 API Datasets, `A`, `B`, and `C` and we need to grant access to all users to `A` and `B` but `C` needs to be restricted to Beta testers. In this case, 2 Groups will be created "External Users" and "Beta Testers". `A` and `B` will be added to "External Users" Group and `C` will be added to "Beta Testers" Group. Beta testers will be in both Groups but other users will be only in the "External Users" group.

5. Usage plans are assigned to users based on a user's membership in particular Groups. These Groups **must** exist for this plugin to work. The Group names are configured using the configuration item `ckan.apikeys.api_usage_plan_groups` which defaults to:

```
   [
       "api-bronze-users",
       "api-silver-users"
       "api-gold-users"
       "api-platinum-users"
   ]
```

If different groups are created, this configuration item **must** be set accordingly. These Groups need to have the following metadata attached:

| Key                       | Value                                                                    |
| ------------------------- |--------------------------------------------------------------------------|
| `api-usage-plan-name`     | Plan name e.g. `bronze`, `silver`                                        |
| `api-usage-plan-quota`    | Quota (number) e.g. 10000                                                |
| `api-usage-plan-rate`     | Rate (number) e.g. 10                                                    |
| `api-usage-plan-priority` | A priority order e.g. bronze has the highest priority and is the default |


- It is expected that CA Gateway performs some form of caching of authorization requests. If this is not the case and it invokes the `validate_api_key` action for each API call, further optimization (e.g. adding caching) may be needed in the plugin.

## `validate_api_token`

This action has the following signature:


```
GET /api/3/action/validate_cookie
Cookie: ckan=<ckan_cookie>
```

where, `<ckan_cookie>` is a CKAN session cookie. 

The response of the action is a [standard CKAN API response](https://docs.ckan.org/en/2.9/api/) with the `result` field containing logged in status and user profile if logged in E.g.

```
    ...
    "result": {
        "logged_in": true,
        "user": {
            "id": "...",
            "name": "...",
            "fullname": "...",
            "last_active: "<timestamp>",
            "href": "<user_link>"
        }
    }
```

If user is not logged in, no `user` will be returned. E.g.

```
    "result": {
        "logged_in": false
    }
```
