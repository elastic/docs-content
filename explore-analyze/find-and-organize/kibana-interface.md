---
description: Find your way around the Kibana interface, including the global header, the space selector, the navigation menu, and the application menu of each page.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
type: overview
---

# The {{kib}} interface

{{kib}} uses a standard layout that every app follows, so what you need stays in the same place as you move between apps:

* The **global header** runs across the top of the screen and stays the same in every app.
* The **navigation menu** on the left lists the apps you can open.
* The **workspace** fills the rest of the screen. Each page opens with an **application menu** that holds the actions available on it.

Two more elements appear as you work:

* A **flyout** slides in from the right of the workspace to show contextual content, such as the details of a table row.
* {applies_to}`stack: ga 9.4` The **sidebar** is a resizable panel on the right of the screen, where apps such as the AI assistant open beside your work.

This page describes spaces that use a solution view: **Search**, **Observability**, or **Security**. Spaces that use the **Classic** solution view have a different layout. To check or change the solution view of a space, refer to [Spaces](/deploy-manage/manage-spaces.md). In {{serverless-full}}, every project uses a solution view.

## Global header

The global header holds the following elements.

| Element | What it does |
|---|---|
| {icon}`logo_elastic` logo | Opens the home page of your current space. |
| Space selector | Moves you to another space.<br>{applies_to}`stack: ga 9.6` On {{ecloud}}, it also opens your other projects or deployments, the **Connection details** of the current one, and **Invite users**. |
| Global search field | Searches for apps and for the objects you created. Refer to [Find apps and objects](/explore-analyze/find-and-organize/find-apps-and-objects.md). |
| {icon}`question` **Help menu** | Opens links to the documentation, to support, and to the connection details of your project or deployment. |
| AI assistant or agent | Opens the AI assistant or agent of your solution. Its label depends on which one your project or deployment offers. |
| Your avatar | Opens the user menu, where you can change your appearance and language preferences, customize your navigation menu, and log out. |

{applies_to}`stack: ga 9.6` The space selector shows the name of your current space. On {{ecloud}}, it shows the name of your project or deployment instead, and adds the name of your current space when that project or deployment contains more than one space.

For the steps to move between spaces, refer to [Spaces](/deploy-manage/manage-spaces.md).

## Navigation menu

The navigation menu lists the apps of your solution view. When a top-level item contains sub-items, selecting it opens the **secondary navigation** to its right.

You can reorder the apps in the menu and hide the ones you don't use. Refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md).

## Application menu

The application menu sits at the top of the workspace and holds the actions available on the current page. When the actions don't all fit, the remaining ones move under {icon}`ellipsis` **More**.

{applies_to}`stack: ga 9.6` The application menu also holds the title of the page. On pages that describe a single object, such as a dashboard, selecting the title renames the object. Pages that have a parent page get a back button instead of a breadcrumb trail. Hovering over the back button shows where it leads, and when a page has more than one parent, it opens a menu of destinations.

## Next steps

* To open an app or find an object you created, refer to [Find apps and objects](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* To change which apps appear in the navigation menu, refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md).
* To switch to another space or create one, refer to [Spaces](/deploy-manage/manage-spaces.md).
