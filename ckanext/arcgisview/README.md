# TFNSW ArcGIS View Extension for CKAN

The `tfnsw_arcgisview` extension was developed to allow the team to share ArcGIS visualizations, which are typically behind a login wall, with the public. This extension ensures that ArcGIS visualizations can be embedded seamlessly in the CKAN portal, providing a smooth user experience without authentication prompts.

## Overview

The `tfnsw_arcgisview` extension enables the embedding of secure ArcGIS visualizations within an iframe in CKAN. By using stored credentials, it automatically generates an authentication token to load the ArcGIS visualization without requiring end users to log in.

### Configuration

The extension requires the following configuration values in `ckan.ini`:

- `ckanext.arcgis.username`: ArcGIS account username (provided by the TFNSW team).
- `ckanext.arcgis.password`: ArcGIS account password (stored securely).
- `ckanext.arcgis.referrer`: The referrer URL for ArcGIS authentication.
- `ckanext.arcgis.arcgis_url`: The base URL for the ArcGIS service.

> **Security Note**: The ArcGIS credentials are stored as secure variables in Azure DevOps and managed within AWS Secrets Manager during container deployment to ensure secure handling.

## How It Works

1. **Add the Extension to CKAN**: Ensure the `tfnsw_arcgisview` extension is added to your `ckan.ini` configuration file.

2. **Add a Resource**: Create a resource in CKAN for the dataset you wish to link with an ArcGIS visualization. This resource doesn’t have to contain data but serves as the basis for creating the view.

3. **Create the View**: In the newly created resource, select "ArcGIS View" from the view type dropdown menu.

4. **Enter the ArcGIS Visualization URL**: Provide the URL for the ArcGIS visualization you want to embed.

5. **Render the View**:
   - When the view is loaded, the extension uses the provided credentials to request an authentication token from ArcGIS.
   - The token is then appended to the ArcGIS URL, allowing it to load securely within an iframe in CKAN.
   - This setup enables CKAN to authenticate automatically with ArcGIS, so users see the visualization without being prompted for login credentials.

By using this extension, TFNSW can display ArcGIS visualizations securely in CKAN, ensuring public access without compromising on authentication security.