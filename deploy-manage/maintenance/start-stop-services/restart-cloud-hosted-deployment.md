---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-restart-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-api-deployment-other.html
applies_to:
  deployment:
     ess:
---

# Restart an {{ech}} deployment

You can restart your deployment through the deployment overview UI or by using an API.

## Restart your deployment through the deployment overview [ec-restart-deployment]

You might need to restart your deployment while addressing issues, like cycling garbage collection.

On the deployment overview, from the **Action** drop-down menu select **Restart {{es}}**.

You can choose to restart without downtime or you can restart all nodes simultaneously.

Note that if you are looking to restart {{es}} to clear out [deployment activity](../../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) plan failures, you may instead run a [no-op plan](../../../troubleshoot/monitoring/deployment-health-warnings.md) to re-synchronize the last successful configuration settings between {{ech}} and {{es}}.

## Restart an {{es}} resource by using an API [ec_restart_an_elasticsearch_resource]

Restart an Elasticsearch resource by calling the following API request:

```sh
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/$RESOURCE_KIND/$REF_ID/_restart"
```

`DEPLOYMENT_ID`  The ID of the deployment returned in the response for `POST /deployments`

`RESOURCE_KIND`  Type of the deployment resource. Depending on the version to be deployed, it can be `elasticsearch`, `kibana`, `apm`, `integrations_server`, `appsearch` or `enterprise_search`

`REF_ID`  Name given to each resource type in the attribute `ref_id`. `main-elasticsearch` in the preceding example

## Shut down an {{ech}} deployment [ec_shut_down_a_elasticsearch_service_deployment]

Shut down an {{ech}} deployment by calling the following API request:

```sh
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/_shutdown"
```

`DEPLOYMENT_ID`  The ID of the deployment returned in the response for `POST /deployments`
