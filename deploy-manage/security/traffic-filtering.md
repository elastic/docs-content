---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-deployment-configuration.html
---

# Secure network access

:::{warning}
**This page is a work in progress.** 
:::


Never expose {{es}} to unwanted internet traffic. Using an application to sanitize requests to {{es}} still poses risks, such as a malicious user writing [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search) requests that could overwhelm an {{es}} cluster and bring it down. Depending on your environment, consider the following:

- **IP traffic filtering**: Restrict access based on IP addresses or CIDR ranges.
- **Private link filters**: Secure connectivity through AWS PrivateLink, Azure Private Link, or GCP Private Service Connect.
- **Elastic Cloud static IPs**: Use static IP addresses for predictable firewall rules.
