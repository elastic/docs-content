---
navigation_title: Region and hosting
applies_to:
  stack: ga
  serverless: ga
description: Learn which regions host Elastic Inference Service (EIS), how inference requests are routed, and how to restrict routing with region preferences.
---

# Region and hosting [eis-regions]

This page lists the {{aws}}, Azure, and {{gcp}} regions where Elastic {{infer-cap}} Service (EIS) is available and explains how {{infer}} requests are routed.

## Available regions [available-regions]

**{{aws}}:**

* `us-east-1` (N. Virginia, US)
* `eu-central-1` (Frankfurt, Germany)
* `eu-west-1` (Ireland)

**Azure:**

* `eastus` (Virginia, US)

**{{gcp}}:**

* `asia-southeast1` (Singapore)
* `europe-west1` (Belgium)
* `us-east4` (N. Virginia, US)
* `us-east5` (Columbus, US)

All {{infer}} requests sent through EIS are routed to the nearest region, regardless of where your {{es}} deployment or {{serverless-short}} project is hosted. For deployments and projects in an EU region, we will route to the nearest EIS presence in an EU region.

{applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` If you configure [region preferences](#inference-region-preferences), EIS routes only within your allowed geographies or regions.

Depending on the model being used, request processing can involve Elastic {{infer}} infrastructure and, in some cases, trusted third-party model providers. For example, ELSER and Jina requests are processed entirely within Elastic {{infer}} infrastructure. Other models, such as large language models or third-party embedding models, can involve additional processing by their respective model providers, which can operate in different cloud platforms or regions.

## Inference region preferences [inference-region-preferences]

```{applies_to}
stack: ga 9.5
serverless: ga
```

Region preferences let you restrict where EIS processes {{infer}} requests.
Use them when your organization needs {{infer}} to stay within approved geographies for compliance or data residency.

You can express preferences in one of two ways:

* **Geographies**: Broader geographic areas, shown as options such as **North America — All available regions**.
* **Regions**: Specific cloud service provider regions, for example **US East (N. Virginia) - AWS**.

You must choose either geographies or regions. The two modes are mutually exclusive.

When no region policy is configured, EIS uses the default nearest-region routing described on this page.

### How enforcement works [region-preferences-enforcement]

After you save a region policy:

* EIS routes {{infer}} requests only to locations that match your allowed geographies or regions.
* EIS does not silently fall back to a disallowed region during outages or capacity events.
* Models that aren't available in any of your allowed locations become unavailable for use.
  In model details, check the **Regions** field to see where each model can run.
* If a request targets a model that isn't available in your allowed locations, {{infer}} fails with a `403` error that includes:

  ```text
  Requested model is not available in the allowed inference regions
  ```

* If you try to save a policy that would deny access to {{infer}} endpoints that are already in use by ingest pipelines or indices, {{es}} rejects the change with a conflict error.

### Configure region preferences in Kibana [configure-region-preferences-kibana]

:::{important}
Changing region preferences affects all Elastic {{infer-cap}} Service endpoints across all spaces.
Before you save, check **Regions** in the details for any models you rely on.
Models that aren't available in your allowed locations become unavailable.
:::

To open **Elastic {{infer}}**, you typically need the `Inference Endpoints: all` and `Advanced Settings: read` {{kib}} privileges.
To load and save region preferences, you also need the `manage_inference` {{es}} cluster privilege.

The **Region preferences** dialog lists only the geographies and regions currently available for your deployment.
It can show fewer options than the full EIS hosting list on this page.

1. Go to the **Elastic Inference Service** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Region preferences**.
1. Turn on **Restrict inference to specific locations**.

   :::{image} /explore-analyze/images/eis-manage-region-preferences.png
   :alt: Region preferences dialog with Restrict inference to specific locations turned on and the Geographies tab open
   :screenshot:
   :::

1. Choose a mode:

   * **Geographies**: Select one or more geographic areas.
   * **Regions**: Expand a geography and select one or more cloud provider regions.
1. Select **Save preferences**.
1. In the confirmation dialog, review your pending allowed geographies or regions.

   :::{image} /explore-analyze/images/eis-confirm-region-change.png
   :alt: Confirm region change dialog listing pending allowed regions
   :screenshot:
   :::

1. Select **Save**.

When the update succeeds, {{kib}} shows the **Region preferences saved** message.
If the policy would deny access to in-use {{infer}} endpoints, {{kib}} blocks the update and shows **Region policy update blocked**.

#### Restore default nearest-region routing [restore-default-region-preferences]

1. Open **Region preferences**.
1. Turn off **Restrict inference to specific locations**.
1. Select **I understand this resets my region preferences** in the **Reset region preferences to default?** dialog.
1. Select **Reset to default**.

   :::{image} /explore-analyze/images/eis-reset-region-preferences.png
   :alt: Reset region preferences to default confirmation dialog
   :screenshot:
   :::

### Configure region preferences with the API [configure-region-preferences-api]

You can also manage the region policy with the {{es}} Inference APIs.
These APIs require the `manage_inference` cluster privilege to create, update, or delete a policy, and `monitor_inference` to retrieve it.

To allow specific geographies:

```console
PUT _inference/_region_policy
{
  "region_policy": {
    "allowed_geos": ["us", "eu"]
  }
}
```

Supported geography codes include `us`, `eu`, and `apac`.

To allow specific cloud provider regions:

```console
PUT _inference/_region_policy
{
  "region_policy": {
    "allowed_regions": [
      { "csp": "aws", "region": "us-east-1" },
      { "csp": "gcp", "region": "europe-west1" }
    ]
  }
}
```

If the new policy would deny access to {{infer}} endpoints that are currently referenced by ingest pipelines or indices, the request fails with a conflict (`409`) error similar to:

```text
Cannot put the region policy because it would deny access to the following in-use inference endpoints: <endpoint-ids>. Ensure that these inference endpoints are not in use, or use force to ignore this warning and proceed anyway.
```

Resolve the conflict by removing those endpoint references first, or use the `force` parameter on the [create or update inference region policy]({{es-apis}}operation/operation-inference-put-region-policy) API if you intentionally want to apply the policy anyway.

To retrieve the current policy:

```console
GET _inference/_region_policy
```

If no policy is configured, the response is a `404` error with the reason `No region policy is configured for this deployment`.

To remove the policy and restore default nearest-region routing:

```console
DELETE _inference/_region_policy
```

For full request and response details, refer to the [create or update inference region policy]({{es-apis}}operation/operation-inference-put-region-policy), [get inference region policy]({{es-apis}}operation/operation-inference-get-region-policy), and [delete inference region policy]({{es-apis}}operation/operation-inference-delete-region-policy) APIs.
