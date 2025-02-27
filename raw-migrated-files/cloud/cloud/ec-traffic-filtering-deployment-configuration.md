# Traffic Filtering [ec-traffic-filtering-deployment-configuration]

Traffic filtering is one of the security layers available in {{ecloud}}. It allows you to limit how your deployments can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to *only* the sources that you trust.

{{ecloud}} supports the following traffic sources:

* [IP addresses and Classless Inter-Domain Routing (CIDR) masks](../../../deploy-manage/security/ip-traffic-filtering.md), e.g. `82.102.25.74` or `199.226.244.0/24`.
* [AWS Virtual Private Clouds (VPCs) over AWS PrivateLink](../../../deploy-manage/security/aws-privatelink-traffic-filters.md), supported only in AWS regions.
* [Azure Virtual Networks (VNets)](../../../deploy-manage/security/azure-private-link-traffic-filters.md), supported only in Azure regions.
* [GCP Private Service Connect](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md), supported only in GCP regions.
* [Remote cluster connections](../../../deploy-manage/remote-clusters/ec-enable-ccs.md), using organization and Elasticsearch cluster IDs for securing cross-cluster operations.

Filtering rules are grouped into rule sets, which in turn are associated with one or more deployments to take effect. Traffic between the instances in your deployment is automatically allowed.

Traffic filter operates on the proxy. Requests rejected by the traffic filter are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.

::::{note} 
Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.
::::


::::{note} 
You can have a maximum of 1024 rule sets per organization and 128 rules in each rule set.
::::



## Terminology [ec-traffic-filter-terminology] 

Traffic filter rule
:   Specifies traffic originating from an IP address, a CIDR mask, an AWS VPC endpoint ID, or an Azure Private Link Endpoint.

Traffic filter rule set
:   A named set of *traffic filter rules*. It defines allowed traffic sources. Rule sets can be used across multiple deployments. Note that the rules are not in effect until the rule set is associated with a deployment.

Rule set association
:   One or more rule sets can be associated with a deployment. In such a case, the traffic sources specified in the rule sets are allowed to connect to the deployment. No other traffic source  is allowed.


## How does it work? [ec-traffic-filter-how-does-it-work] 

By default, all your deployments are accessible over the public internet. They are not accessible over unknown PrivateLink connections.

Once you associate at least one traffic filter with a deployment, traffic that does not match any rules (for this deployment) is denied.

::::{note} 
This only applies to external traffic. Internal traffic is managed by {{ecloud}}. For example, Kibana can connect to Elasticsearch, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.
::::


You can assign multiple rule sets to a single deployment. The rule sets can be of  different types.

In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match the request is rejected with `403 Forbidden`.

You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created.

::::{note} 
A *default* rule set is not automatically attached to existing deployments.
::::


For more information about creating and editing rule sets and then associating them with your deployments, read more about [IP addresses and CIDR masks](../../../deploy-manage/security/ip-traffic-filtering.md), [AWS Virtual Private Clouds (VPCs) over AWS PrivateLink](../../../deploy-manage/security/aws-privatelink-traffic-filters.md), [Azure VNets over Azure Private Link](../../../deploy-manage/security/azure-private-link-traffic-filters.md), or [GCP Private Service Connect](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md).

::::{note} 
Traffic filter rule sets are bound to a single region. The rule sets can be assigned only to deployments in the same region. If you want to associate a rule set with deployments in multiple regions you have to create the same rule set in all the regions you want to apply it to.
::::


::::{note} 
Traffic filter rule sets when associated with a deployment will apply to all deployment endpoints, such as Elasticsearch, Kibana, APM Server, and others.
::::


::::{note} 
Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint; deny all access over Private Link*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.
::::



## Example scenarios [ec-traffic-filter-how-does-it-work-example] 

Jane creates a deployment. At this point the deployment is accessible over internet through its public endpoint, e.g. `https://fcd41689e9214319b1278325fd6af7cd.us-east-1.aws.found.io`. The deployment is protected by username+password authentication, but there’s no additional traffic source filtering.

Jane wants to restrict access to the deployment so that only the traffic originating from Jane’s VPC is allowed.

* They create a Traffic Filter *Private Link Endpoint* rule set, thus registering their VPC with {{ecloud}}.
* They associate this rule set with the deployment.
* At this point, their deployment is only accessible over PrivateLink from Jane’s VPC. This does not affect other security layers, so Jane’s users need to authenticate with username+password.
* The deployment is no longer accessible over the public internet endpoint.

Later on, Jane wants to allow access to the deployment from Jane’s Office.

* They create an IP rule set with office IP range give as a CIDR mask, e.g. `199.226.244.0/24`.
* They attach the rule set to the deployment.
* The deployment is accessible from Jane’s VPC and from Jane’s Office.

Finally, Jane decides to allow anyone to connect to the deployment over the public internet.

* They create the *allow all* rule set, with the CIDR mask `0.0.0.0/0`.
* They associate it with Jane’s deployment.
* Anyone with a valid username+password can now access the deployment.
* They could remove the Jane’s Office rule set — `199.226.244.0/24`. It is a subset of the *allow all*. They prefer to keep it attached anyways, in case they need to deny access from the public internet in the future.


## Deploy traffic filters [ec-traffic-filter-details] 

Follow the instructions that match your use case:

* [IP addresses and Classless Inter-Domain Routing (CIDR) masks](../../../deploy-manage/security/ip-traffic-filtering.md), e.g. `82.102.25.74` or `199.226.244.0/24`.
* Traffic filters compatible with specific cloud providers:
* [AWS Virtual Private Clouds (VPCs) over AWS PrivateLink](../../../deploy-manage/security/aws-privatelink-traffic-filters.md).
* [Azure Virtual Networks (VNets)](../../../deploy-manage/security/azure-private-link-traffic-filters.md).
* [GCP Private Service Connect](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md).


## Troubleshooting [ec-traffic-filter-troubleshooting] 

This section offers suggestions on how to troubleshoot your traffic filters. Before you start make sure you check the [Restrictions and known problems](../../../deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md).


### Review the rule sets associated with a deployment [ec-review-rule-sets] 

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Select the **Security** tab on the left-hand side menu bar.
4. Traffic filter rule sets are listed under **Traffic filters**.

On this screen you can view and remove existing filters and attach new filters.


### Identify default rule sets [ec-default-rule-sets] 

To identify which rule sets are automatically applied to new deployments in your account:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
3. Under the **Features** tab, open the **Traffic filters** page.
4. You can find the list of traffic filter rule sets.
5. Select each of the rule sets — **Include by default** is checked when this rule set is automatically applied to all new deployments in its region.


### How to view rejected requests [ec-rejected-traffic-requests] 

Requests rejected by traffic filter have status code `403 Forbidden` and response body `{"ok":false,"message":"Forbidden due to traffic filtering. Please see the Elastic documentation on Traffic Filtering for more information."}`.









