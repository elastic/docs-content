---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-change-hardware-profile.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Manage hardware profiles [ec-change-hardware-profile]

## Hardware profile [ec-hardware-profile]

Deployment hardware profiles deploy the {{stack}} on virtual hardware. Each hardware profile has a different blend of storage, RAM, and vCPU.

{{ecloud}} regularly introduces new hardware profiles to provide:

* More optimal hardware for applications in the {{stack}}.
* Cost efficiencies when new hardware from Cloud providers becomes available.

::::{tip}
The {{ecloud}} console indicates when a new version of a hardware profile is available in the overview page for your deployment, under the Hardware profile section.
::::


## Change the hardware profile using the {{ecloud}} console [ec_change_the_hardware_profile_using_the_elastic_cloud_console]

::::{note}
Deployments using {{stack}} versions prior to 7.10 do not support changing the hardware profile through the {{ecloud}} console or API. To change the hardware profile, first upgrade to version 7.10 or later.
::::


### Upgrade to the newest version of your current hardware profile [ec_upgrade_to_the_newest_version_of_your_current_hardware_profile]

Note that if there’s no indication that a newer version is available, that means that your deployment is already running on the latest version of that hardware profile.

1. On the deployment overview page, next to your current hardware profile where there is indication of a newer available version, select **Edit**.

    :::{image} /deploy-manage/images/cloud-ec-new-hardware-profile-version.png
    :alt: Badge indicating new hardware profile version
    :width: 50%
    :::

2. Preview the changes for the new hardware profile version.

    :::{image} /deploy-manage/images/cloud-ec-preview-hardware-profile.png
    :alt: Notification showing that a new profile version is there
    :::

    The configuration screen summarizes hardware changes for each component of your deployment.

    :::{image} /deploy-manage/images/cloud-ec-preview-profile-changes.png
    :alt: Preview of the changes between the 2 versions of the hardware profile
    :::

3. Select **Update** to apply the change.


### Change to a different hardware profile [ec_change_to_a_different_hardware_profile]

When the current hardware profile of your deployment isn’t the most optimal one available for your usage, you can change it as follows:

1. On the deployment overview page, next to your current hardware profile, select **Edit**.
2. Select the hardware profile you wish to change to. The configuration screen summarizes hardware changes for each component of your deployment.

    :::{image} /deploy-manage/images/cloud-ec-preview-different-profile-changes.png
    :alt: Preview of the changes between the 2 hardware profiles
    :::

3. Select **Update** to apply the change.

::::{note}
If your deployment is configured for high availability, the hardware profile change does not impact your ability to read and write from the deployment as the change is rolled out instance by instance. Refer to [Plan for production](elastic-cloud-hosted-planning.md) to learn about high availability (HA) and how to configure your deployment as HA.
::::




## Change the hardware profile using the API [ec_change_the_hardware_profile_using_the_api]

::::{note}
Deployments using {{stack}} versions prior to 7.10 do not support changing the hardware profile through the {{ecloud}} console or API. To change the hardware profile, first upgrade to version 7.10 or later.
::::


Prerequisites:

* A valid {{ecloud}} [API key](../../api-keys/elastic-cloud-api-keys.md) (`$EC_API_KEY`)
* The deployment ID of the deployment you wish to modify (`{{deployment_id}}`)

Replace those values with your actual API key and deployment ID in the following instructions.

1. Get the current API payload for your deployment.

    ```sh
    curl \
    -H "Authorization: ApiKey $EC_API_KEY" \
    "https://api.elastic-cloud.com/api/v1/deployments/{deployment_id}"
    ```

2. Using the API payload for your deployment, determine the following:

    * Your current `deployment_template` ID. The template ID corresponds to the hardware profile used for your deployment.

        ```json
        "resources":{
              "elasticsearch":[
                 {
                    "ref_id":"main-elasticsearch",
                    "id":"$CLUSTER_ID",
                    "region":"gcp-us-central1",
                    "info":{
                       "cluster_id":"$CLUSTER_ID",
                       "cluster_name":"$CLUSTER_NAME",
                       "deployment_id":"$DEPLOYMENT_ID",
                       "plan_info":{
                          "current":{
                             "plan":{
                                "deployment_template":{
                                   "id":"gcp-cpu-optimized-v5"
                                },
        ```

    * The region that your deployment is in:

        ```json
        "resources":{
              "elasticsearch":[
                 {
                    "ref_id":"main-elasticsearch",
                    "id":"$DEPLOYMENT_ID",
                    "region":"gcp-us-central1",
        ```

