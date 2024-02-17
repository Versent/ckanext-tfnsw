# ckanext-tfnsw

This CKAN extension provides following plugins

- [`tfnsw_customauth`](ckanext/customauth/README.md)
- `tfnsw_discourse`
- `tfnsw_metrics`
- `tfnsw_odiebot`
- `tfnsw_openapiview`
- `tfnsw_s3view`
- `tfnsw_subscriptions`
- `tfnsw_theme`
- `tfnsw_userreg`

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible? |
| --------------- | ----------- |
| 2.8 and earlier | not tested  |
| 2.9             | Yes         |

This extension does not require Python packages other than those already available to extensions from CKAN core.

## Installation

Add following to the plugins list in `ckan.ini`:

```
## Plugins Settings
ckan.plugins = envvars image_view ... tfnsw_customauth tfnsw_discourse ...
```
