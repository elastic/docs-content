---
type: how-to
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: kibana
navigation_title: Customize Kibana branding
description: Replace the default Elastic branding in Kibana with your own logo, organization name, page title, and favicon.
---

% Companion page to the Custom branding section of the Advanced Settings reference:
% kibana://reference/advanced-settings.md#kibana-custom-branding-settings
% If setting names, descriptions, or constraints change in either page, update the other too.

# Customize {{kib}} branding

Replace the default Elastic logo, organization name, browser tab title, and favicon with your own custom assets. Changes apply globally to all spaces in the deployment.

## Before you begin

- You must have an [Enterprise subscription](https://www.elastic.co/subscriptions).
- You must have the `Advanced Settings` {{kib}} privilege.

## Configure custom branding

1. Open **Advanced Settings** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Global Settings** tab.
3. In the **Custom branding** section, configure one or more of the following settings:

   - **Custom logo**: Upload an image to replace the Elastic logo in the header of all {{kib}} pages. Logos look best when they are no larger than 128×128 pixels and have a transparent background. The file must be less than 200 kilobytes.
   - **Organization name**: Upload an image to replace the text next to the logo in the header. Images look best when they are no larger than 200×84 pixels and have a transparent background. The file must be less than 200 kilobytes.
   - **Page title**: The text that appears on {{kib}} browser tabs.
   - **Favicon (SVG)**: Enter the URL of a custom SVG image to display on {{kib}} browser tabs. The recommended size is 16×16 pixels.
   - **Favicon (PNG)**: Enter the URL of a custom PNG image for browsers that don't support SVG.

4. Select **Save changes**. A confirmation toast confirms that your settings were saved.
5. Refresh the page to apply the new branding.

:::{tip}
To revert a setting to its default value, clear the field and select **Save changes**.
:::

## Related pages

- [{{kib}} advanced settings](kibana://reference/advanced-settings.md#kibana-custom-branding-settings)
