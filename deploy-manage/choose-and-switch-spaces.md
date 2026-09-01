---
description: Switch between Kibana spaces from the global header. Control whether Kibana opens your last selected space when you log in, or shows the space selector.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
type: how-to
---

# Select and switch Kibana spaces

The spaces you can open depend on your roles. Switching spaces does not change your permissions.

## Before you begin

You can open only the spaces that your roles grant access to.

## Switch spaces

1. Open the space selector from the [global header](/explore-analyze/find-and-organize/kibana-interface.md#global-header). Where you find it depends on your deployment type and version:

   * {applies_to}`serverless: ga` Select the name of your project in the global header, then select your current space to open **My spaces**.
   * {applies_to}`stack: ga 9.6` In spaces that use a solution view, select the name of your deployment in the global header, then select your current space to open **My spaces**. When the global header shows the name of your current space instead of a deployment name, selecting it opens **My spaces** directly.
   * In all other cases, select the avatar of your current space in the global header to open the **Spaces** menu.

   :::{image} /deploy-manage/images/kibana-change-space.png
   :alt: Change current space menu
   :screenshot:
   :width: 50%
   :::

2. Select the space you want to open.

The selected space opens. It's visible in the header.

## Understand what happens when you log in

If you can access only one space, {{kib}} opens it.

If you can access more than one space, {{kib}} does one of the following:

- {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` {{kib}} can remember the space you last used and open it. If {{kib}} has no remembered space, or you no longer have access to it, {{kib}} asks you to select a space. A direct link to a {{kib}} app or object opens that destination. It does not send you to the remembered space.
- {applies_to}`stack: ga =9.5` The behavior depends on your deployment type:
  - On self-managed deployments, {{ece}}, and {{eck}}, {{kib}} can remember the space you last used and open it. If {{kib}} has no remembered space, or you no longer have access to it, {{kib}} asks you to select a space. A direct link to a {{kib}} app or object opens that destination. It does not send you to the remembered space.
  - On {{ecloud}}, {{kib}} asks you to select a space. It does not persist your last space. The **Spaces preferences** user menu item is not available.
- {applies_to}`stack: ga 9.0-9.4` {{kib}} asks you to select a space.

## Change whether Kibana remembers your last space [remember-last-selected-space]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

This personal preference is on by default. It controls whether {{kib}} opens your last space when you log in.

:::{note}
:applies_to: ech:
On {{ecloud}}, {{kib}} does not persist your last space. The **Spaces preferences** user menu item is not available.
:::

1. Open the user menu from the header.

2. Open the space preference settings. The menu item depends on your deployment:

   * {applies_to}`ech: ga` {applies_to}`serverless: ga` Select **Spaces preferences**.
   * {applies_to}`self: ga` {applies_to}`ece: ga` {applies_to}`eck: ga` Select **Edit profile**.

3. Turn **Remember last selected space** on or off.

4. Save your changes.

The next time you log in, {{kib}} follows this preference. If the preference is off and you can access more than one space, {{kib}} shows the space selector.

## Related pages

- [Spaces](/deploy-manage/manage-spaces.md)
- [The {{kib}} interface](/explore-analyze/find-and-organize/kibana-interface.md)
