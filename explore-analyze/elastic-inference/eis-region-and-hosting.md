---
navigation_title: Region and hosting
applies_to:
  stack: ga
  serverless: ga
description: Learn which regions host Elastic Inference Service (EIS) and how inference requests are routed.
---

# Region and hosting [eis-regions]

This page lists the {{aws}} and {{gcp}} regions where Elastic {{infer-cap}} Service (EIS) is available and explains how {{infer}} requests are routed.

**{{aws}}:**

* `us-east-1` (Virginia)

**{{gcp}}:**

* `asia-southeast1` (Singapore)
* `europe-west1` (Belgium)
* `us-east4` (Virginia)

All {{infer}} requests sent through EIS are routed to the nearest region, regardless of where your {{es}} deployment or {{serverless-short}} project is hosted.

Depending on the model being used, request processing may involve Elastic {{infer}} infrastructure and, in some cases, trusted third-party model providers. For example, ELSER and Jina requests are processed entirely within Elastic {{infer}} infrastructure. Other models, such as large language models or third-party embedding models, may involve additional processing by their respective model providers, which can operate in different cloud platforms or regions.
