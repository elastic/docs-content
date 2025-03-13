---
applies_to:
  deployment:
    ece: ga
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-through-the-api.html
---

# Manage traffic filtering through the ECE API [ece-traffic-filtering-through-the-api]

This example demonstrates how to use the Elastic Cloud Enterprise RESTful API to manage different types of traffic filters. We cover the following examples:

* [Create a traffic filter rule set](ece-traffic-filtering-through-the-api.md#ece-create-a-traffic-filter-rule-set)

    * [IP traffic filter ingress rule set](ece-traffic-filtering-through-the-api.md#ece-ip-traffic-filters-ingress-rule-set)

* [Update a traffic filter rule set](ece-traffic-filtering-through-the-api.md#ece-update-a-traffic-filter-rule-set)
* [Associate a rule set with a deployment](ece-traffic-filtering-through-the-api.md#ece-associate-rule-set-with-a-deployment)
* [Delete a rule set association with a deployment](ece-traffic-filtering-through-the-api.md#ece-delete-rule-set-association-with-a-deployment)
* [Delete a traffic filter rule set](ece-traffic-filtering-through-the-api.md#ece-delete-a-rule-set)

Read through the main [Traffic Filtering](traffic-filtering.md) page to learn about the general concepts behind filtering access to your Elastic Cloud Enterprise deployments.


## Create a traffic filter rule set [ece-create-a-traffic-filter-rule-set] 


### IP traffic filter ingress rule set [ece-ip-traffic-filters-ingress-rule-set] 

Send a request like the following to create an IP traffic filter ingress rule set:

```sh
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

If the request is successful, a response containing a $RULESET_ID is returned. $RULESET_ID is required to update or delete the rule set itself, or it can be used to associate the rule set to a deployment.

```sh
{
  "id" : "5470a0010ebf437bb9294ea9fcba0ba0"
}
```






## Update a traffic filter rule set [ece-update-a-traffic-filter-rule-set] 

Send a request like the following to update an IP traffic filter ingress rule set:

```sh
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


## Associate a rule set with a deployment [ece-associate-rule-set-with-a-deployment] 

Send a request like the following to associate a rule set with a deployment:

```sh
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


## Delete a rule set association with a deployment [ece-delete-rule-set-association-with-a-deployment] 

Send a request like the following to delete a rule set association with a deployment:

```sh
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID/associations/deployment/$DEPLOYMENT_ID \
```


## Delete a traffic filter rule set [ece-delete-a-rule-set] 

Send a request like the following to delete a traffic filter rule set:

```sh
curl -XDELETE \
-H "Authorization: ApiKey $API_KEY" \
https://$COORDINATOR_HOST:12443/api/v1/deployments/traffic-filter/rulesets/$RULESET_ID \
```

