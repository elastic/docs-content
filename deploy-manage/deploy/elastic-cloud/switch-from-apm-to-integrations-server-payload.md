---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-integrations-server-apm-switch.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
navigation_title: Switch from APM to Integrations Server
---

# Switch from APM to Integrations Server payload on {{ech}} [ec-integrations-server-apm-switch]

This example shows how to use the {{ecloud}} RESTful API to switch from using [APM & Fleet Server](#ec-manage-apm-and-fleet) to [Integrations Server](manage-integrations-server.md).


### Requirements [ec_requirements_3]

Given a deployment that is using an APM & Fleet Server with {{stack}} version 8.0 or later, it is possible to start using Integrations Server instead by updating the deployment with an Integrations Server payload. Switching from APM & Fleet Server to Integrations Server in this way ensures that the endpoints and credentials currently used by APM Server and Fleet Server remain the same after the switch.

In order to start using the Integrations Server payload, you first need to enable the APM integration for Elastic Agent by following the steps in [Switch to the Elastic APM integration](/solutions/observability/apm/switch-an-elastic-cloud-cluster-to-apm-integration.md).


### API request example [ec_api_request_example_3]

The example shows how to use the API to create a deployment with APM with version 8.0 and update the deployment to switch to Integrations Server.


#### Create a deployment with APM [ec_create_a_deployment_with_apm]

::::{note}
When creating a deployment with version 8.0 using an APM payload, the APM integration for Elastic Agent is enabled by default.
::::


The following creates a deployment that uses the `gcp-storage-optimized` deployment template in the `gcp-us-east4` region

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments" \
-d '
{
  "resources": {
    "apm": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "gcp-us-east4",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "gcp.apm.n2.68x32x45",
              "zone_count": 1,
              "size": {
                "resource": "memory",
                "value": 1024
              }
            }
          ],
          "apm": {
            "version": "8.0.0"
          }
        },
        "ref_id": "main-apm"
      }
    ],
    "elasticsearch": [
      {
        "region": "gcp-us-east4", <1>
        "settings": {
          "dedicated_masters_threshold": 6
        },
        "plan": {
          "autoscaling_enabled": false,
          "cluster_topology": [
            {
              "zone_count": 2,
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                },
                "enabled_built_in_plugins": []
              },
              "instance_configuration_id": "gcp.es.datahot.n2.68x10x45",
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
                "resource": "memory",
                "value": 8192
              }
            },
            {
              "zone_count": 2,
              "elasticsearch": {
                "node_attributes": {
                  "data": "warm"
                },
                "enabled_built_in_plugins": []
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
                },
                "enabled_built_in_plugins": []
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
                },
                "enabled_built_in_plugins": []
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
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
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
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
              }
            },
            {
              "zone_count": 1,
              "instance_configuration_id": "gcp.es.ml.n2.68x16x45",
              "node_roles": [
                "ml",
                "remote_cluster_client"
              ],
              "id": "ml",
              "size": {
                "resource": "memory",
                "value": 0
              },
              "elasticsearch": {
                "enabled_built_in_plugins": []
              }
            }
          ],
          "elasticsearch": {
            "version": "8.0.0"
          },
          "deployment_template": {
            "id": "gcp-storage-optimized" <2>
          }
        },
        "ref_id": "main-elasticsearch"
      }
    ],
    "enterprise_search": [],
    "kibana": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "gcp-us-east4",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "gcp.kibana.n2.68x32x45",
              "zone_count": 1,
              "size": {
                "resource": "memory",
                "value": 1024
              }
            }
          ],
          "kibana": {
            "version": "8.0.0"
          }
        },
        "ref_id": "main-kibana"
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



#### Identify the instance configuration to use for Integrations Server [ec_identify_the_instance_configuration_to_use_for_integrations_server]

Once the deployment is created, find the `instance_configuration_id` for the Integrations Server payload. It must be supported by the deployment template used by the deployment created in the previous step.

In the example above, the deployment was created using the `gcp-storage-optimized` deployment template in the `gcp-us-east4` region.

To find the `instance_configuration_id`, fetch the deployment template using the template ID, the region, and the version used by the deployment (Integrations Server is supported on version 8.0 and higher).

```sh
curl -XGET \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/templates/gcp-storage-optimized?region=gcp-us-east4&show_instance_configurations=false&stack_version=8.0.0"
```

This returns a deployment template like the following:

