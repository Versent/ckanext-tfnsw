# Tableau Adjustable Iframe Extension for CKAN

This extension was created specifically for integrating Tableau visualizations into the CKAN portal. The goal was to seamlessly embed Tableau Public visualizations without the distracting navigation elements and scrollbars, ensuring a consistent user experience within the CKAN environment.

## Problem Statement

When embedding visualizations from Tableau Public, we encountered two main issues:
1. **Navigation Bar Visibility:** The embedded visualizations included a bottom navigation bar, allowing users to access Tableau's site directly. For our purposes, users needed to stay within the CKAN portal.
2. **Scrollbars (Vertical & Horizontal):** Due to varying dimensions of Tableau visualizations, both horizontal and vertical scrollbars appeared in the embedded view, disrupting the layout and usability.

## Solution Overview

After discussions with the Tableau team, we decided to implement the following solutions:

1. **Horizontal Scrollbar Fix**: We created a custom CSS theme to expand the container `<div>`, accommodating wider visualizations and removing the need for horizontal scrolling. The container width was set to **1250px** based on the TFNSW team’s primary visualization needs.

2. **Vertical Scrollbar and Navigation Bar Fix**: By using the `AdjustableIframeView` extension, we embedded Tableau visualizations within an iframe, enabling us to dynamically adjust the iframe’s height based on the visualization. This allowed us to eliminate both the vertical scrollbar and the bottom navigation bar.

## How to Use

1. **Add Extension to CKAN**: Add the `tfnsw_adjustableiframeview` extension to your CKAN.ini.
2. **Add an Empty Resource**: Add an empty resource to the required dataset in CKAN.
3. **Create a View**: Create a view for the new resource. In the view's dropdown menu, select the "Adjustable Iframe" option.
4. **Enter the URL**: You will be prompted to enter the Tableau Public URL of the visualization. Ensure to append an `iframeHeight` parameter to the URL to specify the iframe’s height.
   
   **Example URL**:
   ```
   https://public.tableau.com/views/pathtoviz:showVizHome=no&:embed=true&:&iframeHeight=800
   ```

   - In this example, `iframeHeight=800` sets the iframe’s height to 800px, accommodating the full visualization height and hiding the vertical scrollbar.

5. **Render the View**: When the view is rendered, the Jinja template checks for the `iframeHeight` parameter and sets the iframe height accordingly. This adjustment prevents the appearance of the vertical scrollbar and hides the bottom navigation bar.

### Note
Finding the correct height for the iframe may take a few tries, as the optimal `iframeHeight` value depends on each specific visualization.

