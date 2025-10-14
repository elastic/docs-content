---
navigation_title: Upgrade on {{ece}}
applies_to:
  deployment:
    ece: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: elasticsearch
---

# Upgrade your deployment on {{ece}} (ECE)

A single click in the {{ecloud}} console can upgrade a deployment running on ECE to a newer version, add more processing capacity, change plugins, and enable or disable high availability, all at the same time. During the upgrade process, {{es}}, {{kib}}, Elastic APM, and all of your deployment components are upgraded simultaneously.

Once you're [prepared to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md), do the following: 

1. Ensure your current ECE and Docker or Podman versions are [compatible](https://www.elastic.co/support/matrix/#elastic-cloud-enterprise) with the {{stack}} version you're upgrading to. For example, if you're upgrading to 9.0.0, the minimum required version is ECE 4.0. If you don’t have a compatible version installed, [upgrade your orchestrator](/deploy-manage/upgrade/orchestrator/upgrade-cloud-enterprise.md).  
2. Download the most recent [stack pack](/deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md#ece_most_recent_elastic_stack_packs) for the version you’re upgrading to, then [add the stack pack](/deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md#ece-manage-elastic-stack-add) to your ECE installation using the Cloud UI.
3. If not configured already, [assign a snapshots repository](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) to your deployment to enable snapshots and back up your data. Although this is optional, we recommend this step.
 
## Perform the upgrade 

1. [Log in to the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md). 
2. On the **Deployments** page, select your deployment.
   
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

1. In the **Deployment version** section, click **Upgrade**.
2. Select the version you're upgrading to. For example, `9.0.0`.
3. Click **Upgrade**, then **Confirm upgrade**. The new configuration takes a few minutes to create.

   ::::{note} 
   If any incompatibilities are detected when you attempt to upgrade, the UI provides a link to the Upgrade Assistant, which checks for deprecated settings in your cluster and indices and helps you resolve them. If there are any issues that would prevent a successful upgrade, the upgrade is blocked. After resolving the issues, return to the **Deployments** page and restart the upgrade. Also check the [release notes](/release-notes/index.md) to stay aware of changes and known issues for the version you're upgrading to.
   ::::

**Security realm settings**

During the upgrade process, you are prompted to update the security realm settings if your user settings include a `xpack.security.authc.realms` value.

If the security realms are configured in `user_settings`, you’ll be prompted to modify the settings:

1. On the **Update security realm settings** window, edit the settings.
2. Click **Update settings**. If the security realm settings are located in `user_settings_override`, contact support to help you upgrade.

## Next steps

Once you've successfully upgraded your deployment, [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md), such as {{ls}}, {{agents}}, or {{beats}}. 

