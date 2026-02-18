---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-claim-traffic-filter-link-id-through-the-api.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Claim private connection ownership

This example demonstrates how to use the {{ecloud}} RESTful API to claim different types of private connection IDs (AWS PrivateLink, Azure Private Link, and GCP Private Service Connect). We cover the following examples:

* [Claim a private connection ID](#claim-private-connection-id)

    * [AWS PrivateLink](#ec-claim-aws-privatelink)
    * [Azure Private Link](#ec-claim-azure-private-link)
    * [GCP Private Service Connect](#ec-claim-gcp-private-service-connect)

* [List claimed private connection IDs](#list-claimed-private-connection-ids)
* [Unclaim a private connection ID](#unclaim-private-connection-id)

    * [AWS PrivateLink](#ec-unclaim-aws-privatelink)
    * [Azure Private Link](#ec-unclaim-azure-private-link)
    * [GCP Private Service Connect](#ec-unclaim-gcp-private-service-connect)



## Claim a private connection ID [claim-private-connection-id] 


### AWS PrivateLink [ec-claim-aws-privatelink] 

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_claim \
-d '
{
  "region": "eu-west-1",
  "link_id": "$VPC_ENDPOINT_ID"
}
'
```


### GCP Private Service Connect [ec-claim-gcp-private-service-connect] 

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_claim \
-d '
{
  "region": "gcp-us-central1",
  "link_id": "$PSC_CONNECTION_ID"
}
'
```


### Azure Private Link [ec-claim-azure-private-link] 

In the case of Azure Private Link, two pieces of information are needed.

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_claim \
-d '
{
  "region": "azure-eastus2",
  "azure_endpoint_name": "$AZURE_ENDPOINT_NAME",
  "azure_endpoint_guid": "$AZURE_ENDPOINT_GUID"
}
'
```


## List claimed private connection IDs [list-claimed-private-connection-ids] 

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids \
```


## Unclaim a private connection ID [unclaim-private-connection-id] 


### AWS PrivateLink [ec-unclaim-aws-privatelink] 

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_unclaim \
-d '
{
  "region": "eu-west-1",
  "link_id": "$VPC_ENDPOINT_ID"
}
'
```


### GCP Private Service Connect [ec-unclaim-gcp-private-service-connect] 

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_unclaim \
-d '
{
  "region": "gcp-us-central1",
  "link_id": "$PSC_CONNECTION_ID"
}
'
```


### Azure Private Link [ec-unclaim-azure-private-link]

In the case of Azure Private Link, two pieces of information are needed.

```sh
curl \
-H "Authorization: ApiKey $API_KEY" \
-H 'content-type: application/json' \
https://api.elastic-cloud.com/api/v1/deployments/traffic-filter/link-ids/_unclaim \
-d '
{
  "region": "azure-eastus2",
  "azure_endpoint_name": "$AZURE_ENDPOINT_NAME",
  "azure_endpoint_guid": "$AZURE_ENDPOINT_GUID"
}
'
```

