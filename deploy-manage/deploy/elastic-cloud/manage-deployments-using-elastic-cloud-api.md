---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-api-deployment-crud.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Manage deployments using the {{ecloud}} API [ec-api-deployment-crud]

The following examples demonstrate Create, Read, Update and Delete operations on a `deployments` resource. If you haven’t created an API Key yet, you can follow the [Authentication documentation](../../api-keys/elastic-cloud-api-keys.md).


## Listing your deployments [ec_listing_your_deployments]

List the details about all of your {{ech}} deployments.

```sh
curl \
-H "Authorization: ApiKey $EC_API_KEY" \
https://api.elastic-cloud.com/api/v1/deployments
```


## Getting details about a particular deployment [ec_getting_details_about_a_particular_deployment]

List the details about a particular deployment identified by `id`.

```sh
curl \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID"
```


## Using the API to create your first deployment [ec_using_the_api_to_create_your_first_deployment]

When you create a new deployment through the API, you have two options:

1. **Use default values.** The simplest option is to create the deployment using a set of default values that are gathered automatically from a deployment template specified in the API request.
2. **Configure the deployment settings manually.** With this option, the API request to create a new deployment is very descriptive, with many settings to tweak. If you use this option we recommend that you configure your desired deployment in the {{ecloud}} UI and copy the JSON payload.


### Create a deployment using default values [ec-api-examples-deployment-simple]

