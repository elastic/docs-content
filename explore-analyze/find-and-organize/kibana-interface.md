---
description: Find your way around the Kibana interface, including the global header, the space switcher, the navigation menu, and the page header of each page.
applies_to:
  stack: ga 9.6
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
type: overview
---

# The {{kib}} interface

Every app opens inside the same {{kib}} layout, so the controls you need stay in the same place as you move between apps:

* The **global header** runs across the top of the screen. It holds the controls that apply everywhere, such as the space switcher and the global search field.
* The **navigation menu** on the left lists the apps you can open.
* The **workspace** fills the rest of the screen. Each page in the workspace opens with a page header that carries the title of the page and the actions available on it.

This layout applies to spaces that use a solution view: **Search**, **Observability**, or **Security**. Spaces that use the **Classic** solution view keep the previous layout. To check or change the solution view of a space, refer to [Spaces](/deploy-manage/manage-spaces.md). In {{serverless-full}}, every project uses a solution view.

## Global header

From left to right, the global header holds the following controls.

| Control | What it does |
|---|---|
| {icon}`logo_elastic` logo | Opens the home page of your current space. |
| Space switcher | Moves you to another space. |
| **Find content...** | Opens the global search field in a modal, where you can search for apps and objects. Refer to [Find apps and objects](/explore-analyze/find-and-organize/find-apps-and-objects.md). |
| {icon}`question` **Help menu** | Opens links to the documentation, to support, and to the connection details of your project or deployment. |
| Your avatar | Opens the user menu, where you can change your appearance and language preferences, customize your navigation menu, and log out. |

### Space switcher

The space switcher shows the name of your current space. On {{ecloud}}, it shows the name of your project or deployment instead, and adds the name of your current space when that project or deployment contains more than one space.

Selecting the switcher opens **My spaces**, which lists the spaces you can access. On {{ecloud}}, it first opens a menu with two entries: select your space name to reach **My spaces**, or select your project or deployment name to reach **My projects** or **My deployments**, where you can manage the current project or deployment, or create another. For the steps to move between spaces, refer to [Spaces](/deploy-manage/manage-spaces.md).

On {{ecloud}}, the switcher also links to the **Connection details** of the current project or deployment, and to **Invite users** when you have permission to manage users.

## Navigation menu

The navigation menu lists the apps of your solution view. When a top-level item contains sub-items, selecting it opens the **secondary navigation** to its right.

You can reorder the apps in the menu and hide the ones you don't use. Refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md).

## Page header

Each page opens with a header that holds the title of the page and everything you can do with it:

* The page title. On pages that describe a single object, such as a dashboard, selecting the title renames the object.
* A back button, on pages that have a parent page. Hovering over it shows where it leads. When a page has more than one parent, the button opens a menu of destinations instead.
* Badges and tabs, on pages that have them.
* The **application menu**, on the right, which holds the actions for the page. When the actions don't all fit, the remaining ones move under {icon}`ellipsis` **More**.

Pages in a solution view don't show a breadcrumb trail. The back button moves you up a level instead.

## Next steps

* To open an app or find an object you created, refer to [Find apps and objects](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* To change which apps appear in the navigation menu, refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md).
* To switch to another space or create one, refer to [Spaces](/deploy-manage/manage-spaces.md).
