---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-image.html
---

# Image panels [add-image]

To personalize your dashboards, add your own logos and graphics with the **Image** panel.

::::{important}
Image uploads are limited to 10 MiB.

::::


You can upload images from your computer, select previously uploaded images, or add images from an external link.

1. From your dashboard, select **Add panel**.
2. In the **Add panel** flyout, select **Image**. The **Add image** flyout appears and lets you add and configure the image you want to display.
3. Add your image and configure the settings, and then click **Save**.

:::{image} ../../images/kibana-dashboard_addImageEditor_8.7.0.png
:alt: Add image editor
:class: screenshot
:::

To manage your uploaded image files, go to the **Files** management page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{warning}
When you export a dashboard, the uploaded image files are not exported. When importing a dashboard with an image panel, and the image file is unavailable, the image panel displays a `not found` warning. Such panels have to be fixed manually by re-uploading the image using the panel’s image editor.

::::


