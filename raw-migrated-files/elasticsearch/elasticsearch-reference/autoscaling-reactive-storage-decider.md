# Reactive storage decider [autoscaling-reactive-storage-decider]

The [autoscaling](../../../deploy-manage/autoscaling.md) reactive storage decider (`reactive_storage`) calculates the storage required to contain the current data set. It signals that additional storage capacity is necessary when existing capacity has been exceeded (reactively).

The reactive storage decider is enabled for all policies governing data nodes and has no configuration options.

The decider relies partially on using [data tier preference](../../../manage-data/lifecycle/data-tiers.md#data-tier-allocation) allocation rather than node attributes. In particular, scaling a data tier into existence (starting the first node in a tier) will result in starting a node in any data tier that is empty if not using allocation based on data tier preference. Using the [ILM migrate](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-migrate.html) action to migrate between tiers is the preferred way of allocating to tiers and fully supports scaling a tier into existence.

