---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-phone-home.html
---

# Statistics collected by {{ece}} [ece-phone-home]

When you [log into the Cloud UI](log-into-cloud-ui.md) for the first time, you are asked to agree to the software license agreement and can opt out of sharing some basic usage statistics about {{ece}} with Elastic. These statistics are never shared with anyone else. If you are unsure about opting out, the following information describes what we collect.

For each {{ece}} installation, we collect:

* Installation ID
* License information
* The number of hosts in the installation
* The number of allocators
* The total capacity by provided by allocators
* The total RAM used by allocators
* The availability zone each allocator belongs to
* The total RAM available to and the total RAM used by each availability zone
* The number of {{es}} clusters

For each {{es}} cluster, we collect:

* Whether a cluster has a {{kib}} instance associated with it
* Whether monitoring is configured

Sharing these statistics with us can help us understand how you use our product better and can help us improve the product.

If you already agreed to statistics sharing and would prefer to opt out, you can follow these steps:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Turn off the **Share usage statistics with Elastic** setting.

