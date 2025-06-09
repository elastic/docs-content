---
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: ga
navigation_title: "Add IP filters"
---

# IP filtering

This section covers traffic filtering by IP address or CIDR block.

The way that you configure IP filters depends on your deployment type.

:::{tip}
If you use {{ech}} or {{eck}}, then other [network security](/deploy-manage/security/traffic-filtering.md) methods are also available.
:::

## Serverless and ECH

In {{serverless-full}} and {{ech}}, network security policies are created at the organization level, and then applied at the deployment level. Follow these guides to learn how to create, apply, and manage these policies using your preferred method:
  
  * [In the {{ecloud}} console](/deploy-manage/security/ip-filtering-cloud.md)
  * [Using the {{ecloud}} API](/deploy-manage/security/ec-traffic-filtering-through-the-api)
  
To learn how multiple IP filter policies are processed, and how IP filters and [private connections](/deploy-manage/security/private-link-traffic-filters.md) work together in ECH, refer to [](/deploy-manage/security/network-security-policies.md).

## ECE

In {{ece}}, filter rules are created at the platform level, and then applied at the deployment level. Follow these guides to learn how to create, apply, and manage these policies using your preferred method:
  
  * [In the Cloud UI](/deploy-manage/security/ip-filtering-ece.md)
  * [Using the {{ecloud}} API](/deploy-manage/security/ec-traffic-filtering-through-the-api)
  
To learn how multiple rules are processed, refer to [Traffic filter rules](/deploy-manage/security/traffic-filter-rules.md).

## ECK and self managed

In {{eck}} and self-managed clusters, traffic filters are applied at the cluster level using `elasticsearch.yml`. [Learn how to configure traffic filtering at the cluster level](/deploy-manage/security/ip-filtering-basic.md).