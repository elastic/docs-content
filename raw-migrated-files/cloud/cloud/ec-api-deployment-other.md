# Other deployment operations [ec-api-deployment-other]


## Restart an Elasticsearch resource [ec_restart_an_elasticsearch_resource] 

Restart an Elasticsearch resource.

```sh
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/$RESOURCE_KIND/$REF_ID/_restart"
```

`DEPLOYMENT_ID`  The ID of the deployment returned in the response for `POST /deployments`

`RESOURCE_KIND`  Type of the deployment resource. Depending on the version to be deployed, it can be `elasticsearch`, `kibana`, `apm`, `integrations_server`, `appsearch` or `enterprise_search`

`REF_ID`  Name given to each resource type in the attribute `ref_id`. `main-elasticsearch` in the preceding example


## Shut down a Elasticsearch Service deployment [ec_shut_down_a_elasticsearch_service_deployment] 

Shut down a Elasticsearch Service deployment.

```sh
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/$DEPLOYMENT_ID/_shutdown"
```

`DEPLOYMENT_ID`  The ID of the deployment returned in the response for `POST /deployments`

