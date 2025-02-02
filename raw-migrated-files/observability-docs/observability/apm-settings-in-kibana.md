---
navigation_title: "Settings"
---

# Applications UI settings [apm-settings-in-kibana]


You do not need to configure any settings to use the Applications UI. It is enabled by default. If you’d like to adjust the default settings, see [APM Settings](https://www.elastic.co/guide/en/kibana/current/apm-settings-kb.html).


## APM Indices [apm-indices-settings]

The Applications UI uses data views to query APM indices. To change the default APM indices that the Applications UI queries, open the Applications UI and select **Settings** → **Indices**. Index settings in the Applications UI take precedence over those set in `kibana.yml`.

APM indices are {{kib}} Spaces-aware; Changes to APM index settings will only apply to the currently enabled space. See [Control access to APM data](../../../solutions/observability/apps/control-access-to-apm-data.md) for more information.


## APM Labs [apm-labs]

**APM Labs** allows you to easily try out new features that are technical preview.

To enable APM labs, navigate to **Applications** → **Settings*** → ***General settings*** and toggle ***Enable labs button in APM**. Select **Save changes** and refresh the page.

After enabling **APM Labs** select **Labs** in the toolbar to see the technical preview features available to try out.
