---
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Manage access to AI Features

This page describes how to use the GenAI Settings page to control access to AI-powered features in your deployments in the following ways:


- Manage which AI connectors are available in your environment. 
- Enable or disable AI Assistant and other AI-powered features in your environment.
- {applies_to}`stack: ga 9.2` {applies_to}`serverless: unavailable` Specify in which Elastic solutions the `AI Assistant for Observability and Search` and the `AI Assistant for Security` appear.


## Requirements

- To access the **GenAI Settings** page, you need the `Actions and connectors: all` or `Actions and connectors: read` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- To modify the settings on this page, you need the `Advanced Settings: all` {{kib}} privilege.

## The GenAI Settings page

To manage these settings, go to the **GenAI Settings** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{applies-switch}

:::{applies-item} stack: ga 9.2

![GenAI Settings page for Stack](/explore-analyze/images/ai-assistant-settings-page.png "")


The **GenAI Settings** page has the following settings:

- **Default AI Connector**: Use this setting to specify which connector is selected by default. This affects all AI-powered features, not just AI Assistant. 
- **Disallow all other connectors**: Enable this setting to prevent connectors other than the default connector specified above from being used in your space. This affects all AI-powered features, not just AI Assistant. 
- **AI feature visibility**: This button opens the current Space's settings page. Here you can specify which features should appear in your environment, including AI-powered features. 
- **AI Assistant visibility**: This setting allows you to choose which AI Assistants are available to use and where. You can choose to only show the AI Assistants in their native solutions, in other {{kib}} pages (for example, Discover, Dashboards, and Stack Management), or select **Hide all assistants** to disable AI Assistant throughout {{kib}}.

:::

:::{applies-item} serverless:

![GenAI Settings page for Serverless](/explore-analyze/images/ai-assistant-settings-page-serverless.png "")

The **GenAI Settings** page has the following settings:

- **Default AI Connector**: Click **Manage connectors** to open the **Connectors** page, where you can create or delete AI connectors. To update these settings, you need the `Actions and connectors: all` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **AI feature visibility**: Click **Go to Permissions tab** to access the active {{kib}} space's settings page, where you can specify which features each custom user role has access to in your environment. This includes AI-powered features such as AI Assistant. 

:::

::::

