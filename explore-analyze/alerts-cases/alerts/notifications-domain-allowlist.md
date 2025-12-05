---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-organizations-notifications-domain-allowlist.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-hosted
description: Instructions for configuring the domain allowlist that restricts email recipients for alerting notifications.
---

# Notifications domain allowlist [organizations-notifications-domain-allowlist]

The notifications domain allowlist restricts the possible recipients for alert emails. {{es}} {{watcher}} and {{kib}} alerting actions send emails only if the recipient domains are included in this allowlist. You can configure the allowlist from your organization's Contacts page.

::::{note}
The recipients are only restricted if one or more domains are configured. If there are no domains configured, notifications can be sent to any recipient domain (No restrictions apply).
::::

You can configure the allowlist on the organization [Contacts](https://cloud.elastic.co/account/contacts?page=docs&placement=docs-body) page.

::::{warning}
Changes to the allowlist do not take effect immediately. After saving your changes, run a configuration change on each of your deployments to apply the updated allowlist.
::::

## Apply the updated domain allowlist to a deployment [apply-update-domain-allowlist]

### Using the UI [using-the-ui]

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Select a deployment.
3. From your deployment menu, go to the **Edit** page.
4. Select **Save**.

This updates the notifications settings for {{es}} and {{kib}} to reflect what is configured on the organizations **Contacts** page.

### Use the {{ecloud}} Control CLI [use-the-ecloud-control-cli]

Updating multiple deployments through the UI can take a lot of time. Instead, you can use the [{{ecloud}} Control](ecctl://reference/index.md) command-line interface (`ecctl`) to automate the deployment update.

The following example script shows how to update all deployments of an organization:

```bash
$!/bin/bash
ecctl deployment list --format "{{ .ID }}" | while read id ; do
    echo "Updating deployment $id"
    temp_file=$(mktemp)

    # Get current deployment formatted as an update request
    # The request is stored into a temporary file
    ecctl deployment show $id --generate-update-payload > $temp_file

    # Update the deployment using this request
    ecctl deployment update $id --file $temp_file

    rm $temp_file
done
```
