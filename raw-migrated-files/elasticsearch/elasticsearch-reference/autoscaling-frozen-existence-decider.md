# Frozen existence decider [autoscaling-frozen-existence-decider]

The [autoscaling](../../../deploy-manage/autoscaling.md) frozen existence decider (`frozen_existence`) ensures that once the first index enters the frozen ILM phase, the frozen tier is scaled into existence.

The frozen existence decider is enabled for all policies governing frozen data nodes and has no configuration options.

