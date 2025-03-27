---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrading-v7.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrading-v6.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrading-v5.html
navigation_title: "Upgrade on {{ech}}"
---

# Upgrade on {{ech}} (ECH)

Once you are [prepared to upgrade](../../../deploy-manage/upgrade/deployment-or-cluster.md), a single click in the {{ecloud}} console can upgrade a deployment to a newer version, add more processing capacity, change plugins, and enable or disable high availability, all at the same time. During the upgrade process, {{es}}, {{kib}}, and all of your deployment components are upgraded simultaneously.

Minor version upgrades, upgrades from 8.18 to 9.0, and cluster configuration changes can be performed with no downtime. {{ecloud}} only supports upgrades to released versions. Release candidate builds and master snapshots are not supported.

::::{important} 
Although it’s simple to upgrade an {{ecloud}} deployment, the new version might include breaking changes that affect your application. Ensure you review breaking changes and deprecation logs, make any necessary changes, and test against the new version before upgrading your production deployment.
::::

## Perform the upgrade [perform-cloud-upgrade] 

Log in to your {{ecloud}} environment:

1. Log in to the [{{ech}} console](https://cloud.elastic.co/login). 
2. Select your deployment on the home page in the {{ech}} card or go to the **Deployments** page.
      
   Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.


To upgrade a deployment:

1. In the **Deployment version** section, click **Upgrade**.
2. Select the appropriate version you're upgrading to. 
3. Click **Upgrade**, then **Confirm upgrade**. The new configuration takes a few minutes to create.

    ::::{note} 
    If any incompatibilities are detected when you attempt to upgrade, the UI provides a link to the Upgrade Assistant, which checks for deprecated settings in your cluster and indices and helps you resolve them. If there are any issues that would prevent a successful upgrade, the upgrade is blocked. After resolving the issues, return to the **Deployments** page and restart the upgrade. Also check the [release notes](/release-notes/index.md) to stay aware of changes and known issues for the version you're upgrading to.
    ::::


Snapshots
:   To keep your data safe during the upgrade process, a snapshot is taken automatically before any changes are made to your cluster. After a major version upgrade is complete and a snapshot of the upgraded cluster is available, all snapshots taken with the previous major version of {{es}} are stored in the snapshot repository.


Security realm settings
:   During the upgrade process, you are prompted to update the security realm settings if your user settings include a `xpack.security.authc.realms` value.

    If the security realms are configured in `user_settings`, you’ll be prompted to modify the settings:

    1. On the **Update security realm settings** window, edit the settings.
    2. Click **Update settings**. If the security realm settings are located in `user_settings_override`, contact support to help you upgrade.

### Next steps

Once you've successfully upgraded on {{ech}}, [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md), such as {{ls}}, {{agents}}, or {{beats}}. 
