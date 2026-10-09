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


| Preference | What you can do | Where it applies |
|---|---|---|
| [Color mode](/explore-analyze/find-and-organize/personal-preferences/dark-mode.md) | Show {{kib}} in light or dark colors, or match your operating system. | All your spaces |
| [Contrast](/explore-analyze/find-and-organize/personal-preferences/high-contrast.md) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` Use normal or high contrast to improve visibility, or match your operating system. | All your spaces |
| [Language](/explore-analyze/find-and-organize/personal-preferences/change-interface-language.md) | {applies_to}`serverless: beta` {applies_to}`stack: beta 9.5+` Show the {{kib}} interface in another language. | All your spaces |
| [Space at login](/deploy-manage/choose-and-switch-spaces.md#remember-last-selected-space) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` Open the last space you used when you log in, or show the space selector instead. Availability depends on your deployment type. | All your spaces |
| [Navigation menu layout](/explore-analyze/find-and-organize/customize-navigation.md) | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` Reorder the apps in the navigation menu and hide the ones you don't use. | Each space separately |

## Find your preferences

For color mode, contrast, language, and space at login, where you open the preference depends on how you sign in to {{kib}}:

* If you sign in with your {{ecloud}} account, open the user menu in the global header and select the item for the preference, such as **Appearance** or **Language**.
* If you sign in any other way, for example with a username and password or on a self-managed deployment, select **Edit profile** from the user menu in the global header. Your profile page has a section for each preference.

You can reorder and hide apps in the navigation menu of any space that uses a solution view (**Search**, **Observability**, or **Security**). To start, open **Customize navigation** from **More** in the navigation menu. Spaces that use the **Classic** solution view don't offer this option. A space you haven't customized keeps its default layout. Refer to [Customize your navigation menu](/explore-analyze/find-and-organize/customize-navigation.md) for the steps.

## Settings that apply to everyone

Some settings change {{kib}} for everyone in a space instead of only for you. Administrators manage these settings. For more information, refer to:

* [Manage {{kib}} Spaces](/deploy-manage/manage-spaces.md)
* [Advanced settings](kibana://reference/advanced-settings.md)

To manage your {{ecloud}} account, such as your email address, password, or organizations, refer to [](/cloud-account/index.md).

## Related pages

* [The {{kib}} interface](/explore-analyze/find-and-organize/kibana-interface.md)
* [Select and switch {{kib}} spaces](/deploy-manage/choose-and-switch-spaces.md)
