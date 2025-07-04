---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-integrations-server-api-example.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Enable Integrations Server through the API [ece-integrations-server-api-example]

This example demonstrates how to use the {{ece}} RESTful API to create a deployment with Integrations Server enabled.

For more information on how to manage Integrations Server from the UI, check [Manage your Integrations Server](manage-integrations-server.md)


## Requirements [ece_requirements_4]

Integrations Server can be enabled only on new deployments, starting with {{stack}} version 8.0.

It’s possible to enable Integrations Server on an existing deployment with version 8.0 only if the legacy [APM & Fleet Server](https://www.elastic.co/guide/en/cloud-enterprise/3.8/ece-manage-apm-and-fleet.html) hasn’t been previously enabled on the deployment.


## API request example [ece_api_request_example_2]

Run this example API request to create a deployment with Integrations Server:

```sh
curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments -H 'content-type: application/json' -d '
{
  "resources": {
    "elasticsearch": [
      {
        "ref_id": "main-elasticsearch",
        "region": "ece-region",
        "plan": {
          "cluster_topology": [
            {
              "id": "hot_content",
              "node_roles": [
                "master",
                "ingest",
                "transform",
                "data_hot",
                "remote_cluster_client",
                "data_content"
              ],
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                },
                "enabled_built_in_plugins": []
              },
              "instance_configuration_id": "data.default",
              "size": {
                "value": 4096,
                "resource": "memory"
              }
            },
            {
              "id": "warm",
              "node_roles": [
                "data_warm",
                "remote_cluster_client"
              ],
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "warm"
                },
                "enabled_built_in_plugins": []
              },
              "instance_configuration_id": "data.highstorage",
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "cold",
              "node_roles": [
                "data_cold",
                "remote_cluster_client"
              ],
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "cold"
                },
                "enabled_built_in_plugins": []
              },
              "instance_configuration_id": "data.highstorage",
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "frozen",
              "node_roles": [
                "data_frozen"
              ],
              "zone_count": 1,
              "elasticsearch": {
                "node_attributes": {
                  "data": "frozen"
                },
                "enabled_built_in_plugins": []
              },
              "instance_configuration_id": "data.frozen",
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "coordinating",
              "node_roles": [
                "ingest",
                "remote_cluster_client"
              ],
              "zone_count": 1,
              "instance_configuration_id": "coordinating",
              "size": {
                "value": 0,
                "resource": "memory"
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
              }
            },
            {
              "id": "master",
              "node_roles": [
                "master",
                "remote_cluster_client"
              ],
              "zone_count": 1,
              "instance_configuration_id": "master",
              "size": {
                "value": 0,
                "resource": "memory"
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
              }
            },
            {
              "id": "ml",
              "node_roles": [
                "ml",
                "remote_cluster_client"
              ],
              "zone_count": 1,
              "instance_configuration_id": "ml",
              "size": {
                "value": 1024,
                "resource": "memory"
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
              }
            }
          ],
          "elasticsearch": {
            "version": "8.0.0"
          },
          "autoscaling_enabled": false,
          "deployment_template": {
            "id": "default"
          }
        },
        "settings": {
          "dedicated_masters_threshold": 6,
          "snapshot": {
            "enabled": false
          }
        }
      }
    ],
    "kibana": [
      {
        "ref_id": "main-kibana",
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "ece-region",
        "plan": {
          "zone_count": 1,
          "cluster_topology": [
            {
              "instance_configuration_id": "kibana",
              "size": {
                "value": 1024,
                "resource": "memory"
              },
              "zone_count": 1
            }
          ],
          "kibana": {
            "version": "8.0.0"
          }
        }
      }
    ],
    "enterprise_search": [],
    "integrations_server": [
      {
        "ref_id": "main-integrations_server",
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "ece-region",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "integrations.server",
              "size": {
                "value": 512,
                "resource": "memory"
              },
              "zone_count": 1
            }
          ],
          "integrations_server": {
            "version": "8.0.0"
          }
        }
      }
    ]
  },
  "name": "My deployment",
  "metadata": {
    "system_owned": false
  }
}
'
```


