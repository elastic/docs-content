---
navigation_title: Failover when clusterA is down
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_failover_when_clustera_is_down_2.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Bi-directional recovery: Failover when clusterA is down [_failover_when_clustera_is_down_2]

1. You can simulate this by shutting down either of the clusters. Let’s shut down `cluster A` in this tutorial.
2. Start {{ls}} with the same configuration file. (This step is not required in real use cases where {{ls}} ingests continuously.)

    ```sh
    ### On Logstash server ###
    bin/logstash -f multiple_hosts.conf
    ```

3. Observe all {{ls}} traffic will be redirected to `cluster B` automatically.

    ::::{tip} 
    You should also redirect all search traffic to the `clusterB` cluster during this time.
    ::::

4. The two data streams on `cluster B` now contain a different number of documents.

    * data streams on cluster A (down)

        * 50 documents in `logs-generic-default-replicated_from_clusterb`
        * 50 documents in `logs-generic-default`

    * data streams On cluster B (up)

        * 50 documents in `logs-generic-default-replicated_from_clustera`
        * 150 documents in `logs-generic-default`


