---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Firewalls blocking Elastic Agent
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Troubleshoot firewalls blocking {{agent}}

If you suspect that a corporate firewall is hindering {{agent}}, the following subsections explain how to test each component of the connection and implement an appropriate solution. 

:::{tip}
Run the following tests within the context of your execution environment. That is, if your chosen installation method is Kubernetes, run the commands from within the pod; for Docker, run the commands from within the container, and so on. 
:::

There are three main components of {{agent}}'s connection with your system:

1. {{agent}} registers your cluster with {{ecloud}}
2. {{agent}} connects to your cluster
3. {{agent}} sends metrics from your cluster to {{ecloud}}

## 1. Test the registration of your cluster with {{ecloud}}

If there is an issue with the first component, the agent will stop working and your logs might look like: 

```sh
... failed to register Cloud Connected Mode: ... Post \"https://api.elastic-cloud.com/api/v1/cloud-connected/clusters\": ...
```

To test if your organization is not allowing the agent to register your cluster with {{ecloud}}, run the following command:

```json
curl -XPOST -i \
https://api.elastic-cloud.com/api/v1/cloud-connected/clusters \
-H 'Content-Type: application/json' \
-d '{"self_managed_cluster": {"id": "my-cluster-uuid", "name": "my-cluster-name", "version": "9.1.0"}, "license": {"uid": "my-license-id", "type": "basic"}}'
```

The command should return an HTTP 401 response similar to: 

```json
      {"UnauthorizedMessages":["Invalid credential headers"],"Cause":null}
```
If you do not receive a similar response, configure your HTTP proxy to allow it to reach the URL (with headers and a JSON body):

```json
      POST https://api.elastic-cloud.com/api/v1/cloud-connected/clusters
```
:::{note}
If you are using Docker, you may need to complete this configuration directly via the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables.
:::

If there is an issue with the second component, {{agent}} cannot connect to your cluster. To test if your organization is not allowing this connection, run the following command depending on your chosen authentication method:

:::::{tab-set}
:group: api-key-or-basic

::::{tab-item} API key
:sync: api-key

```json
curl -XGET -i $AUTOOPS_ES_URL \
-H "Authorization: ApiKey $AUTOOPS_ES_API_KEY"
```
::::

::::{tab-item} Basic
:sync: basic

```json
curl -XGET -i $AUTOOPS_ES_URL \
-u $AUTOOPS_ES_USERNAME
```
::::

:::::

The command should return a response similar to:

```json
{
"name" : "1c72f00a6195",
"cluster_name" : "my-ccm-cluster",
"cluster_uuid" : "2O_EjO6kTR6AEVYwL5fPEw",
"version" : {
"number" : "9.1.3",
"build_flavor" : "default",
"build_type" : "docker",
"build_hash" : "0c781091a2f57de895a73a1391ff8426c0153c8d",
"build_date" : "2025-08-24T22:05:04.526302670Z",
"build_snapshot" : false,
"lucene_version" : "10.2.2",
"minimum_wire_compatibility_version" : "8.19.0",
"minimum_index_compatibility_version" : "8.0.0"
},
"tagline" : "You Know, for Search"
}
```

If you do not receive a similar response, your system will return an error indicating one or more reasons for failure as outlined in the following table. Use the corresponding proposed solution to fix the issue.

| Reason for failure | Proposed solution |
| :--- | :--- |
| The {{es}} endpoint URL you specified is incorrect/not reachable | - Make sure you are using `http` or `https` correctly. <br> - Make sure you are providing the correct port. The default port is **9200**. <br> - If you have verified that the URL is correct, your network team may need to open the firewall to allow-list this URL. |
| Your API key is incorrect | - Recheck for typos. <br> - If your cluster is on versions 9.1.0 through 9.1.3, ensure that you have the base64-decoded version of the key by running the following command: <br><br> `echo $AUTOOPS_ES_API_KEY | base64 -d` <br><br> If your key has a colon (:), it is not base64 encoded. If your key has an equal sign (=), it is base64 coded. <br> For versions 9.1.4 and above, both formats will work.|
| Your username and/or password are incorrect | - Recheck for typos. <br> - Ensure that your provided user has the [necessary privileges](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#configure-agent). We do not recommend providing a privileged superuser like `elastic` for this purpose.|
| You are providing both the API key and username/password | Choose one type of authentication only. |
| A proxy is blocking communication with your {{es}} cluster | You may have to configure `NO_PROXY`. |
| You are using a custom SSL/TLS configuration with {{es}} | Disable SSL/TLS verification so that your system trusts all certificates. We do not recommend disabling verification in production environments. <br><br> If you are using API key authentication, run the following command: <br><br>`curl -XGET --insecure -i $AUTOOPS_ES_URL \ -H "Authorization: ApiKey $AUTOOPS_ES_API_KEY"`. <br><br> If you are using username/password authentication, run the following command: <br><br> `curl -XGET --insecure -i $AUTOOPS_ES_URL \ -u $AUTOOPS_ES_USERNAME` <br><br> If the issue is resolved, you need to configure your custom SSL/TLS settings with {{agent}}. If the issue persists, contact [Elastic support](https://support.elastic.co/).| 
| You are connecting a local development cluster using Docker without specifying `--network host` | - Make sure you are following all the steps to [connect your local development cluster to AutoOps](/deploy-manage/monitor/autoops/cc-connect-local-dev-to-autoops.md#connect-your-local-development-cluster-to-autoops). <br> - In the [Install agent](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#install-agent) step, make sure you are replacing `docker run -d \` with `docker run -d --network host \`. |


If there is an issue with the third component, the agent will attempt to establish the connection and your logs might look like: 
    
```sh
... Exporting failed. Dropping data. ... no more retries left: failed to make an HTTP request: Post \"https://otel-collector.auto-ops.eu-west-1.aws.cloud.elastic.co:4318/v1/logs\": ...
```
    
To test if your organization is not allowing the agent to send metrics from your cluster to {{ecloud}}, run the following command. We will use AWS eu-west-1 as the CSP region, but you should replace it with your chosen CSP region before running the command.

```json
curl -XPOST -i \
https://otel-collector.auto-ops.eu-west-1.aws.cloud.elastic.co:4318/v1/logs \
-H 'Content-Type: application/json'

```
The command should return an HTTP 401 response similar to: 

```json
  {"code":16,"message":"no auth provided"}
```

If you do not receive a similar response, configure your HTTP proxy to allow it to reach the URL (with headers and an arbitrary body):

```json
  POST https://otel-collector.auto-ops.${REGION}.${CSP}.cloud.elastic.co:4318/v1/logs
```
:::{note}
If you are using Docker, you may need to complete this configuration directly via the `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables.
:::