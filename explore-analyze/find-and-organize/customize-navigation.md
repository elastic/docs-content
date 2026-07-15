---
description: Reorder and hide apps in the Kibana navigation menu to match how you work. Customizations apply only to you and only in the current space.
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
---

# Customize your navigation menu

You can reorder the apps in the navigation menu and hide the ones you don't use, so the layout matches how you work. Your changes apply only to you, and only in the current space. Other users of the space are not affected.

## Before you begin

Navigation customization is available only in spaces that use a solution view (**Search**, **Observability**, or **Security**). It is not available in spaces that use the **Classic** solution view. To check or change the solution view of a space, refer to [Manage spaces](/deploy-manage/manage-spaces.md).

## Reorder and hide apps

1. Open the **Customize navigation** modal in either of these ways:

    * From the user menu, select your avatar in the header, then select **Customize navigation**.
    * In the navigation menu, select **More**, then select **Customize navigation**.

2. Make your changes:

    * To reorder an app, drag it by its handle to a new position in the list.
    * To hide an app, turn off its toggle or drag it to the **Hide under More** list. Hidden apps remain available from the **More** menu in the navigation menu.
    * To show a hidden app again, turn on its toggle or drag it back to the top list.

    Your changes preview live in the navigation menu as you make them.

3. Select **Apply** to save your layout. To discard your changes instead, select **Cancel**.

The navigation menu now reflects your new order, and any apps you hid appear under **More**.

:::{note}
When screen space is limited, some visible apps might still appear under **More** even if you haven't hidden them.
:::

## Reset to the space default

To discard all of your customizations and return to the space's default layout, open the **Customize navigation** modal, select **Reset to default**, then select **Apply**.

## Related pages

Adjust other Kibana settings to your own preferences:

* [Use dark mode in Kibana](/cloud-account/dark-mode.md)
* [Use high-contrast mode in Kibana](/cloud-account/high-contrast.md)
