# Upgrade Elastic on-prem [upgrading-elastic-stack-on-prem]

Once you are [prepared to upgrade](../../../deploy-manage/upgrade/deployment-or-cluster.md), you will need to upgrade each of your Elastic components individually.

1. Consider closing {{ml}} jobs before you start the upgrade process. While {{ml}} jobs can continue to run during a rolling upgrade, it increases the overhead on the cluster during the upgrade process.
2. Upgrade the components of your Elastic Stack in the following order:

    1. {{es}} Hadoop: [install instructions](elasticsearch-hadoop://reference/installation.md)
    2. {{es}}: [upgrade instructions](../../../deploy-manage/upgrade/deployment-or-cluster.md)
    3. Kibana: [upgrade instructions](../../../deploy-manage/upgrade/deployment-or-cluster.md)
    4. Java API Client: [dependency configuration](elasticsearch-java://reference/installation.md#maven)
    5. Logstash: [upgrade instructions](logstash://reference/upgrading-logstash.md)
    6. Beats: [upgrade instructions](beats://reference/libbeat/upgrading.md)
    7. {{agent}}: [upgrade instructions](/reference/ingestion-tools/fleet/upgrade-elastic-agent.md)


