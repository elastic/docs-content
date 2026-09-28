---
type: how-to
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
navigation_title: Customize Kibana branding
description: Replace the default Elastic branding in Kibana with your own logo, organization name, page title, and favicon.
---

% Companion page to the Custom branding section of the Advanced Settings reference:
% kibana://reference/advanced-settings.md#kibana-custom-branding-settings
% If setting names, descriptions, or constraints change in either page, update the other too.

# Customize {{kib}} branding

Replace the default Elastic logo, organization name, and more with your own custom assets. Changes apply globally to all spaces.

## Before you begin

- You must have an [Enterprise subscription](https://www.elastic.co/subscriptions).
- You must have the `Advanced Settings` {{kib}} privilege.

## Configure custom branding

1. Open **Advanced Settings** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Global Settings** tab.
3. In the **Custom branding** section, configure one or more of the following settings:

   - **Custom logo**: Upload an SVG, JPEG, PNG, or GIF image to replace the Elastic logo in the header of all {{kib}} pages. Logos look best when they are no larger than 128×128 pixels and have a transparent background. The file must be less than 200 kilobytes.
   - **Organization name**: Upload an SVG, JPEG, PNG, or GIF image to replace the text next to the logo in the header. Images look best when they are no larger than 200×84 pixels and have a transparent background. The file must be less than 200 kilobytes.
   - {applies_to}`serverless: unavailable` **Page title**: The text that appears on {{kib}} browser tabs.
   - **Favicon (SVG)**: Enter the URL of a custom SVG image to display on {{kib}} browser tabs. The recommended size is 16×16 pixels.
   - **Favicon (PNG)**: Enter the URL of a custom PNG image for browsers that don't support SVG.

4. Select **Save changes**. A confirmation toast confirms that your settings were saved.
5. Refresh the page to apply the new branding.

:::{tip}
To revert a setting to its default value, clear the field and select **Save changes**.
:::

## Example: Acme Corp custom branding

This example applies consistent branding for a fictional company, Acme Corp, across every custom branding setting. The custom logo and organization name are files you upload directly. The favicons use URLs that point to hosted images instead, so the example values use a placeholder-image service.

| Setting | Example value |
|---|---|
| **Custom logo** | Upload `acme-logo.png`, a 128×128 pixel transparent PNG under 200 kilobytes. |
| **Organization name** | Upload `acme-org-name.png`, a 200×84 pixel transparent PNG under 200 kilobytes. |
| {applies_to}`serverless: unavailable` **Page title** | `Acme Corp` |
| **Favicon (SVG)** | `https://placehold.co/16x16/5B3CC4/FFFFFF?text=A` |
| **Favicon (PNG)** | `https://placehold.co/32x32/5B3CC4/FFFFFF.png?text=A` |

Favicon (PNG) has no recommended size. This example uses 32×32 pixels, a common fallback size for browsers that don't support SVG.

After you save these changes and refresh the page, {{kib}} shows the Acme Corp logo and organization name in the header on every space. On {{stack}} deployments, the browser tab shows `Acme Corp` as the page title. Browser tabs and bookmarks show the Acme Corp favicon instead of the default Elastic favicon.

## Related pages

- [{{kib}} advanced settings](kibana://reference/advanced-settings.md#kibana-custom-branding-settings)
