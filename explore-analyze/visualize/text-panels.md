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

:::::{applies-switch}

::::{applies-item} stack: ga 9.0
Content for Stack 9.1
::::

::::{applies-item} stack: ga 9.2 
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

:::::