This example requires minimal information in the API payload, and creates a deployment with default settings and a default name. You just need to specify one of the [available deployment templates](cloud://reference/cloud-hosted/ec-regions-templates-instances.md) in your API request header and the deployment is created using default settings from that template.

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments?template_id=gcp-general-purpose" \
-d '
{
  "version": "8.17.1",<1>
  "region": "gcp-europe-west1"<2>
}
'
```

1. Optional: You can specify a version for the deployment. If this field is omitted a default version is used.
2. Required: One of the [available regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md) must be provided in the request.


A `resource` field can be included in this request (check the following, manual example for the field details). When a `resource` is present, the content of the request is used instead of any default values provided by the deployment template.


### Create a deployment [ec_create_a_deployment]

This example creates a new deployment named "my-first-api-deployment" with the following characteristics:

* Version 8.17.1 of the {{stack}}
* {{es}} cluster in two zones with 4 GB of memory for each node
* 1 GB single zone {{kib}} instance and 1 GB Integrations Server instance

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments" \
-d '
{
  "resources": {
    "elasticsearch": [
      {
        "region": "gcp-us-central1", <1>
        "ref_id": "main-elasticsearch",
        "plan": {
          "cluster_topology": [
            {
              "zone_count": 2, <2>
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                }
              },
              "instance_configuration_id": "gcp.es.datahot.n2.68x16x45", <3>
              "node_roles": [
                "master",
                "ingest",
                "transform",
                "data_hot",
                "remote_cluster_client",
                "data_content"
              ],
              "id": "hot_content",
              "size": {
                "value": 4096, <4>
                "resource": "memory"
              }
            },
            {
              "zone_count": 2,
              "elasticsearch": {
                "node_attributes": {
                  "data": "warm"
                }
              },
              "instance_configuration_id": "gcp.es.datawarm.n2.68x10x190",
              "node_roles": [
                "data_warm",
                "remote_cluster_client"
              ],
              "id": "warm",
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "cold"
                }
              },
              "instance_configuration_id": "gcp.es.datacold.n2.68x10x190",
              "node_roles": [
                "data_cold",
                "remote_cluster_client"
              ],
              "id": "cold",
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "frozen"
                }
              },
              "instance_configuration_id": "gcp.es.datafrozen.n2.68x10x95",
              "node_roles": [
                "data_frozen"
              ],
              "id": "frozen",
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "zone_count": 3,
              "instance_configuration_id": "gcp.es.master.n2.68x32x45",
              "node_roles": [
                "master",
                "remote_cluster_client"
              ],
              "id": "master",
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "zone_count": 2,
              "instance_configuration_id": "gcp.es.coordinating.n2.68x16x45",
              "node_roles": [
                "ingest",
                "remote_cluster_client"
              ],
              "id": "coordinating",
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "zone_count": 1,
              "instance_configuration_id": "gcp.es.ml.n2.68x32x45",
              "node_roles": [
                "ml",
                "remote_cluster_client"
              ],
              "id": "ml",
              "size": {
                "resource": "memory",
                "value": 0
              }
            }
          ],
          "elasticsearch": {
            "version": "8.17.1",
            "enabled_built_in_plugins": []
          },
          "deployment_template": {
            "id": "gcp-general-purpose-v3" <5>
          }
        }
      }
    ],
    "kibana": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "gcp-us-central1",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "gcp.kibana.n2.68x32x45",
              "zone_count": 1, <6>
              "size": {
                "resource": "memory",
                "value": 1024 <7>
              }
            }
          ],
          "kibana": {
            "version": "8.17.1"
          }
        },
        "ref_id": "main-kibana"
      }
    ],
    "integrations_server": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "gcp-us-central1",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "gcp.integrationsserver.n2.68x32x45",
              "zone_count": 1, <8>
              "size": {
                "resource": "memory",
                "value": 1024 <9>
              }
            }
          ],
          "integrations_server": {
            "version": "8.17.1"
          }
        },
        "ref_id": "main-integrations_server"
      }
    ]
  },
  "name": "my-first-api-deployment"
}
'
```

1. [Available Regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md)
2. Availability zones for the {{es}} cluster
3. [Available instance configurations](cloud://reference/cloud-hosted/ec-regions-templates-instances.md)
4. Memory allocated for each {{es}} node
5. [Available templates](cloud://reference/cloud-hosted/ec-regions-templates-instances.md)
6. Availability zones for Kibana
7. Memory allocated for Kibana
8. Availability zones for Integrations Server
9. Memory allocated for Integrations Server


::::{tip}
You can get the payload easily from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) **Create Deployment** page, customize the regions, zones, memory allocated for each components, and then select **Equivalent API request**.
::::



## Using the API to create deployment with non EOL versions [ec_using_the_api_to_create_deployment_with_non_eol_versions]

You are able to create deployments with *non* [End-of-life (EOL) versions](available-stack-versions.md#ec-version-policy-eol) via API, which are not selectable in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) UI. You can simply replace the version number in the above example.


## Update a deployment [ec_update_a_deployment]

Modify the {{es}} resource by increasing the amount of memory to 8 GB.

```sh
curl -XPUT \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID" \
-d '
{
  "name": "my-first-api-deployment-with-new-name", <1>
  "prune_orphans": false,
  "resources": {
    "elasticsearch": [
      {
        "region": "gcp-us-central1",
        "ref_id": "main-elasticsearch",
        "plan": {
          "cluster_topology": [
            {
              "zone_count": 2,
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                }
              },
              "instance_configuration_id": "gcp.es.datahot.n2.68x16x45",
              "node_roles": [
                "data_hot",
                "data_content",
                "master",
                "ingest",
                "remote_cluster_client",
                "transform"
              ],
              "id": "hot_content",
              "size": {
                "value": 8192, <2>
                "resource": "memory"
              }
            }
          ],
          "elasticsearch": {
            "version": "8.17.1"
          },
          "deployment_template": {
            "id": "gcp-general-purpose-v3"
          }
        }
      }
    ]
  }
}
'
```

1. Give the deployment a new name
2. Increase the amount of memory allocated for each {{es}} node to 8 GB


::::{tip}
You can get the payload easily from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) deployment **Edit** page, customize the zone count, memory allocated for each components, and then select **Equivalent API request**.
::::


A 200 status code means that the configuration change was accepted.
