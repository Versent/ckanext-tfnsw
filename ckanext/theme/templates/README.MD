# CKANEXT-TFNSW Template Overrides

## Template Overrides Details

### `template/packages/snippets/additional_info.html`
This template was extended to support hyperlinks in the "Additional Information" section of the dataset page. The added code checks if the value from the key-value pair is a URL and, if it is, displays it as a hyperlink.

### `template/packages/snippets/resource_view.html`
When adding a view to a resource, it was observed that CKAN provided an "Embed" button on the view page, which offered HTML code for embedding CKAN pages on other websites. TFNSW requested the removal of this button, so it was removed from the resource view page.

### `template/page.html`
This template was modified to include a new custom CSS snippet that expands the container div by 50px to accommodate the Tableau visualization added to the page. Without this change, a horizontal scrollbar appeared on the frame.

### `public/container_theme.css`
This file contains a custom CSS snippet that was added to the `page.html` template to expand the container div by 50px to accommodate the Tableau visualization. Without this change, a horizontal scrollbar appeared on the frame.