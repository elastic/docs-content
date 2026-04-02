---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-integrations-server-apm-switch.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
navigation_title: Switch from APM to Integrations Server
---

# Switch from APM to Integrations Server payload on {{ece}} [ece-integrations-server-apm-switch]

This example shows how to use the {{ece}} RESTful API to switch from using the legacy [APM & Fleet Server](https://www.elastic.co/guide/en/cloud-enterprise/3.8/ece-manage-apm-and-fleet.html) to [Integrations Server](manage-integrations-server.md).


## Requirements [ece_requirements_5]

Given a deployment that is using an APM & Fleet Server with {{stack}} version 8.0 or later, it is possible to start using Integrations Server instead by updating the deployment with an Integrations Server payload. Switching from APM & Fleet Server to Integrations Server in this way ensures that the endpoints and credentials currently used by APM Server and Fleet Server remain the same after the switch.

In order to start using the Integrations Server payload, you first need to enable the APM integration for Elastic Agent by following the steps in [Switch to the Elastic APM integration](/solutions/observability/apm/switch-an-elastic-cloud-cluster-to-apm-integration.md).


## API request example [ece_api_request_example_3]

The example shows how to use the API to create a deployment with APM with version 8.0 and update the deployment to switch to Integrations Server.


### Create a deployment with APM [ece_create_a_deployment_with_apm]

::::{note}
When creating a deployment with version 8.0 using an APM payload, the APM integration for Elastic Agent is enabled by default.
::::


The following creates a deployment that uses the `default` deployment template in the `ece-region`

```sh
curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments -H 'content-type: application/json' -d '
{
  "resources": {
    "elasticsearch": [
      {
        "ref_id": "main-elasticsearch",
        "region": "ece-region", <1>
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
            "id": "default" <2>
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
    "apm": [
      {
        "ref_id": "main-apm",
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "ece-region",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "apm",
              "size": {
                "value": 512,
                "resource": "memory"
              },
              "zone_count": 1
            }
          ],
          "apm": {
            "version": "8.0.0"
          }
        }
      }
    ]
  },
  "name": "switch-to-integrations-server",
  "metadata": {
    "system_owned": false
  }
}
'
```

1. The region where the deployment is created
2. The deployment template used by the deployment



### Identify the instance configuration to use for Integrations Server [ece_identify_the_instance_configuration_to_use_for_integrations_server]

Once the deployment is created, find the `instance_configuration_id` for the Integrations Server payload. It must be supported by the deployment template used by the deployment created in the previous step.

In the example above, the deployment was created using the  `default` deployment template in the `ece-region` region.

To find the `instance_configuration_id`, fetch the deployment template using the template ID, the region, and the version used by the deployment (Integrations Server is supported on version 8.0 and higher).

```sh
curl -XGET \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://$COORDINATOR_HOST:12443/api/v1/deployments/templates/default?region=ece-region&show_instance_configurations=false&stack_version=8.0.0"
```

This return a template like

```json
{
    "id": "default",
    "name": "Default",
    "description": "Default deployment template for clusters",
    "deployment_template": {
        "resources": {
            "elasticsearch": [
                ...
            ],
            "kibana": [
                ...
            ],
            "apm": [
                ...
            ],
            "enterprise_search": [
                ...
            ],
            "integrations_server": [
                {
                    "ref_id": "integrations_server-ref-id",
                    "elasticsearch_cluster_ref_id": "es-ref-id",
                    "region": "ece-region",
                    "plan": {
                        "cluster_topology": [
                            {
                                "instance_configuration_id": "integrations.server", <1>
                                "size": {
                                    "value": 512,
                                    "resource": "memory"
                                },
                                "zone_count": 1
                            }
                        ],
                        "integrations_server": {}
                    }
                }
            ]
        }
    },
    "system_owned": true,
    "metadata": [
        {
            "key": "parent_solution",
            "value": "stack"
        }
    ],
    "order": 0,
    "template_category_id": "default"
}
```

1. The instance configuration ID to use in the Integrations Server payload in the next step.



### Update deployment using the Integrations Server payload [ece_update_deployment_using_the_integrations_server_payload]

Finally, to switch to Integrations Server, update the deployment using the Integrations Server payload, setting `instance_configuration_id` to the value identified in the previous step.

```sh
curl -XPUT \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://$COORDINATOR_HOST:12443/api/v1/deployments/<deployment-id>" \
-d '
{
  "prune_orphans": false, <2>
  "resources": {
    "integrations_server": [
      {
        "region": "ece-region",
        "ref_id": "main-integrations_server",
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "integrations.server", <1>
              "size": {
                "value": 512,
                "resource": "memory"
              },
              "zone_count": 1
            }
          ],
          "integrations_server": {
            "version": "8.0.0"
          },
          "transient": {
            "strategy": {
              "autodetect": {}
            }
          }
        }
      }
    ]
  }
}
'
```

1. Make sure to use the `instance_configuration_id` for Integrations Server from the deployment template.
2. Make sure `prune_orphans` is set to `false`. `prune_orphans` is an important parameter. It specifies how resources not included in the body of this PUT request should be handled. If `false`, those resources not included are kept intact.


