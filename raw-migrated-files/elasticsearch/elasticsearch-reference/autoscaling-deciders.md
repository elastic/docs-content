# Autoscaling deciders [autoscaling-deciders]

[Reactive storage decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates required storage capacity of current data set. Available for policies governing data nodes.

[Proactive storage decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates required storage capacity based on current ingestion into hot nodes. Available for policies governing hot data nodes.

[Frozen shards decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates required memory capacity based on the number of partially mounted shards. Available for policies governing frozen data nodes.

[Frozen storage decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates required storage capacity as a percentage of the total data set of partially mounted indices. Available for policies governing frozen data nodes.

[Frozen existence decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates a minimum require frozen memory and storage capacity when any index is in the frozen [ILM](../../../manage-data/lifecycle/index-lifecycle-management.md) phase.

[Machine learning decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Estimates required memory capacity based on machine learning jobs. Available for policies governing machine learning nodes.

[Fixed decider](../../../deploy-manage/autoscaling/autoscaling-deciders.md)
:   Responds with a fixed required capacity. This decider is intended for testing only.








