---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-static-ips.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# {{ecloud}} Static IPs [ec-static-ips]

{{ecloud}} provides a range of static IP addresses that enable you to allow or deny IP ranges. There are two types of static IP addresses, [ingress](#ec-ingress) and [egress](#ec-egress), and they each have their own set of use cases. In general, static IPs can be used to introduce network controls (for example, firewall rules) for traffic that goes to and from {{ecloud}} deployments over the Internet. Use of static IPs is not applicable to private cloud service provider connections (for example, AWS/Azure PrivateLink, GCP Private Service Connect). 

Static IP addresses are [subject to change](#ec-warning), and not all [cloud provider regions](#ec-regions) are currently fully supported for ingress and egress static IPs. For this reason, we generally do not recommend that you use firewall rules to allow or restrict certain IP ranges. Consider using [private connectivity](/deploy-manage/security/private-connectivity.md) for deployment endpoints on {{ech}}. However, in situations where using private connectivity services do not meet requirements (for example, secure traffic **from** {{ecloud}}), static IP ranges can be used.


## Ingress Static IPs: Traffic to {{ecloud}} [ec-ingress] 

Suitable usage of ingress static IPs to introduce network controls:

* All traffic **towards {{ecloud}} deployments** from the public Internet, your private cloud network over the public Internet, or your on-premises network over the public Internet (e.g. {{es}} traffic, {{kib}} traffic, etc) uses Ingress Static IPs as network destination

Not suitable usage of ingress static IPs to introduce network controls:

* Traffic over private cloud service provider connections (e.g. AWS Privatelink, GCP Private Service Connect, Azure Private Link)
* Traffic to the [Cloud Console](http://cloud.elastic.co)
* Traffic to non {{ecloud}} websites and services hosted by Elastic (e.g. www.elastic.co)


## Egress Static IPs: Traffic From {{ecloud}} [ec-egress] 

Suitable usage of egress static IPs to introduce network controls:

* Traffic **from {{ecloud}} deployments** towards the public Internet, your private cloud network over the public Internet, or your on-premises network over the public Internet (e.g. custom Slack alerts, Email alerts, {{kib}} alerts, etc.) uses Egress Static IPs as network source
* Cross-cluster replication/cross-cluster search traffic **from {{ecloud}} deployments** towards on-premises {{ece}} deployments protected by on-premises firewalls or {{ece}} IP filters

Not suitable usage of egress static IPs to introduce network controls:

* Snapshot traffic that stays within the same cloud provider and regional boundaries (e.g. an {{ecloud}} deployment hosted in aws-us-east-1 using an S3 bucket also hosted in aws-us-east-1 as a snapshot repository)


## Supported Regions [ec-regions] 

::::{dropdown} AWS
| Region | Ingress Static IPs | Egress Static IPs |
| --- | --- | --- |
| aws-af-south-1 | No | Yes |
| aws-ap-east-1 | No | Yes |
| aws-ap-northeast-1 | No | Yes |
| aws-ap-northeast-2 | No | Yes |
| aws-ap-south-1 | No | Yes |
| aws-ap-southeast-1 | No | Yes |
| aws-ap-southeast-2 | No | Yes |
| aws-ca-central-1 | No | Yes |
| aws-eu-central-1 | No | Yes |
| aws-eu-north-1 | Yes | Yes |
| aws-eu-south-1 | No | Yes |
| aws-eu-west-1 | No | Yes |
| aws-eu-west-2 | No | Yes |
| aws-eu-west-3 | No | Yes |
| aws-me-south | No | Yes |
| aws-sa-east-1 | Yes | Yes |
| aws-us-east-1 | Yes | Yes |
| aws-us-east-2 | No | Yes |
| aws-us-west-1 | Yes | Yes |
| aws-us-west-2 | No | Yes |

::::


::::{dropdown} Azure
| Region | Ingress Static IPs | Egress Static IPs |
| --- | --- | --- |
| azure-australiaeast | Yes | Yes |
| azure-brazilsouth | Yes | Yes |
| azure-canadacentral | Yes | Yes |
| azure-centralindia | Yes | Yes |
| azure-centralus | Yes | Yes |
| azure-eastus | Yes | Yes |
| azure-eastus2 | Yes | Yes |
| azure-francecentral | Yes | Yes |
| azure-japaneast | Yes | Yes |
| azure-northeurope | Yes | Yes |
| azure-southafricanorth | Yes | Yes |
| azure-southcentralus | Yes | Yes |
| azure-southeastasia | Yes | Yes |
| azure-uksouth | Yes | Yes |
| azure-westeurope | Yes | Yes |
| azure-westus2 | Yes | Yes |

::::


::::{dropdown} GCP
| Region | Ingress Static IPs | Egress Static IPs |
| --- | --- | --- |
| gcp-asia-east1 | Yes | No |
| gcp-asia-northeast1 | Yes | No |
| gcp-asia-northeast3 | Yes | No |
| gcp-asia-south1 | Yes | No |
| gcp-asia-southeast1 | Yes | No |
| gcp-asia-southeast2 | Yes | No |
| gcp-australia-southeast1 | Yes | No |
| gcp-europe-north1 | Yes | No |
| gcp-europe-west1 | Yes | No |
| gcp-europe-west2 | Yes | No |
| gcp-europe-west3 | Yes | No |
| gcp-europe-west4 | Yes | No |
| gcp-europe-west9 | Yes | No |
| gcp-northamerica-northeast1 | Yes | No |
| gcp-southamerica-east1 | Yes | No |
| gcp-us-central1 | Yes | No |
| gcp-us-east1 | Yes | No |
| gcp-us-east4 | Yes | No |
| gcp-us-west1 | Yes | No |
| gcp-us-west2 | Yes | No |

::::


::::{warning} 
:name: ec-warning

Static IP ranges are subject to change. You will need to update your firewall rules when they change to prevent service disruptions. We will announce changes at least 8 weeks in advance (see [example](https://status.elastic.co/incidents/1xs411x77wgh)). Subscribe to the [{{ecloud}} status page](https://status.elastic.co/) to remain up to date with any changes to the Static IP ranges which you will need to update at your side.
::::



## Using Static IPs [ec_using_static_ips] 

The {{ecloud}} range of static IPs is formatted as a simple JSON object and can be found at link: [https://ips.cld.elstc.co/](https://ips.cld.elstc.co/). Any searching, formatting, or filtering can be done on the client side.

For example:

`curl -s https://ips.cld.elstc.co/ | jq '.regions["aws-us-east-1"]'`

