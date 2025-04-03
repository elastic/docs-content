---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-securing-apm-server.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-keep-data-secure.html
---

# Use APM securely [apm-securing-apm-server]

When setting up Elastic APM, it’s critical to ensure that application data is secure from start to finish. You should approach securing your application data from different perspectives:

|     |     |
| --- | --- |
| **What kind of data is collected?** | Ensure that data doesn’t contain sensitive information like passwords,  credit card numbers, health data, or other identifiable information.<br>  Read more in [Secure data](../../../solutions/observability/apps/application-data-security.md). |
| **How do APM agents and {{agent}} communicate?** | Ensure that any communication between APM agents and {{agent}}  are both encrypted and authenticated.<br>  Read more in [Secure communication with APM agents](../../../solutions/observability/apps/secure-communication-with-apm-agents.md). |
| **How do APM Server and the {{stack}} communicate?** | Use role-based access control to grant APM Server users access  to secured resources. The roles that you set up depend on your organization’s security requirements and the  minimum privileges required to use specific features.<br>  Read more in [Secure communication with the {{stack}}](../../../solutions/observability/apps/secure-communication-with-elastic-stack.md). |
| **Who can use the Applications UI?** | Use role-based access control to grant users access to features of the Applications UI.<br>  Read more in [Secure access to the Applications UI](../../../solutions/observability/apps/secure-access-to-applications-ui.md). |