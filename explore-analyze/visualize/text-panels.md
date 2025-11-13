---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-text.html
description: Add Markdown text panels to dashboards for context and instructions. Display formatted text, images, and links using GitHub-flavored Markdown syntax.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Text panels [add-text]

Text panels add context to dashboards by displaying formatted text, instructions, images, and links. You write content using GitHub-flavored Markdown, which supports headings, lists, code blocks, tables, and more.

Use text panels to explain dashboard purpose, provide usage instructions, document data sources, or add important notes for dashboard viewers.

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

::::{applies-item} stack: ga 9.0
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

