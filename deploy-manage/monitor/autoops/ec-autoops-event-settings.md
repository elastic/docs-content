---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-event-settings.html
---

# Events Settings [ec-autoops-event-settings]

AutoOps events are triggered when specific conditions are met and are closed when those conditions are no longer satisfied. An event can be triggered by multiple conditions, and each event comes with a default setting that can be adjusted differently for each connected deployment.

::::{note}
Only a user with Cloud Organization Owner role can set up notifications.
::::


To view event settings, go to the event details page and select **Customize** from the menu. Note that for some events, AutoOps doesn’t provide the option to customize it.

The event settings include:

* Event trigger threshold - This is a list of parameters explicitly set for an event. Default settings can be adjusted to meet operational and business needs. You can apply different settings to some or all deployments.
* Index patterns to exclude - AutoOps will exclude system indices to prevent unnecessary events from opening. You can add or remove indices from the list.
* Data roles tier to exclude from indications - Add threshold based on the type of data tier.

:::{image} ../../../images/cloud-autoops-event-settings.png
:alt: Event settings
:::


## Event settings report [ec-event-settings-report]

The **Event Settings** report provides a list of all the events for which the settings were modified.

From the **Event Settings** report, you can click **Add** to add new settings, or select the edit icon to modify the existing settings.

:::{image} ../../../images/cloud-autoops-events-settings-report.png
:alt: Event settings report
:::

