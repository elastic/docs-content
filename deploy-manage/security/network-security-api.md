---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-through-the-api.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-through-the-api.html
applies_to:
  deployment:
    ess:
    ece:
  serverless:
products:
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-serverless
navigation_title: Through the API
---

# Manage network security through the API

This example demonstrates how to use the {{ecloud}} RESTful API, {{ece}} RESTful API, or {{serverless-full}} RESTful API or to manage different types of network security policies and rules. 

We cover the following examples:

* [Create an IP filter policy or IP filtering rule set](#create-ip-filter-policy)

  * [Ingress](#ip-filter-policy-ingress)
  * [Egress](#ip-filter-policy-egress) {applies_to}`ess: beta`
  
* [Create a private connection policy](#private-connection) {applies_to}`ess:`
  * [AWS Privatelink](#private-connection-policy-aws)
  * [Azure Private Link](#private-connection-policy-azure)
  * [GCP Private Service Connect](#private-connection-policy-gcp)

* [Update a policy or rule set](#update-policy-rs)
* [Associate a policy or rule set with a project or deployment](#associate-policy-rs-with-deployment)
* [Remove a policy or rule set from a project or deployment](#delete-policy-rs-association-with-deployment)
* [Delete a policy or rule set](#delete-policy-rs)

Refer to [](network-security.md) to learn more about network security across all deployment types.

:::{tip}
Policies in {{ecloud}} are the equivalent of rule sets in {{ece}} and the {{ecloud}} API.
:::

## API reference

To learn more about these endpoints, refer to the reference for your deployment type:

* [{{ecloud}} API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deploymentstrafficfilter)
* [{{ece}} API](https://www.elastic.co/docs/api/doc/cloud-enterprise/group/endpoint-deploymentstrafficfilter)


## Terminology in the {{ecloud}} console and APIs
```{applies_to}
deployment:
  ess:
serverless:
```

In {{ecloud}}, terminology related to network security has changed to more accurately reflect functionality. Terminology in the related APIs has not yet been updated.

| {{ecloud}} concept | API terminology | 
| --- | --- | 
| Network security | Traffic filters | 
| Network security policy | Traffic filter |
| IP filter policy | IP filtering rule set | 
| IP filter source | IP filter rule | 
| Private connection policy | Private link traffic filter |
| VPC filter | Private link filter rule |

## Create an IP filter policy or IP filtering rule set [create-ip-filter-policy]

IP filter policies in {{ecloud}} are the equivalent of IP filtering rule sets in {{ece}}.

Both policies and rule sets consist of multiple unique entries, each representing a source IP address or CIDR range. In {{ecloud}}, these entries are referred to as sources. In {{ece}} and the {{ecloud}} API, these entries are referred to as rules.

### Ingress [ip-filter-policy-ingress]

Send a request like the following to create an IP filter ingress policy or rule set:

::::{applies-switch}

:::{applies-item} ess:

```json
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "My ingress IP filter policy",
  "region": "azure-japaneast", <1>
  "description": "",
  "type": "ip", <2>
  "rules": [
    {
      "description": "Allow inbound traffic from IP address 192.168.131.0",
      "source": "192.168.131.0"
    },
    {
      "description": "Allow inbound traffic within CIDR block 192.168.132.6/22",
      "source": "192.168.132.6/22"
    }
  ],
  "include_by_default": false
}
'
```

1. The region is always the same region as the deployment you want to associate with an IP filter policy. For details, check the [list of available regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md).
2. The type of policy. In the JSON object, we use `ip` for IP filter policies. Currently, we support `ip`, `egress_firewall`, `vpce` (AWS Private Link), `azure_private_endpoint` and `gcp_private_service_connect_endpoint`. These are described in further detail below.
:::
:::{applies-item} serverless:

```json
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/serverless/traffic-filters \
-d '
{
  "name": "My ingress IP filter policy",
  "region": "ap-southeast-1" <1>
  "description": "",
  "type": "ip", <2>
  "rules": [
    {
      "description": "Allow inbound traffic from IP address 192.168.131.0",
      "source": "192.168.131.0"
    },
    {
      "description": "Allow inbound traffic within CIDR block 192.168.132.6/22",
      "source": "192.168.132.6/22"
    }
  ],
  "include_by_default": false
}
'
```

1. The region is always the same region as the project you want to associate with an IP filter policy. For details, check the [list of available regions](/deploy-manage/deploy/elastic-cloud/regions.md).

2. The type of policy. In the JSON object, we use `ip` for IP filter policies. Currently, only `ip` is supported.
:::
:::{applies-item} ece:

```json
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "My IP filtering Ingress Rule Set",
  "region": "ece-region",
  "description": "",
  "type": "ip",
  "rules": [
    {
      "description": "Allow inbound traffic from IP address 192.168.131.0",
      "source": "192.168.131.0"
    },
    {
      "description": "Allow inbound traffic within CIDR block 192.168.132.6/22",
      "source": "192.168.132.6/22"
    }
  ],
  "include_by_default": false
}
'
```
:::
::::

If the request is successful, a response containing an ID for the policy or rule set is returned. This ID is required to update or delete the policy or rule set itself, or it can be used to associate the policy or rule set to a deployment or project. It is referred to as `$POLICY_ID` or `$RULESET_ID` in the following examples.

```json
{
  "id" : "5470a0010ebf437bb9294ea9fcba0ba0"
}
```


### Egress [ip-filter-policy-egress]
```{applies_to}
deployment:
  ess: beta
```

Send a request like the following to create an IP filter ingress policy:

```json
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "My IP filtering Egress Rule Set",
  "region": "azure-japaneast",
  "description": "",
  "type": "egress_firewall",
  "rules": [
    {
       "description": "Allow outbound traffic to IP address 192.168.131.0",
       "egress_rule":
       {
           "target": "192.168.131.0",
           "protocol": "all" <1>
       }
    },
    {
       "description": "Allow outbound traffic to CIDR block 192.168.132.6/22",
       "egress_rule":
       {
           "target": "192.168.132.6/22",
           "protocol": "all"
       }
    },
  ],
  "include_by_default": false
}
'
```

1. This can be `udp`, `tcp`, or `all`.


## Create a private connection policy [private-connection]
```{applies_to}
deployment:
  ess:
```

Learn how to create a private connection policy using the {{ecloud}} API. In the API, a VPC filter in a private connection policy is referred to as a rule.

:::{tip}
Private connection policies are optional for AWS PrivateLink and GCP Private Service Connect. After the VPC endpoint and DNS record are created, private connectivity is established.

Creating a private connection policy and associating it with your deployments allows you to do the following:

* Record that you've established private connectivity between the cloud service provider and Elastic in the applicable region.
* [View a list of the resources](network-security-policies.md#protected-resources-overview) that have private connections applied.
* Filter traffic to your deployment using VPC filters.

A private connection policy is required to establish a private connection with Azure Private Link.
:::


### AWS Privatelink [private-connection-policy-aws]

Send a request like the following to create an AWS PrivateLink private connection policy:

```json
curl -XPOST \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "AWS Private Link private connection policy",
  "region": "ap-northeast-1",
  "description": "",
  "type": "vpce",
  "rules": [
    {
      "source": "vpce-00000000000" <1>
    }
  ],
  "include_by_default": false
}
'
```

1. To learn how to find the value for `source` for type `vpce`, refer to [Find your VPC endpoint ID](private-connectivity-aws.md#ec-find-your-endpoint). This setting is supported only in AWS regions.


### Azure Private Link [private-connection-policy-azure]

Send a request like the following to create an Azure Private Link private connection policy:

```json
curl -XPOST \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "Azure Private Link private connection policy",
  "region": "azure-japaneast",
  "description": "",
  "type": "azure_private_endpoint",
  "rules": [
    {
      "azure_endpoint_name": "azure-demo", 
      "azure_endpoint_guid": "7c0f05e4-e32b-4b10-a246-7b77f7dcc63c" <1>
    }
  ],
  "include_by_default": false
}
'
```

1. To learn how to find the value for `azure_endpoint_name` and `azure_endpoint_guid` for type `azure_private_endpoint`, refer to [Find your private endpoint resource name](private-connectivity-azure.md#ec-find-your-resource-name) and [Find your private endpoint resource ID](private-connectivity-azure.md#ec-find-your-resource-id). This setting is supported only in Azure regions.


### GCP Private Service Connect [private-connection-policy-gcp]

Send a request like the following to create a GCP Private Service Connect private connection policy:

```json
curl -XPOST \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets \
-d '
{
  "name": "GCP Private Service Connect private connection policy",
  "region": "gcp-asia-northeast1",
  "description": "",
  "type": "gcp_private_service_connect_endpoint",
  "rules": [
    {
      "source": "18446744072646845332" <1>
    }
  ],
  "include_by_default": false
}
'
```

1. To find the value for `source` for type `gcp_private_service_connect_endpoint`, check [Find your Private Service Connect connection ID](private-connectivity-gcp.md#ec-find-your-psc-connection-id). This setting is supported only in GCP regions.


## Update a policy or rule set [update-policy-rs]

Send a request like the following to update an IP filter ingress policy or rule set.

Policies in {{ecloud}} are the equivalent of rule sets in {{ece}}.

::::{applies-switch}

:::{applies-item} ess:

```json
curl -XPUT \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets/$POLICY_ID \
-d '
{
  "name": "My ingress IP filter policy",
  "region": "azure-japaneast",
  "description": "",
  "type": "ip",
  "rules": [
    {
      "description": "Allow inbound traffic from IP address 192.168.131.0",
      "source": "192.168.131.0"
    },
    {
      "description": "Allow inbound traffic within CIDR block 192.168.132.6/22",
      "source": "192.168.132.6/22"
    }
  ],
  "include_by_default": true
}
'
```
:::
:::{applies-item} serverless:

```json
curl -X PATCH \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/serverless/traffic-filters/$POLICY_ID \
-d '
{
  "description": "Updated description of the policy",
  "rules": [
    {
      "description": "Updated description of the source",
      "source": "192.168.131.0"
    },
  ],
  "include_by_default": true
}
'
```
:::
:::{applies-item} ece:

```json
curl -XPUT \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID \
-d '
{
  "name": "My IP filtering Ingress Rule Set",
  "region": "ece-region",
  "description": "",
  "type": "ip",
  "rules": [
    {
      "description": "Allow inbound traffic from IP address 192.168.131.0",
      "source": "192.168.131.0"
    },
    {
      "description": "Allow inbound traffic within CIDR block 192.168.132.6/22",
      "source": "192.168.132.6/22"
    }
  ],
  "include_by_default": true
}
'
```
:::
::::


## Associate a policy or rule set with a project or deployment [associate-policy-rs-with-deployment]

Send a request like the following to associate a policy or rule set with a project or deployment.

Policies in {{ecloud}} are the equivalent of rule sets in {{ece}}.

:::::{applies-switch}

::::{applies-item} ess:

```json
curl -XPOST \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets/$POLICY_ID/associations \
-d '
{
   "entity_type" : "deployment",
   "id" : "'"$DEPLOYMENT_ID"'"
}
'
```
::::

::::{applies-item} serverless:

To associate a network security policy to a project, you must update the project object.

```json
curl -X PATCH \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/admin/serverless/projects/elasticsearch \ <1>
-d '
{
  "traffic_filters": [
    {
      "id": "$POLICY_ID"
    },
    {
      "id": "$ANOTHER_POLICY_ID"
    }
  ]
}
'
```
1. Pass the project type in the endpoint URL: either `elasticsearch`, `observability`, or `security`.

:::{warning}
When adding, updating, or removing a policy association, you must provide a complete list of policies to be associated with the project in the `PATCH` request body. Any policies not included in this list will be removed from the project. 
:::
::::

::::{applies-item} ece:

```json
curl -XPOST \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID/associations \
-d '
{
   "entity_type" : "deployment",
   "id" : "'"$DEPLOYMENT_ID"'"
}
'
```
::::
:::::


## Remove a policy or rule set from a project or deployment [delete-policy-rs-association-with-deployment]

Send a request like the following to remove a policy or rule set from a project or deployment.

Policies in {{ecloud}} are the equivalent of rule sets in {{ece}}.

::::{applies-switch}

:::{applies-item} ess:

```json
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets/$POLICY_ID/associations/deployment/$DEPLOYMENT_ID \
```
:::

:::{applies-item} serverless:

To remove a network security policy from a project, you must update the project object. Pass a complete list of policies in the `PATCH` request body, excluding the policy that you want to remove from the list.

```json
curl -X PATCH \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/admin/serverless/projects/elasticsearch \ <1>
-d '
{
  "traffic_filters": [
    {
      "id": "$REMAINING_POLICY_ID" <2>
    }
  ]
}
'
```
1. Pass the project type in the endpoint URL: either `elasticsearch`, `observability`, or `security`.
2. `$POLICY_ID`, the policy that you want to remove, is not included in the list.
:::
:::

:::{applies-item} ece:

```json
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID/associations/deployment/$DEPLOYMENT_ID \
```
:::
::::


## Delete a policy or rule set [delete-policy-rs]

Send a request like the following to delete a policy or rule set.

Policies in {{ecloud}} are the equivalent of rule sets in {{ece}}.

::::{applies-switch}

:::{applies-item} ess:

```json
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/rulesets/$POLICY_ID \
```
:::
:::{applies-item} serverless:

```json
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
https://api.elastic-cloud.com/api/v1/serverless/traffic-filters/$POLICY_ID \
```
:::
:::{applies-item} ece:

```json
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID \
```
:::
::::