```json
{
    "description": "Good for most ingestion use cases with 7-10 days of data available for fast access. Also good for light search use cases without heavy indexing or CPU needs.",
    "name": "Storage optimized",
    "template_category_id": "storage-optimized",
    "id": "gcp-storage-optimized",
    "deployment_template": {
        "resources": {
            "integrations_server": [
                {
                    "elasticsearch_cluster_ref_id": "es-ref-id",
                    "region": "gcp-us-east4",
                    "plan": {
                        "cluster_topology": [
                            {
                                "instance_configuration_id": "gcp.integrationsserver.n2.68x32x45", <1>
                                "zone_count": 1,
                                "size": {
                                    "resource": "memory",
                                    "value": 1024
                                }
                            }
                        ],
                        "integrations_server": {}
                    },
                    "ref_id": "integrations_server-ref-id"
                }
            ],
            "elasticsearch": [
                ...
            ],
            "enterprise_search": [
                ...
            ],
            "kibana": [
                ...
            ],
            "apm": [
                ...
            ]
        }
    },
    "order": 1,
    "system_owned": true,
    "metadata": [
        ...
    ]
}
```

1. The instance configuration ID to use in Integrations Server payload in the next step.



#### Update deployment using the Integrations Server payload [ec_update_deployment_using_the_integrations_server_payload]

Finally, to switch to Integrations Server, update the deployment using the Integrations Server payload, setting `instance_configuration_id` to the value identified in the previous step.

```sh
curl -XPUT \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/<deployment-id>" \
-d '
{
  "name": "switch-to-integrations-server",
  "alias": "switch-to-integrations-server",
  "prune_orphans": false, <2>
  "metadata": {
    "system_owned": false,
    "hidden": false
  },
  "resources": {
    "integrations_server": [
      {
        "region": "gcp-us-east4",
        "ref_id": "main-integrations_server",
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "gcp.integrationsserver.n2.68x32x45", <1>
              "zone_count": 1,
              "size": {
                "resource": "memory",
                "value": 1024
              }
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


## Manage your APM & Fleet Server [ec-manage-apm-and-fleet]

::::{note}
Beginning with {{stack}} version 8.0, [Integrations Server](manage-integrations-server.md) is replacing APM & Fleet Server. New deployments with version 8.0 will use Integrations Server automatically. Existing deployments using APM & Fleet Server will continue to use APM & Fleet Server after upgrading to version 8.0.
::::


You have the option to add a combined [Application Performance Monitoring (APM) Server](/solutions/observability/apm/index.md) and [Fleet Server](/reference/fleet/index.md) to your deployment. APM allows you to monitor software services and applications in real time, turning that data into documents stored in the {{es}} cluster. Fleet allows you to centrally manage Elastic Agents on many hosts.

As part of provisioning, the APM Server and Fleet Server are already configured to work with {{es}} and {{kib}}. At the end of provisioning, you are shown the secret token to configure communication between the APM Server and the backend [APM Agents](/reference/apm-agents/index.md). The APM Agents get deployed within your services and applications.

From the deployment **APM & Fleet** page you can also:

* Get the URL to complete the APM agent configuration.
* Use the `elastic` credentials to go to the APM area of {{kib}}. Step by step instructions to configure a variety of agents are available right in {{kib}}. After that, you can use the pre-built, dedicated dashboards and the APM tab to visualize the data that is sent back from the APM Agents.
* Use the `elastic` credentials to go to the Fleet area of {{kib}}. Step by step instructions to download and install Elastic Agent on your hosts are available right in {{kib}}. After that, you can manage enrolled Elastic Agents on the **Agents** tab, and the data shipped back from those Elastic Agents on the **Data streams** tab.
* Reset the APM secret token.

    ::::{important}
    Resetting the token disrupts your APM service and restarts the server. When the server restarts, you’ll need to update all of your agents with the new token.
    ::::

* Access the APM & Fleet logs and metrics.
* Stop and restart your APM & Fleet Server.
* Upgrade your APM & Fleet Server version if it is out of sync with your {{es}} cluster.
* Fully remove the APM & Fleet Server, delete it from the disk, and stop the charges.


### Upgrading to {{stack}} 8.0 [ec-upgrade-apm-stack-8]

The following APM settings have been removed in {{stack}} version 8.0. This change is only relevant to users upgrading a standalone (legacy) deployment of APM Server to {{stack}} version 8.0. Check [Add APM user settings](/solutions/observability/apm/apm-server/configure.md) for more details.

```yaml
apm-server.api_key.enabled
apm-server.api_key.limit
apm-server.ilm.*
apm-server.frontend.*
apm-server.register.*
apm-server.rum.allow_service_names
apm-server.rum.event_rate.lru_size
apm-server.rum.event_rate.limit
apm-server.rum.rate_limit
output.elasticsearch.bulk_max_size
output.elasticsearch.index
output.elasticsearch.indices
output.elasticsearch.pipeline
output.elasticsearch.pipelines
output.elasticsearch.worker
setup.*
queue.*
```


