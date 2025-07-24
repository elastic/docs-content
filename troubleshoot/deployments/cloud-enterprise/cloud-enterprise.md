---
navigation_title: Elastic Cloud Enterprise
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-troubleshooting.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Troubleshoot Elastic Cloud Enterprise

## Finding deployments [ts-ece-find]

When you first installed Elastic Cloud Enterprise and [logged into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md), three [system deployments](/deploy-manage/deploy/cloud-enterprise/system-deployments-configuration.md) were already in place. After [creating your first deployments](/deploy-manage/deploy/cloud-enterprise/create-deployment.md), you may still be managing only a few. But in a production environment with hundreds or even thousands of deployments, identifying those that require attention becomes critical.

The **Deployments** page in the Cloud UI provides several ways to find deployments that might need your attention, whether you’re troubleshooting, planning upgrades, or performing routine maintenance. You can:

* Review visual health indicators of deployments at a glance.
* Search by full or partial deployment names or IDs.
* Use the **Health** and **Version** filter dropdowns to narrow the list of deployments shown. These filters help you find deployments by version, configuration status, or other attributes, making it easier to identify those that require upgrades, are undergoing changes, or match specific operational criteria.