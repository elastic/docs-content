---
description: Select and switch Kibana spaces, and control whether Kibana returns to your last space when you log in.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# Select and switch Kibana spaces

The spaces you can access depend on your roles. Switching spaces does not change your permissions.

## Switch spaces

From the global header, select your current space, then select the space you want to open.

:::{image} /deploy-manage/images/kibana-change-space.png
:alt: Change current space menu
:screenshot:
:width: 50%
:::

## Understand what happens when you log in

{applies_to}`ech: ga` {applies_to}`serverless: ga` If you can access more than one space, {{kib}} asks you to select a space when you log in.

{applies_to}`self: ga` {applies_to}`ece: ga` {applies_to}`eck: ga` On self-managed deployments, what {{kib}} opens when you log in depends on your version and whether it has remembered a space:

   - {applies_to}`stack: ga 9.5+` {{kib}} can remember the space you use and return you to it. If {{kib}} has no remembered space or you no longer have access to it, {{kib}} asks you to select a space. A direct link continues to open the linked {{kib}} app or object instead of redirecting you to the remembered space.
   - {applies_to}`stack: ga 9.0-9.4` If you can access more than one space, {{kib}} asks you to select a space.

## Change whether Kibana remembers your space
```{applies_to}
stack: ga 9.5
serverless: unavailable
```

This personal preference controls whether {{kib}} returns you to your last space or shows the space selector when you log in and can access multiple spaces.

1. From the global header's user menu, select **Edit profile**.
2. In **Space Configuration**, turn **Remember last selected space** on or off.
3. Select **Save changes**.

When you turn off **Remember last selected space**, {{kib}} shows the space selector the next time you log in and can access more than one space.

To create, configure, or delete spaces, refer to [Manage spaces](/deploy-manage/manage-spaces.md).
