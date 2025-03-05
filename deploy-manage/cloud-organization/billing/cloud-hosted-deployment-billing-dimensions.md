---
navigation_title: "Hosted billing dimensions"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-dimensions.html
applies_to:
  deployment:
    ess: all
---

# Cloud Hosted deployment billing dimensions [ec-billing-dimensions]

{{ech}} billing is based on your actual usage across a number of dimensions, as follows:

1. [Deployment capacity](#ram-hours)
2. [Data Transfer](#data-transfer)
3. [Storage](#storage)
4. [Synthetics](#synthetics)

Read on for detail about each of these billing dimensions.


## Deployment capacity [ram-hours] 

Deployment capacity refers to the cost of the nodes in your Elasticsearch deployment, plus additional node types such as Kibana, APM, and ML.  Each node type is priced in terms of GB of RAM per hour (CPU and disk are scaled with RAM and included in this price).  To calculate deployment capacity costs, we total up the cost of the nodes in your deployment(s) and multiply by GBs of RAM and how long they’ve been running.

Deployment capacity typically constitutes the majority of your bill, and is the easiest to understand and control.


### How can I control the deployment capacity cost? [ec_how_can_i_control_the_deployment_capacity_cost] 

Deployment capacity is purely a function of your current deployment configuration and time.  To reduce this cost, you must [configure your deployment](../../deploy/elastic-cloud/configure.md) to use fewer resources.  To determine how much a particular deployment configuration will cost, try our [pricing calculator](https://cloud.elastic.co/pricing).


## Data Transfer [data-transfer] 

Data Transfer accounts for the volume of data (payload) going into, out of, and between the nodes in a deployment, which is summed up to a cumulative amount within a billing cycle.

We meter and bill data transfer using three dimensions:

1. Data in (free)
:   *Data in* accounts for all of the traffic going into the deployment. It includes index requests with data payload, as well as queries sent to the deployment (although the byte size of the latter is typically much smaller).

2. Data out
:   *Data out* accounts for all of the traffic coming out of the deployment. This includes search results, as well as monitoring data sent from the deployment. The same rate applies regardless of the destination of the data, whether to the internet, to another region, or to a cloud provider account in the same region. Data coming out of the deployment through AWS PrivateLink, GCP Private Service Connect, or Azure Private Link, is also considered *Data out*.

3. Data inter-node
:   *Data inter-node* accounts for all of the traffic sent between the components of the deployment. This includes the data sync between nodes of a cluster which is managed automatically by Elasticsearch cluster sharding. It also includes data related to search queries executed across multiple nodes of a cluster. Note that single-node Elasticsearch clusters typically have lower charges, but may still incur inter-node charges accounting for data exchanged with Kibana nodes or other nodes, such as machine learning or APM.

We provide a free allowance of 100GB per month, which includes the sum of *data out* and *data inter-node*, across all deployments in the account. Once this threshold is passed, a charge is applied for any data transfer used in excess of the 100GB monthly free allowance.

::::{note} 
Data inter-node charges are currently waived for Azure deployments.
::::



### How can I control the Data Transfer cost? [ec_how_can_i_control_the_data_transfer_cost] 

Data transfer out of deployments and between nodes of the cluster is hard to control, as it is a function of the use case employed for the cluster and cannot always be tuned. Use cases such as batch queries executed at a frequent interval may be revisited to help lower transfer costs, if applicable. Watcher email alerts also count towards data transfer out of the deployment, so you may want to reduce their frequency and size.

The largest contributor to inter-node data transfer is usually shard movement between nodes in a cluster.  The only way to prevent shard movement is by having a single node in a single availability zone. This solution is only possible for clusters up to 64GB RAM and is not recommended as it creates a risk of data loss. [Oversharding](/deploy-manage/production-guidance/optimize-performance/size-shards.md) can cause excessive shard movement. Avoiding oversharding can also help control costs and improve performance. Note that creating snapshots generates inter-node data transfer. The *storage* cost of snapshots is detailed later in this document.

The exact root cause of unusual data transfer is not always something we can identify as it can have many causes, some of which are out of our control and not associated with Cloud configuration changes.  It may help to [enable monitoring](../../monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) and examine index and shard activity on your cluster.


## Storage [storage] 

Storage costs are tied to the cost of storing the backup snapshots in the underlying IaaS object store, such as AWS S3, Google Cloud GCS or Azure Storage. These storage costs are *not* for the disk storage that persists the Elasticsearch indices, as that is already included in the [RAM Hours](#ram-hours).

As is common with Cloud providers, we meter and bill snapshot storage using two dimensions:

1. Storage size (GB/month)
:   This is calculated by metering the storage space (GBs) occupied by all snapshots of all deployments tied to an account. The same unit price applies to all regions. To calculate the due charges, we meter the amount of storage on an hourly basis and produce an average size (in GB) for a given month. The average amount is then used to bill the account for the GB/month used within a billing cycle (a calendar month).

    For example, if the storage used in April 2019 was 100GB for 10 days, and then 130GB for the remaining 20 days of the month, the average storage would be 120 GB/month, calculated as (100*10 + 130*20)/30.

    We provide a free allowance of 100 GB/month to all accounts across all the account deployments. Any metered storage usage below that amount will not be billed. Whenever the 100 GB/month threshold is crossed, we bill for the storage used in excess of the 100GB/month free allowance.


2. Storage API requests (1K Requests/month)
:   These costs are calculated by counting the total number of calls to backup or restore snapshots made by all deployments associated with an account. Unlike storage size, this dimension is cumulative, summed up across the billing cycle, and is billed at a price of 1,000 requests.

    We provide a free allowance of 100,000 API requests to all accounts each month across all the account deployments. Once this threshold is passed, we bill only for the use of API requests in excess of the free allowance.

    ::::{note} 
    A single snapshot operation does not equal a single API call. There could be thousands of API calls associated with a single snapshot operation, as different files are written, deleted, and modified. The price we list is per 1000 API calls, so a rate of $0.0018 for 1000 API calls would cost $1.80 for a million calls.
    ::::



### How can I control the storage cost? [ec_how_can_i_control_the_storage_cost] 

Snapshots in {{ech}} save data incrementally at each snapshot event. This means that the effective snapshot size may be larger than the size of the current indices. The snapshot size increases as data is added or updated in the cluster, and deletions do not reduce the snapshot size until the snapshot containing that data is removed.

API requests are executed every time a snapshot is taken or restored, affecting usage costs. In the event that you have any automated processes that use the Elasticsearch API to create or restore snapshots, these should be set so as to avoid unexpected charges.

You can use Kibana to configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted, along with other options. To learn more, refer to the [Snapshot and Restore](../../tools/snapshot-and-restore/create-snapshots.md) documentation.

Note that reducing either the snapshot frequency or retention period limits the availability and the recency of available data to restore from. Your snapshot policy should be configured with both costs and data availability in mind in order to minimize the potential for loss of data. Note also that reducing snapshot frequency and retention will not necessarily decrease your storage costs significantly. For example, if your dataset is only growing over time, then the total amount of data stored across all of your snapshots will be equal to your cluster size, whether that’s split across 10 snapshots or 100.


## Synthetics [synthetics] 

Synthetic Monitoring browser tests are charged per test run (metered in 60 second increments). Lightweight tests are charged per location per month (per deployment) for up to 1k simultaneous test run capacity (~2.6 billion tests per month). Tests executed from private locations do not incur an execution charge. All test result data is stored in your deployment and billed for under existing dimensions.

