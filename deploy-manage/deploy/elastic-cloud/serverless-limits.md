---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-limits.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Index Limit Per Project

Elastic Cloud Serverless scales automatically to support your project loads. While the Elastic Cloud Serverless product offering aims to provide a service which scales well around most variations in the shape of customer data and load, there are some unusual scenarios which can’t necessarily be supported well yet. To ensure a reliable and consistent experience with the service, we have implemented some limits. These limits provide guardrails for performance and stability, and are documented here to help you design your solution with confidence.

Some limits can be increased by request (noted as adjustable) - others are fixed. To request a limit increase, open a support case stating which limit you would like to have increased, the new value you would prefer, and give a brief synopsis of how your use case utilizes indices and data streams to solve data problems at scale. Elastic will review your request and might want to discuss your use case to ensure that increasing the limit will provide the right experience for your workload.

| Limit | Value | Adjustable? |
| :--- | :--- |:---|
| Number of indices per project | 15,000 | Yes |
