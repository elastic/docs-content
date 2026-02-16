---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/elastic-endpoint-deploy-reqs.html
  - https://www.elastic.co/guide/en/serverless/current/security-elastic-endpoint-deploy-reqs.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# {{elastic-defend}} requirements [elastic-endpoint-deploy-reqs]

To properly deploy {{elastic-defend}} without a Mobile Device Management (MDM) profile, you must manually enable additional permissions on the host before {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—is fully functional. For more information, refer to [](enable-access-for-macos.md).

For information about supported operating systems, refer to the [Elastic Support Matrix](https://www.elastic.co/support/matrix#elastic-defend).


## Minimum system requirements [_minimum_system_requirements]

| Requirement | Value |
| --- | --- |
| **CPU** | Under 2% |
| **Disk space** | 1 GB |
| **Resident set size (RSS) memory** | 500 MB |
