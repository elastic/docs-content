---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/introduction.html#kibana-navigation-search
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Find apps and saved objects quickly using the global search field. Search by type, name, and tag with keyboard shortcuts and advanced syntax for efficient navigation.
---

# Find apps and objects [kibana-navigation-search]

To quickly find apps and the objects you create, use the search field in the global header. Search suggestions include deep links into applications, allowing you to directly navigate to the views you need most.

:::{image} /explore-analyze/images/kibana-app-navigation-search.png
:alt: Example of searching for apps
:screenshot:
:width: 60%
:::

You can search for objects by type, name, and tag. To get the most from the search feature, follow these tips:

* Use the keyboard shortcut—**Ctrl**+**/** on Windows and Linux, **Command**+**/** on MacOS—to focus on the input at any time.
* Use the provided syntax keywords.

    |     |     |
    | --- | --- |
    | Search by type | `type:dashboard`<br>Available types: `application`, `canvas-workpad`, `dashboard`, `data-view`, `lens`, `maps`, `query`, `search`, `visualization` |
    | Search by tag | `tag:mytagname`<br>`tag:"tag name with spaces"` |
    | Search by type and name | `type:dashboard my_dashboard_title` |
    | Advanced searches | `tag:(tagname1 or tagname2) my_dashboard_title`<br>`type:lens tag:(tagname1 or tagname2)`<br>`type:(dashboard or canvas-workpad) logs`<br> |


This example searches for visualizations with the tag `design` .

:::{image} /explore-analyze/images/kibana-tags-search.png
:alt: Example of searching for tags
:screenshot:
:width: 60%
:::

