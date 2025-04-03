---
navigation_title: Edit stack settings
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/editing-user-settings.html
---

# Edit stack user settings [editing-user-settings]

From the {{ece}} console you can customize settings for {{es}}, {{kib}}, and other {{stack}} components by applying **user settings** to your deployments. These settings are internally mapped to the appropriate YAML configuration files, such as `elasticsearch.yml` and `kibana.yml`, and they affect all users of that cluster.

To customize the settings of a deployment's {{stack}} components:

1. Open your deployment page in the ECE [Cloud UI](./log-into-cloud-ui.md).
2. In the left navigation menu, select **Edit**.
3. Look for the **Manage user settings and extensions** and **Edit user settings** links for each deployment, and select the one corresponding to the component you want to update, such as {{es}} or {{kib}}.
4. Apply the necessary settings in the **Users Settings** tab of the editor and select **Back** when finished.
5. Select **Save** to apply the changes to the deployment. Saving your changes initiates a configuration plan change that restarts the affected components for you.

The following sections provide extra details and examples for different components:

* [](./edit-stack-settings-elasticsearch.md)
* [](./edit-stack-settings-kibana.md)
* [](./edit-stack-settings-apm.md)
* [](./edit-stack-settings-enterprise.md)
