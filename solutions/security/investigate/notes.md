---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/add-manage-notes.html
  - https://www.elastic.co/guide/en/serverless/current/security-add-manage-notes.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Notes [security-add-manage-notes]

Incorporate notes into your investigative workflows to coordinate responses, conduct threat hunting, and share investigative findings. You can attach notes to alerts, events, and Timelines and manage them from the **Notes** page.

::::{note}
* {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga` You can attach up to 100 notes to alerts and events. The number of notes you can attach to Timelines is unlimited.
* {applies_to}`stack: ga =9.0` Configure the `securitySolution:maxUnassociatedNotes` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#max-notes-alerts-events) to specify the maximum number of notes that you can attach to alerts and events.
::::

## Grant access to notes [notes-privileges]

You can control access to notes by setting the [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) for the **Notes** feature under **Security**.

## View and add notes to alerts and events [notes-alerts-events]

Open the alert or event details flyout to access the **Notes** tab, where you can view existing notes and add new ones. To quickly open the tab, click the **Add note** action (![Add note action](/solutions/images/security-create-note-icon.png "title =20x20")) in the Alerts or Events table. Then, enter a note into the text box, and click **Add note** to create it.

After notes are created, the **Add note** icon displays a notification dot. In the details flyout for alerts, the alert summary in the right panel also shows how many notes are attached to the alert.

:::{image} /solutions/images/security-new-note-alert-event.png
:alt: New note added to an alert
:screenshot:
:::


## View and add notes to Timelines [notes-timelines]

::::{important}
You can only add notes to saved Timelines.
::::


Open the **Notes** Timeline tab, where you can view existing notes for the Timeline and add new ones. Alternatively, use the details flyout for alerts and events that you’re investigating from Timeline. Be aware that notes added this way are automatically attached to the alert or event and the Timeline unless you deselect the **Attach to current Timeline** option.

After notes are created, the **Notes** Timeline tab displays the total number of notes attached to the Timeline.

:::{image} /solutions/images/security-new-note-timeline-tab.png
:alt: New note added to a Timeline
:screenshot:
:::


## Manage all notes [manage-notes]

Use the **Notes** page to view and interact with all existing notes. To access the page, navigate to **Investigations** in the main navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Notes**. From the **Notes** page, you can:

* Search for specific notes
* Filter notes by the user who created them or by the object they’re attached to (notes can be attached to alerts, events, or Timelines)
* Examine the contents of a note (click the text in the **Note content** column)
* Delete one or more notes
* Examine the alert or event that a note is attached to (click the **Expand alert/event details** ![Preview alert or event action](/solutions/images/security-notes-page-document-details.png "title =20x20") icon)
* Open the Timeline that the note is attached to (click the **Open saved timeline** ![Open Timeline action](/solutions/images/security-notes-page-timeline-details.png "title =20x20") icon)

:::{image} /solutions/images/security-notes-management-page.png
:alt: Notes management page
:screenshot:
:::
