---
navigation_title: Deployment health warnings
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-deployment-no-op.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Troubleshoot deployment health warnings on {{ece}} [ece-deployment-no-op]

The {{ece}} **Deployments** page shows the current status of your active deployments. From time to time you may get one or more health warnings, such as the following:

:::{image} /troubleshoot/images/cloud-ec-ce-deployment-health-warning.png
:alt: A screen capture of the deployment page showing a typical warning: Deployment health warning: Latest change to {{es}} configuration failed.
:::

**Single warning**

To resolve a single health warning, we recommended first running a _no-op_ (no operation) plan. This performs a rolling update on the components in your Elastic Cloud Enterprise deployment without actually applying any configuration changes. This is often all that’s needed to resolve a health warning on the UI.

To run a no-op plan:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Select a deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. Select **Save**.

**Multiple warnings**

If multiple health warnings appear for one of your deployments, check [](/troubleshoot/deployments/cloud-enterprise/common-issues.md) or [contact us](/troubleshoot/index.md#contact-us).

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## Additional resources
* [](/troubleshoot/monitoring/deployment-health-warnings.md)
* [Troubleshooting overview](/troubleshoot/index.md)