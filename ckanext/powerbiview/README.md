# TFNSW PowerBI View Extension for CKAN

The `tfnsw_powerbiview` extension was created to securely embed PowerBI reports in CKAN. Since these reports are private and require authentication, the extension leverages the PowerBI API to authenticate and embed them seamlessly within CKAN, following Microsoft’s service principal authentication model.

## Overview

The `tfnsw_powerbiview` extension uses PowerBI’s API to authenticate with a service principal and embed private PowerBI reports in CKAN, ensuring they are viewable by users without prompting for credentials.

### Configuration Requirements

The extension requires the following configuration values in `ckan.ini`:

- `ckanext.powerbi.client_id`: PowerBI Client ID for the service principal
- `ckanext.powerbi.client_secret`: PowerBI Client Secret
- `ckanext.powerbi.tenant_id`: PowerBI Tenant ID (same for both production and non-production environments)

The extension also uses these hardcoded URL values:

- `scope_base`: `"https://analysis.windows.net/powerbi/api/.default"`
- `authority_url`: `"https://login.microsoftonline.com/"+tenant_id`

> **Security Note**: The credentials for the service principal are securely stored in Azure DevOps and managed through AWS Secrets Manager during container deployment.

### Prerequisites and Dependencies

The `tfnsw_powerbiview` extension relies on the [MSAL](https://pypi.org/project/msal/) library for authentication, which is installed during the `ckanext-tfnsw` installation.

### Microsoft Documentation and References

This extension was adapted from the following resources:
- [Microsoft PowerBI Embed Sample for Customers](https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-sample-for-customers?tabs=net-core)
- [PowerBI Developer Samples on GitHub](https://github.com/microsoft/PowerBI-Developer-Samples/tree/master/Python/Embed%20for%20your%20customers)

## How It Works

1. **Add the Extension to CKAN**: Ensure that the `tfnsw_powerbiview` extension is included in the `ckan.ini` configuration file.

2. **Add a Resource**: In CKAN, create a resource for the dataset associated with the PowerBI report. This resource serves as the anchor for the view, even if it doesn’t contain any data.

3. **Create the PowerBI View**: In the newly created resource, select "PowerBI View" from the view type dropdown.

4. **Enter the PowerBI Report URL**: Enter the URL of the PowerBI report you wish to embed.

5. **Render the View**:
   - When the view is loaded, the extension uses the `msal` library to authenticate with PowerBI via the service principal, obtaining an access token with the `client_id`, `client_secret`, and `authority_url`.
   - Using this access token, the extension retrieves the embed information for the specified report.
   - It then generates an embed token by calling the PowerBI `/GenerateToken` API for the report URL.
   - The embed information and token are then returned to the HTML page.
   - JavaScript in the HTML page uses the embed information and token to render the PowerBI report within the CKAN interface.

This setup enables secure, embedded access to PowerBI reports within CKAN, providing users with a seamless experience while maintaining strict access controls.