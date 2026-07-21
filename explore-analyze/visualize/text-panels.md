---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-text.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Text panels [add-text]

To provide context to your dashboard panels, add **Text** panels that display important information, instructions, images, and more. You can create **Text** panels using GitHub-flavored Markdown text.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` You can also save a Markdown panel to the **Visualize Library** to reuse it across multiple dashboards. For details, refer to [Save and reuse Markdown panels across dashboards](#markdown-library-reuse).

## Create a Markdown panel [create-markdown-panel]

:::::{applies-switch}

::::{applies-item} { stack: ga 9.2, serverless: }  
1. From your dashboard, select **Add** => **New panel**.
2. In the **Add panel** flyout, select **Markdown Text**. A Markdown editor appears and lets you configure the information you want to display. 
3. Enter your text, then click **Apply**.

While switching between **Editor** and **Preview** modes, you can keep editing your text.

For example, in **Editor** mode you enter:

:::{image} /explore-analyze/images/kibana-markdown-editor-mode.png
:alt: Markdown text with links
:screenshot:
:width: 60%
:::

The following instructions are displayed in **Preview** mode:

:::{image} /explore-analyze/images/kibana-markdown-preview-mode.png
:alt: Panel with markdown link text
:screenshot:
:width: 60%
:::

Or when you enter:

:::{image} /explore-analyze/images/kibana-markdown-editor-screenshot.png
:alt: Markdown text with image file
:screenshot:
:width: 60%
:::

The following image is displayed:

:::{image} /explore-analyze/images/kibana-markdown-preview-screenshot.png
:alt: Panel with markdown image
:screenshot:
:width: 60%
:::

For detailed information about writing on GitHub, click **Syntax help** on the top-right of the Markdown editor.
::::

::::{applies-item} stack: ga 9.0-9.1
1. From your dashboard, select **Add panel**.
2. In the **Add panel** flyout, select **Text**. A Markdown editor appears and lets you configure the information you want to display.
3. In the **Markdown** field, enter your text, then click **Update**.

For example, when you enter:

:::{image} /explore-analyze/images/kibana-markdown_example_1.png
:alt: Markdown text with links
:screenshot:
:width: 75%
:::

The following instructions are displayed:

:::{image} /explore-analyze/images/kibana-markdown_example_2.png
:alt: Panel with markdown link text
:screenshot:
:width: 75%
:::

Or when you enter:

:::{image} /explore-analyze/images/kibana-markdown_example_3.png
:alt: Markdown text with image file
:screenshot:
:width: 75%
:::

The following image is displayed:

:::{image} /explore-analyze/images/kibana-markdown_example_4.png
:alt: Panel with markdown image
:screenshot:
:::

For detailed information about writing on GitHub, click **Help** on the top-right of the Markdown editor.
::::

:::::

## Save and reuse Markdown panels across dashboards [markdown-library-reuse]

```{applies_to}
stack: ga 9.4
serverless: ga
```

Save a Markdown panel to the **Visualize Library** so you can add it to multiple dashboards. When you edit a saved Markdown panel, your changes are reflected on every dashboard that uses it. For an overview of the library, refer to [Visualize Library](visualize-library.md).

### Save a Markdown panel to the library [markdown-save-to-library]

To save an existing Markdown panel from a dashboard to the **Visualize Library**:

1. On your dashboard, open the {icon}`boxes_vertical` panel menu of the Markdown panel.
2. Select **Save to library**.
3. Enter a **Title** for the panel, then select **Save**.

The panel is now linked to the library. Any subsequent edit you apply to it from a dashboard updates the library entry, and the change appears on every dashboard where the panel is added.

### Add a saved Markdown panel from the library [markdown-add-from-library]

To add a previously saved Markdown panel to a dashboard:

1. From your dashboard, select **Add panel** > **From library** in the toolbar.
2. From the **Types** dropdown, select **Markdown**.
3. Select the panel you want to add.

### Unlink a Markdown panel from the library [markdown-unlink-from-library]

To make changes to a saved Markdown panel on a single dashboard without affecting other dashboards, unlink it from the library:

1. On your dashboard, open the {icon}`boxes_vertical` panel menu of the Markdown panel.
2. Select **Unlink from library**.

The panel is now part of the dashboard only. Edits you make to it no longer update the library entry or other dashboards.

