---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-ce-add-support-for-integrations-server.html
---

# Updating custom templates to support Integrations Server [ece-ce-add-support-for-integrations-server]

Custom deployment templates should be updated in order to support Integrations Server. While system-owned deployment templates are updated automatically during the ECE upgrade process, user-created deployment templates require a manual update.

To manually update your custom deployment templates to support Integrations Server:

1. Obtain a list of all existing deployment templates by sending the following `GET` request, and take note of the `id` of the template you wish to update.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://${COORDINATOR_HOST}:12443/api/v1/deployments/templates?region=ece-region
    ```

2. Copy the template you’d like to update and add an `integrations_server` entry under the `deployment_template.resources` section of the JSON. The result should look like the following:

    ```sh
    "integrations_server" : [
      {
        "ref_id" : "integrations_server-ref-id",
        "elasticsearch_cluster_ref_id" : "main-elasticsearch",
        "region" : "ece-region",
        "plan" : {
          "cluster_topology" : [
            {
              "instance_configuration_id" : "integrations.server",
              "size" : {
                "value" : 512,
                "resource" : "memory"
              },
              "zone_count" : 1
            }
          ],
          "integrations_server" : {

          }
        }
      }
    ]
    ```


Send a `PUT` request with the updated template in the payload to replace the original template with the new one. Remember that:

* The following request is just an example; other resources in the request payload should remain unchanged (they have been truncated in the example).
* You need to replace `{{template_id}}` in the URL with the `id` that you collected in Step 1.

Refer to [set deployment template API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-deployment-template-v2) for more details.

::::{dropdown} Update template API request example
```sh
curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates/{template_id}?region=ece-region -H 'content-type: application/json' -d '
{
  "name": "ECE Custom Template",
  "description": "ECE custom template with added Integrations Server",
  "deployment_template": {
    "resources": {
      "elasticsearch": [...],
      "kibana": [...],
      "apm": [...],
      "enterprise_search": [...],
      "integrations_server": [
        {
            "ref_id": "integrations_server-ref-id",
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
                "integrations_server": {}
        }
      ]
    }
  },
  "system_owned": false
}'
```

::::


After the template is updated, you can start [creating new deployments](create-deployment.md).

