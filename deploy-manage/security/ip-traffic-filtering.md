---
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: unavailable
---

# IP traffic filtering

This section covers traffic filtering by IP address or CIDR block.

The way that you configure IP traffic filters depends on your deployment type: 

* **In {{ece}} and {{ech}}**, traffic filter rules are created at the organization or platform level, and then applied at the deployment level. [Learn how to create, apply and manage these rules](/deploy-manage/security/ip-filtering-cloud.md).
  
  To learn how multiple rules are processed, and how IP traffic filters and [private link traffic filters](/deploy-manage/security/private-link-traffic-filters.md) work together in ECH, refer to [Traffic filter rules](/deploy-manage/security/traffic-filtering.md#traffic-filter-rules).

* **In {{eck}} and self-managed clusters**, traffic filters are applied at the cluster level using `elasticsearch.yml`. [Learn how to configure traffic filtering at the cluster level](/deploy-manage/security/ip-filtering-basic.md).

If you use {{ech}} or {{eck}}, then other [traffic filtering](/deploy-manage/security/traffic-filtering.md) methods are also available.