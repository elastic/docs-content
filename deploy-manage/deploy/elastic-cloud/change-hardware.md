---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-change-hardware-for-a-specific-resource.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Customize instance configuration [ec-change-instance-configuration]

This document explains how to modify the instance configurations used by specific components of your deployment without changing the overall hardware profile assigned to the deployment. This advanced configuration scenario is useful in situations where you need to migrate an Elasticsearch tier or stateless resource to a different hardware type.

## Consideration [ec-considerations-on-changing-ic]

{{stack}} deployments run on virtual hardware defined by instance configurations. For more details, refer to [Hardware profiles](./ec-change-hardware-profile.md#ec-hardware-profile) and [Instance configurations](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) documents.

When a deployment is created, each {{es}} tier and stateless resource (e.g., Kibana) gets an instance configuration assigned to it, based on the hardware profile used. The combination of instance configurations defined within each hardware profile is designed to provide the best possible outcome for each use case. Therefore, it is not advisable to use instance configurations that are not specified on the hardware profile, except in specific situations in which we may need to migrate an {{es}} tier or stateless resource to a different hardware type. An example of such a scenario is when a cloud provider stops supporting a hardware type in a specific region.


## Migrate to a different instance configuration using the API [ec_migrate_to_a_different_instance_configuration_using_the_api]

Hardware profile migrations are possible to perform through the {{ecloud}} console, however, migrating a specific tier or resource to a different instance configuration can only be achieved through the API.

Prerequisites:

* A valid {{ecloud}} [API key](../../api-keys/elastic-cloud-api-keys.md) (`$EC_API_KEY`)

Follow these steps to migrate to a different instance configuration, replacing the default `$EC_API_KEY` value with your actual API key:

1. From the  [list of instance configurations available for each region](cloud://reference/cloud-hosted/ec-regions-templates-instances.md), select the target instance configuration you want to migrate to.

   ::::{note}
   The target instance configuration must be compatible with the {{es}} tier or stateless resource you are updating.
   For example, if you are migrating the hot {{es}} tier, the target instance configuration must also be of the `es.datahot` family.
   ::::

2. Get the deployment update payload from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) **Edit** page, by selecting **Equivalent API request**, and store it in a file called `migrate_instance_configuration.json`.

    Example payload containing relevant data for migrating the hot {{es}} tier:

    ```json
    {
      "resources": {
        "elasticsearch": [
          {
            "plan": {
              "cluster_topology": [
                {
                  "id": "hot_content",
                  "instance_configuration_id": "gcp.es.datahot.n2.68x10x45",
                  "instance_configuration_version": 1,
    ```

3. Set the `instance_configuration_id` field of the {{es}} tier or stateless resource you want to migrate to the **Instance ID** of the instance configuration selected in step 1.
4. If the `instance_configuration_version` field is defined for that {{es}} tier or stateless resource, remove it from the payload.

    Following is the update that would be required to migrate the example above to the `gcp.es.datahot.n2.68x10x95` instance configuration:

    ```json
    {
      "resources": {
        "elasticsearch": [
          {
            "plan": {
              "cluster_topology": [
                {
                  "id": "hot_content",
                  "instance_configuration_id": "gcp.es.datahot.n2.68x10x95",
    ```

5. Use the payload to update your deployment and perform the instance configuration migration.

    ```sh
    curl -XPUT https://api.elastic-cloud.com/api/v1/deployments/{deployment_id} \
    -H "Authorization: ApiKey $EC_API_KEY" \
    -H 'Content-Type: application/json' \
    -d @migrate_instance_configuration.json
    ```


::::{note}
You can perform multiple instance configuration migrations in the same request.
::::


::::{warning}
Having an instance configuration mismatch between the deployment and the hardware profile will cause the {{ecloud}} console to announce that there is a **Newer version available** for the hardware profile. Any hardware profile migration performed through the {{ecloud}} console will cause the instance configurations to be reset to the values in the hardware profile.
::::



## Deprecated instance configurations (ICs) and deployment templates (DTs) [ec-deprecated-icdt]

Hardware profile is also referenced as deployment templates in {{ecloud}}. 

You can find a list of deprecated and valid instance configurations (ICs) and deployment templates (DTs) in two ways:

### Public documentation page

Visit the [Available regions, deployment templates and instance configurations](cloud://reference/cloud-hosted/ec-regions-templates-instances.md) page for detailed information.

### API access

Use the [Get deployment templates API](https://www.elastic.co/docs/api/doc/cloud/operation/operation-get-deployment-templates-v2) with query parameters like `hide_deprecated` to retrieve valid ICs and DTs. This API request returns a list of DTs along with the respective ICs referenced within each DT.

For example, 
* To return valid ICs/DTs the following request can be used: `https://api.elastic-cloud.com/api/v1/deployments/templates?region=us-west-2&hide_deprecated=true`. 
* To list only the deprecated ones, this can be used: `https://api.elastic-cloud.com/api/v1/deployments/templates?region=us-west-2&metadata=legacy:true`.

If a deprecated IC/DT is already in use, it can continue to be used. However, creating or migrating to a deprecated IC/DT is no longer possible and will result in a plan failing. In order to migrate to a valid IC/DT, navigate to the **Edit hardware profile** option in the Cloud UI or use the [Deployment API](https://www.elastic.co/docs/api/doc/cloud/operation/operation-migrate-deployment-template).

::::{note}
Deployments using {{stack}} versions prior to 7.10 do not support changing the hardware profile through the {{ecloud}} console or API. To change the hardware profile, first upgrade to version 7.10 or later.
::::

In addtion, you can refer to below information about how these terminologies are referenced. 
* _Deprecated_ is also referenced as _legacy_. 
* Using the `metadata=legacy:true` query parameter will return only legacy/deprecated DTs.
* Using the `hide_deprecated=true` query parameter will return only valid DTs.
* Not using any of the query parameters above will return all DTs. In this case, check the presence of `legacy: true` in the `metadata` entries within the API response, to verify if an IC/DT is deprecated or not.
