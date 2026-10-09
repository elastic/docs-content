---
navigation_title: Personal preferences
description: Change how Kibana looks and behaves for you only, including color mode, contrast, language, the space Kibana opens at login, and your navigation menu layout.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
type: overview
---

# Personal preferences in {{kib}}

You can change how {{kib}} looks and behaves for you without affecting anyone else. {{kib}} saves each preference with your user in the current project or deployment, so it stays in place when you switch browsers or devices.

## Preferences you can set

Each preference applies either in all your spaces or in each space separately. Select a preference to see how to change it.

| Preference | What you can do | Where it applies |
|---|---|---|
| [Color mode](/explore-analyze/find-and-organize/personal-preferences/dark-mode.md) | Show {{kib}} in light or dark colors, or match your operating system. | All your spaces |
| [Contrast](/explore-analyze/find-and-organize/personal-preferences/high-contrast.md) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` Use normal or high contrast to improve visibility, or match your operating system. | All your spaces |
| [Language](/explore-analyze/find-and-organize/personal-preferences/change-interface-language.md) | {applies_to}`serverless: beta` {applies_to}`stack: beta 9.5+` Show the {{kib}} interface in another language. | All your spaces |
| [Space at login](/deploy-manage/choose-and-switch-spaces.md#remember-last-selected-space) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` Open the last space you used when you log in, or show the space selector instead. Availability depends on your deployment type. | All your spaces |
| [Navigation menu layout](/explore-analyze/find-and-organize/customize-navigation.md) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` Reorder the apps in the navigation menu and hide the ones you don't use. | Each space separately |

## Find your preferences

Where you open a preference depends on how you sign in to {{kib}}:

* If you sign in with your {{ecloud}} account, select the item for the preference you want from the user menu in the global header.
* If you sign in any other way, for example with a username and password or on a self-managed deployment, select **Edit profile** from the user menu in the global header to open your profile page.

The items in the user menu and the sections on the profile page use the same names:

* **Appearance**: Color mode and contrast
* **Language**: Interface language
* **Spaces preferences**: Space at login

You change the layout of the navigation menu with **Customize navigation**, which you can open from **More** in the navigation menu. It's available only in spaces that use a solution view (**Search**, **Observability**, or **Security**), not in spaces that use the **Classic** solution view. A space you haven't customized keeps its default layout. Refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md) for the steps.

## Settings that apply to everyone

Some settings change {{kib}} for everyone in a space instead of only for you. Administrators manage these settings. For more information, refer to:

* [Manage {{kib}} Spaces](/deploy-manage/manage-spaces.md)
* [Advanced settings](kibana://reference/advanced-settings.md)

To manage your {{ecloud}} account, such as your email address, password, or organizations, refer to [](/cloud-account/index.md).

## Related pages

* [The {{kib}} interface](/explore-analyze/find-and-organize/kibana-interface.md)
* [Select and switch {{kib}} spaces](/deploy-manage/choose-and-switch-spaces.md)