3. Check the [hardware profiles available](cloud://reference/cloud-hosted/ec-regions-templates-instances.md) for the region that your deployment is in and find the template ID of the deployment hardware profile you’d like to use.

    ::::{tip}
    If you wish to update your hardware profile to the latest version available for that same profile, locate the template ID corresponding to the `deployment_template` you retrieved at step 2, but without the version information. For example, if your deployment’s current hardware profile is `gcp-cpu-optimized-v5`, use `gcp-cpu-optimized` as a template ID to update your deployment.
    ::::

4. Get the API payload for your deployment based on the new template ID.

    ```sh
    curl -XGET https://api.elastic-cloud.com/api/v1/deployments/{deployment_id}/migrate_template?template_id={new_template_id} \
    -H "Authorization: ApiKey $EC_API_KEY" > migrate_deployment.json
    ```

5. Use the payload returned to update your deployment to use the hardware profile.

    ```sh
    curl -XPUT https://api.elastic-cloud.com/api/v1/deployments/{deployment_id} \
    -H "Authorization: ApiKey $EC_API_KEY" \
    -H 'Content-Type: application/json' \
    -d @migrate_deployment.json
    ```



## List of hardware profiles [ec_list_of_hardware_profiles]

### Storage optimized [ec-profiles-storage]

Your {{es}} data nodes are optimized for high I/O throughput. Use this profile if you are new to {{es}} or don’t need to run a more specialized workload. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Good for most ingestion use cases with 7-10 days of data available for fast access. Also good for light search use cases without heavy indexing or CPU needs.


### Storage optimized (dense) [ec-profiles-storage-dense]

Your {{es}} data nodes are optimized for high I/O throughput. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Ideal for ingestion use cases with more than 10 days of data available for fast access. Also, good for light search use cases with very large data sets.


### CPU optimized [ec-profiles-compute-optimized]

This profile runs CPU-intensive workloads faster. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Consider this configuration for ingestion use cases with 1-4 days of data available for fast access and for search use cases with indexing and querying workloads. Provides the most CPU resources per unit of RAM.


### CPU optimized (ARM) [ec-profiles-compute-optimized-arm]

This profile is similar to CPU optimized profile but powered by ARM instances. Currently, we offer ARM instances on AWS. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Consider this configuration for ingestion use cases with 1-4 days of data available for fast access and for search use cases with indexing and querying workloads. Provides the most CPU resources per unit of RAM.

### Vector search optimized [ec-profiles-vector-search]

This profile is suited for Vector search, Generative AI and Semantic search optimized workloads. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Optimized for applications that leverage Vector Search and/or Generative AI. Also the optimal choice for utilizing ELSER for semantic search applications. Broadly suitable for all semantic search, text embedding, image search, and other Vector Search use cases.

### Vector search optimized (ARM) [ec-profiles-vector-search-arm]

This profile is suited for Vector search, Generative AI and Semantic search optimized workloads powered by ARM instances. Currently, we offer ARM instances on AWS. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Optimized for applications that leverage Vector Search and/or Generative AI. Also the optimal choice for utilizing ELSER for semantic search applications. Broadly suitable for all semantic search, text embedding, image search, and other Vector Search use cases.


### General purpose [ec-profiles-general-purpose]

This profile runs CPU-intensive workloads faster . You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Suitable for ingestion use cases with 5-7 days of data available for fast access. Also good for search workloads with less-frequent indexing and medium to high querying loads. Provides a balance of storage, memory, and CPU.


### General purpose (ARM) [ec-profiles-general-purpose-arm]

This profile is similar to General purpose profile but powered by ARM instances. Currently, we offer ARM instances on AWS. You can find the exact storage, memory, and vCPU allotment on the [hardware details page](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) for each cloud provider.

**Ideal use case**

Suitable for ingestion use cases with 5-7 days of data available for fast access. Also good for search workloads with less-frequent indexing and medium to high querying loads. Provides a balance of storage, memory, and CPU.
