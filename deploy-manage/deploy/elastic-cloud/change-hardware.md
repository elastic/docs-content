---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-change-hardware-for-a-specific-resource.html
---

# Change hardware [ec-change-hardware-for-a-specific-resource]

The virtual hardware on which Elastic stack deployments run is defined by instance configurations. To learn more about what an instance configuration is, refer to [Instance configurations](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html#ec-getting-started-configurations).

When a deployment is created, each Elasticsearch tier and stateless resource (e.g., Kibana, Enterprise Search) gets an instance configuration assigned to it, based on the hardware profile used. The combination of instance configurations defined within each hardware profile is designed to provide the best possible outcome for each use case. Therefore, it is not advisable to use instance configurations that are not specified on the hardware profile, except in specific situations in which we may need to migrate an Elasticsearch tier or stateless resource to a different hardware type. An example of such a scenario is when a cloud provider stops supporting a hardware type in a specific region.


## Migrate to a different instance configuration using the API [ec_migrate_to_a_different_instance_configuration_using_the_api]

Hardware profile migrations are possible to perform through the Elastic Cloud console, however, migrating a specific tier or resource to a different instance configuration can only be achieved through the API.

Prerequisites:

* A valid Elastic Cloud [API key](../../api-keys/elastic-cloud-api-keys.md) (`$EC_API_KEY`)

Follow these steps to migrate to a different instance configuration, replacing the default `$EC_API_KEY` value with your actual API key:

1. From the  [list of instance configurations available for each region](https://www.elastic.co/guide/en/cloud/current/ec-regions-templates-instances.html), select the target instance configuration you want to migrate to.
2. Get the deployment update payload from the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body) **Edit** page, by selecting **Equivalent API request**, and store it in a file called `migrate_instance_configuration.json`.

    Example payload containing relevant data for migrating the hot Elasticsearch tier:

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

3. Set the `instance_configuration_id` field of the Elasticsearch tier or stateless resource you want to migrate to the **Instance ID** of the instance configuration selected in step 1.
4. If the `instance_configuration_version` field is defined for that Elasticsearch tier or stateless resource, remove it from the payload.

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
Having an instance configuration mismatch between the deployment and the hardware profile will cause the Elastic Cloud console to announce that there is a **Newer version available** for the hardware profile. Any hardware profile migration performed through the Elastic Cloud console will cause the instance configurations to be reset to the values in the hardware profile.
::::



## Deprecated instance configurations (ICs) and deployment templates (DTs) [ec-deprecated-icdt]

A list of deprecated and valid ICs/DTs can be found on the [Available regions, deployment templates and instance configurations](https://www.elastic.co/guide/en/cloud/current/ec-regions-templates-instances.html) page, as well as through the API, using `hide_deprecated` to return valid ICs/DTs. For example, to return valid ICs/DTs the following request can be used: `https://api.elastic-cloud.com/api/v1/deployments/templates?region=us-west-2&hide_deprecated=true`. To list only the deprecated ones, this can be used: `https://api.elastic-cloud.com/api/v1/deployments/templates?region=us-west-2&metadata=legacy:true`.

If a deprecated IC/DT is already in use, it can continue to be used. However, creating or migrating to a deprecated IC/DT is no longer possible and will result in a plan failing. In order to migrate to a valid IC/DT, navigate to the **Edit hardware profile** option in the Cloud UI or use the [Deployment API](https://www.elastic.co/docs/api/doc/cloud/operation/operation-migrate-deployment-template).
