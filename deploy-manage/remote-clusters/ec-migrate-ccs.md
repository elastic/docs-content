---
navigation_title: Migrate from the CCS deployment template
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-ccs.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Migrate from the legacy cross-cluster search deployment template in {{ech}} [ec-migrate-ccs]

The legacy cross-cluster search deployment template has been removed from the {{ecloud}} Console. You no longer need a dedicated template to search across deployments. Instead, you can now use any template to [configure remote clusters](ec-enable-ccs.md) and search across them. Existing deployments created using this template are not affected, but they are required to migrate to another template before upgrading to {{stack}} 8.x.

There are two different approaches to do this migration:

* [Migrate using the API](#ec-migrate-ccs-deployment-using-api)
* [Migrate using a snapshot](#ec-migrate-ccs-deployment-using-snapshot)


## Use the API to migrate deployments that use the cross-cluster search template [ec-migrate-ccs-deployment-using-api]

You can use a PUT request to update your deployment, changing both the deployment template ID and the instances required by the new template.

1. First, choose the new template you want to use and obtain its ID. This template ID can be obtained from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) **Create Deployment** page by selecting **Equivalent API request** and inspecting the result for the field `deployment_template`. For example, we are going to use the "Storage optimized" deployment template, and in our GCP region the id is `gcp-storage-optimized-v5`.

   You can also find the template in the [list of templates available for each region](cloud://reference/cloud-hosted/ec-regions-templates-instances.md).

   :::{image} /deploy-manage/images/cloud-ec-migrate-deployment-template(2).png
   :alt: Deployment Template ID
   :screenshot:
   :::

2. Make a request to update your deployment with two changes:

    1. Under `deployment_template`, set `id` to the value obtained in the previous step.
    2. Change the cluster topology to match the new template that your deployment will migrate to.


    ```sh
    curl -H 'Content-Type: application/json' -X PUT -H "Authorization: ApiKey $EC_API_KEY" https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID -d "{
      "resources": {
        "integrations_server": [
          {
            "elasticsearch_cluster_ref_id": "main-elasticsearch",
            "region": "gcp-us-central1",
            "plan": {
              "cluster_topology": [
                {
                  "instance_configuration_id": "gcp.integrationsserver.n2.68x32x45.2",
                  "zone_count": 1,
                  "size": {
                    "resource": "memory",
                    "value": 1024
                  }
                }
              ],
              "integrations_server": {
                "version": "8.7.1"
              }
            },
            "ref_id": "main-integrations_server"
          }
        ],
        "elasticsearch": [
          {
            "region": "gcp-us-central1",
            "settings": {
              "dedicated_masters_threshold": 6
            },
            "plan": {
              "cluster_topology": [
                {
                  "zone_count": 2,
                  "elasticsearch": {
                    "node_attributes": {
                      "data": "hot"
                    }
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
                  "instance_configuration_id": "gcp.es.master.n2.68x32x45.2",
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
                  "instance_configuration_id": "gcp.es.coordinating.n2.68x16x45.2",
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
                "version": "8.7.1",
                "enabled_built_in_plugins": []
              },
              "deployment_template": {
                "id": "gcp-storage-optimized-v5"
              }
            },
            "ref_id": "main-elasticsearch"
          }
        ],
        "enterprise_search": [
          {
            "elasticsearch_cluster_ref_id": "main-elasticsearch",
            "region": "gcp-us-central1",
            "plan": {
              "cluster_topology": [
                {
                  "node_type": {
                    "connector": true,
                    "appserver": true,
                    "worker": true
                  },
                  "instance_configuration_id": "gcp.enterprisesearch.n2.68x32x45",
                  "zone_count": 1,
                  "size": {
                    "resource": "memory",
                    "value": 2048
                  }
                }
              ],
              "enterprise_search": {
                "version": "8.7.1"
              }
            },
            "ref_id": "main-enterprise_search"
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
                  "zone_count": 1,
                  "size": {
                    "resource": "memory",
                    "value": 1024
                  }
                }
              ],
              "kibana": {
                "version": "8.7.1"
              }
            },
            "ref_id": "main-kibana"
          }
        ]
      },
      "settings": {
        "autoscaling_enabled": false
      },
      "name": "My deployment",
      "metadata": {
        "system_owned": false
      }
    }"
    ```

`DEPLOYMENT_ID`
:   The ID of your deployment, as shown in the Cloud UI or obtained through the API.

`REGION`
:   The region of your deployment, as shown in the Cloud UI or obtained through the API.

Note that the `ref_id` and version numbers for your resources may not be the same as shown in this example. Make sure to use the ones your deployment has.


## Use a snapshot to migrate deployments that use the cross-cluster search deployment template [ec-migrate-ccs-deployment-using-snapshot]

You can make this change in the user [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body). The only drawback of this method is that it changes the URL used to access the {{es}} cluster and {{kib}}.

1. From the deployment menu, open the **Snapshots** page and click **Take Snapshot now**. Wait for the snapshot to finish.
2. From the main **Hosted deployments** page, click **Create deployment**. Next to **Settings** toggle on **Restore snapshot data**, and then select your deployment and the snapshot that you created.

    :::{image} /deploy-manage/images/cloud-ec-create-from-snapshot-updated.png
    :alt: Create a Deployment using a snapshot
    :screenshot:
    :::


