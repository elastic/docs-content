---
navigation_title: Hosted billing dimensions
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-dimensions.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Cloud Hosted deployment billing dimensions [ec-billing-dimensions]

{{ech}} billing is based on your actual usage across these categories of billing dimensions:

* [Deployment charges](#deployment-charges)
* [Organization charges](#data-transfer)
* [Add-ons](#add-ons)

Read on for detail about each of these categories and the billing dimensions in them.

## Deployment charges

$$$ram-hours$$$

Deployment charges are charges associated with running {{ech}} deployments. The only deployment charge is deployment capacity.

Deployment capacity refers to the cost of the nodes in your {{es}} deployment, plus additional node types such as {{kib}}, APM, and ML.  Each node type is priced in terms of GB of RAM per hour (CPU and disk are scaled with RAM and included in this price).  To calculate deployment capacity costs, we total up the cost of the nodes in your deployment(s) and multiply by GBs of RAM and how long they’ve been running.

Deployment capacity typically constitutes the majority of your bill, and is the easiest to understand and control.

The rate for deployment capacity depends on your [subscription level](manage-subscription.md), which also determines the level of support that you receive. Support is not listed as a separate charge on your bill.

### How can I control the deployment capacity cost? [ec_how_can_i_control_the_deployment_capacity_cost] 

Deployment capacity is purely a function of your current deployment configuration and time.  To reduce this cost, you must [configure your deployment](../../deploy/elastic-cloud/configure.md) to use fewer resources.  To determine how much a particular deployment configuration will cost, try our {{ech}} [pricing calculator](https://cloud.elastic.co/pricing).


## Organization charges [data-transfer]

Organization charges are applied across the {{ech}} deployments in your {{ecloud}} organization. The only organization charge is data transfer.

Data Transfer accounts for the volume of data (payload) going into, out of, and between the nodes in a deployment, which is summed up to a cumulative amount within a billing cycle.

We meter and bill data transfer using three dimensions:

1. **Data in (free)**
   
   *Data in* accounts for all of the traffic going into the deployment. It includes index requests with data payload, as well as queries sent to the deployment (although the byte size of the latter is typically much smaller).

2. **Data out**
   
   *Data out* accounts for all of the traffic coming out of the deployment. This includes search results, as well as monitoring data sent from the deployment. The same rate applies regardless of the destination of the data, whether to the internet, to another region, or to a cloud provider account in the same region. Data coming out of the deployment through AWS PrivateLink, GCP Private Service Connect, or Azure Private Link, is also considered *Data out*.

3. **Data inter-node**
   
   *Data inter-node* accounts for all of the traffic sent between the components of the deployment. This includes the data sync between nodes of a cluster which is managed automatically by {{es}} cluster sharding. It also includes data related to search queries executed across multiple nodes of a cluster. Note that single-node {{es}} clusters typically have lower charges, but may still incur inter-node charges accounting for data exchanged with {{kib}} nodes or other nodes, such as machine learning or APM.
   
We provide a free allowance of 100GB per month, which includes the sum of *data out* and *data inter-node*, across all deployments in the account. Once this threshold is passed, a charge is applied for any data transfer used in excess of the 100GB monthly free allowance.

::::{note} 
Data inter-node charges are currently waived for Azure deployments.
::::

### How can I control the data transfer cost? [ec_how_can_i_control_the_data_transfer_cost] 

Data transfer out of deployments and between nodes of the cluster is hard to control, as it is a function of the use case employed for the cluster and cannot always be tuned. Use cases such as batch queries executed at a frequent interval may be revisited to help lower transfer costs, if applicable. Watcher email alerts also count towards data transfer out of the deployment, so you may want to reduce their frequency and size.

The largest contributor to inter-node data transfer is usually shard movement between nodes in a cluster. [Oversharding](/deploy-manage/production-guidance/optimize-performance/size-shards.md) can cause excessive shard movement. Avoiding oversharding can also help control costs and improve performance. Note that creating snapshots generates inter-node data transfer. The *storage* cost of snapshots is detailed later in this document.

:::{note}
Using a single {{es}} node can lower inter-node data transfer, but that deployment is not highly available, and you risk losing data. For production, use at least two availability zones. Review [Plan for production](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) for more guidance.
:::

The exact root cause of unusual data transfer is not always something we can identify as it can have many causes, some of which are out of our control and not associated with Cloud configuration changes.  It may help to [enable monitoring](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) and examine index and shard activity on your cluster.


## Add-ons [add-ons]

Add-ons are capabilities that you can enable on your {{ech}} deployments. They're billed based on usage, in addition to the other billing dimensions of your deployments. Add-ons include:

* [Snapshot storage](#storage)
* [Synthetics](#synthetics)
* [Elastic {{infer-cap}} Service](#inference)
* [Workflow executions](#workflow-executions)
* [{{agent-builder}} executions](#agent-builder-executions)
* [{{managed-integrations}}](#managed-integrations)

### Snapshot storage [storage] 

Snapshot storage costs are tied to the cost of storing the backup snapshots in the underlying IaaS object store, such as AWS S3, Google Cloud GCS, or Azure Storage.
As is common with Cloud providers, we meter and bill snapshot storage using two dimensions:

1. **Storage size (GB/month)**
   
   This is calculated by metering the storage space (GBs) occupied by all snapshots of all deployments tied to an account. The same unit price applies to all regions. To calculate the due charges, we meter the amount of storage on an hourly basis and produce an average size (in GB) for a given month. The average amount is then used to bill the account for the GB/month used within a billing cycle (a calendar month).
    
   For example, if the storage used in April 2019 was 100GB for 10 days, and then 130GB for the remaining 20 days of the month, the average storage would be 120 GB/month, calculated as `(100*10 + 130*20)/30`.
   
   We provide a free allowance of 100 GB/month to all accounts across all the account deployments. Any metered storage usage below that amount will not be billed. Whenever the 100 GB/month threshold is crossed, we bill for the storage used in excess of the 100GB/month free allowance.


2. **Storage API requests (1K Requests/month)**
   
   These costs are calculated by counting the total number of calls to backup or restore snapshots made by all deployments associated with an account. Unlike storage size, this dimension is cumulative, summed up across the billing cycle, and is billed at a price of 1,000 requests.
   
   We provide a free allowance of 100,000 API requests to all accounts each month across all the account deployments. Once this threshold is passed, we bill only for the use of API requests in excess of the free allowance.
   
   ::::{note} 
   A single snapshot operation does not equal a single API call. There could be thousands of API calls associated with a single snapshot operation, as different files are written, deleted, and modified. The price we list is per 1000 API calls, so a rate of $0.0018 for 1000 API calls would cost $1.80 for a million calls.
   ::::

#### How can I control snapshot storage cost? [ec_how_can_i_control_the_storage_cost] 

Snapshots in {{ech}} save data incrementally at each snapshot event. This means that the effective snapshot size might be larger than the size of the current indices. The snapshot size increases as data is added or updated in the cluster, and deletions do not reduce the snapshot size until the snapshot containing that data is removed.

API requests are executed every time a snapshot is taken or restored, affecting usage costs. In the event that you have any automated processes that use the {{es}} API to create or restore snapshots, these should be set so as to avoid unexpected charges.

You can use {{kib}} to configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted, along with other options. To learn more, refer to the [Snapshot and restore](../../tools/snapshot-and-restore/create-snapshots.md) documentation.

Note that reducing either the snapshot frequency or retention period limits the availability and the recency of available data to restore from. Your snapshot policy should be configured with both costs and data availability in mind in order to minimize the potential for loss of data. Note also that reducing snapshot frequency and retention will not necessarily decrease your storage costs significantly. For example, if your dataset is only growing over time, then the total amount of data stored across all of your snapshots will be equal to your cluster size, whether that’s split across 10 snapshots or 100.

### Synthetics [synthetics] 

Synthetic Monitoring browser tests are charged per test run (metered in 60 second increments). Lightweight tests are charged per location per month (per deployment) for up to 1k simultaneous test run capacity (~2.6 billion tests per month). Tests executed from private locations do not incur an execution charge. All test result data is stored in your deployment and billed for under existing dimensions.

### Elastic Inference Service [inference]

[Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) is billed based on the tokens used with its models. For the pricing model and how to find {{infer}} usage in the {{ecloud}} Console, refer to [EIS pricing](/explore-analyze/elastic-inference/eis.md#pricing).

### Workflow executions [workflow-executions]

{{ech}} bills [workflows](/explore-analyze/workflows.md) based on workflow executions. Each workflow run counts as one execution. For metering details, including how unsuccessful and skipped runs are handled, refer to [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-billing).

The first 10,000 workflow executions across the {{ech}} deployments in an {{ecloud}} organization each month are included at no additional charge. Executions beyond 10,000 are billed for each execution, with volume tier discounts at higher usage levels. Each tier's rate applies only to the executions within that tier's range.

Volume tier usage resets at the start of each month. As a result, after your free allocation is used, the same usage can cost more early in the month than at the end of the previous one. For current billing amounts and tier breakpoints, refer to the [Hosted add-ons pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=stack_hosted&group=addons&dimension=executions).

### Agent Builder executions [agent-builder-executions]

{{ech}} bills {{agent-builder}} based on executions. Each completed interaction with an agent counts as at least one execution. For metering details, including how token volume and error responses are counted, refer to [Monitor usage and costs](/explore-analyze/ai-features/agent-builder/monitor-usage.md).

The first 10,000 {{agent-builder}} executions across the {{ech}} deployments in an {{ecloud}} organization each month are included at no additional charge. Executions beyond 10,000 are billed for each execution, with volume tier discounts at higher usage levels. Each tier's rate applies only to the executions within that tier's range.

Volume tier usage resets at the start of each month. As a result, after your free allocation is used, the same usage can cost more early in the month than at the end of the previous one. For current billing amounts and tier breakpoints, refer to the [Hosted add-ons pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=stack_hosted&group=addons&dimension=executions).

### {{managed-integrations}} [managed-integrations]

On {{ech}}, each deployed {{managed-integration}} is billed based on integration hours. For the rates, how usage is metered, and the {{managed-integrations}} that are exceptions, refer to the [{{managed-integrations}} FAQ](/reference/managed-integrations/managed-integrations-faq.md#managed-integrations-faq-pricing).
