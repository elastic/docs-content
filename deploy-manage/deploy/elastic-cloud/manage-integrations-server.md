---
navigation_title: Manage Integrations Server
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-manage-integrations-server.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Manage Integrations server in {{ech}} [ec-manage-integrations-server]

For deployments that are version 8.0 and later, you have the option to add a combined [Application Performance Monitoring (APM) Server](/solutions/observability/apm/index.md) and [Fleet Server](/reference/fleet/index.md) to your deployment. APM allows you to monitor software services and applications in real time, turning that data into documents stored in the {{es}} cluster. Fleet allows you to centrally manage Elastic Agents on many hosts.

As part of provisioning, the APM Server and Fleet Server are already configured to work with {{es}} and {{kib}}. At the end of provisioning, you are shown the secret token to configure communication between the APM Server and the backend [APM Agents](/reference/apm-agents/index.md). The APM Agents get deployed within your services and applications.

From the deployment **Integrations Server** page you can also:

* Get the URL to complete the APM agent configuration.
* Use the `elastic` credentials to go to the APM area of {{kib}}. Step by step instructions to configure a variety of agents are available right in {{kib}}. After that, you can use the pre-built, dedicated dashboards and the APM tab to visualize the data that is sent back from the APM Agents.
* Use the `elastic` credentials to go to the Fleet area of {{kib}}. Step by step instructions to download and install Elastic Agent on your hosts are available right in {{kib}}. After that, you can manage enrolled Elastic Agents on the **Agents** tab, and the data shipped back from those Elastic Agents on the **Data streams** tab.
* Access the Integrations Server logs and metrics.
* Stop and restart your Integrations Server.
* Upgrade your Integrations Server version if it is out of sync with your {{es}} cluster.
* Fully remove the Integrations Server, delete it from the disk, and stop the charges.

::::{important}
The APM secret token can no longer be reset from the {{ecloud}} UI. Check [Secret token](/solutions/observability/apm/secret-token.md) for instructions on managing a secret token. Note that resetting the token disrupts your APM service and restarts the server. When the server restarts, you’ll need to update all of your agents with the new token.
::::


## Enable Integrations Server through the API [ec-integrations-server-api-example]

This example demonstrates how to use the {{ecloud}} RESTful API to create a deployment with Integrations Server enabled.


#### Requirements [ec_requirements_2]

Integrations Server can be enabled only on new deployments, starting with {{stack}} version 8.0.

It’s possible to enable Integrations Server on an existing deployment with version 8.0 only if [APM & Fleet Server](switch-from-apm-to-integrations-server-payload.md#ec-manage-apm-and-fleet) hasn’t been previously enabled on the deployment.


#### API request example [ec_api_request_example_2]

Run this example API request to create a deployment with Integrations Server:


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
        "region": "eu-west-1",
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
              "instance_configuration_id": "aws.es.datahot.i3",
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
              "instance_configuration_id": "aws.es.datawarm.d3",
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
              "instance_configuration_id": "aws.es.datacold.d3",
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
              "instance_configuration_id": "aws.es.datafrozen.i3en",
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
              "instance_configuration_id": "aws.es.master.c5d",
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
              "instance_configuration_id": "aws.es.coordinating.m5d",
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
              "instance_configuration_id": "aws.es.ml.m5d",
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
            "id": "aws-storage-optimized"
          }
        },
        "ref_id": "main-elasticsearch"
      }
    ],
    "kibana": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "eu-west-1",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "aws.kibana.c5d",
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
    ],
    "integrations_server": [
      {
        "elasticsearch_cluster_ref_id": "main-elasticsearch",
        "region": "eu-west-1",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "aws.integrations_server.c5d",
              "zone_count": 1,
              "size": {
                "resource": "memory",
                "value": 1024
              }
            }
          ],
          "integrations_server": {
            "version": "8.0.0"
          }
        },
        "ref_id": "main-integrations_server"
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


