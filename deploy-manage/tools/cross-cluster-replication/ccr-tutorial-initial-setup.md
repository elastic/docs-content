---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-tutorial-initial-setup.html
---

# Initial setup [ccr-tutorial-initial-setup]

1. Set up a remote cluster on both clusters.

    ```console
    ### On cluster A ###
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "clusterB": {
              "mode": "proxy",
              "skip_unavailable": true,
              "server_name": "clusterb.es.region-b.gcp.elastic-cloud.com",
              "proxy_socket_connections": 18,
              "proxy_address": "clusterb.es.region-b.gcp.elastic-cloud.com:9400"
            }
          }
        }
      }
    }
    ### On cluster B ###
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "clusterA": {
              "mode": "proxy",
              "skip_unavailable": true,
              "server_name": "clustera.es.region-a.gcp.elastic-cloud.com",
              "proxy_socket_connections": 18,
              "proxy_address": "clustera.es.region-a.gcp.elastic-cloud.com:9400"
            }
          }
        }
      }
    }
    ```

2. Set up bi-directional cross-cluster replication.

    ```console
    ### On cluster A ###
    PUT /_ccr/auto_follow/logs-generic-default
    {
      "remote_cluster": "clusterB",
      "leader_index_patterns": [
        ".ds-logs-generic-default-20*"
      ],
      "leader_index_exclusion_patterns":"*-replicated_from_clustera",
      "follow_index_pattern": "{{leader_index}}-replicated_from_clusterb"
    }

    ### On cluster B ###
    PUT /_ccr/auto_follow/logs-generic-default
    {
      "remote_cluster": "clusterA",
      "leader_index_patterns": [
        ".ds-logs-generic-default-20*"
      ],
      "leader_index_exclusion_patterns":"*-replicated_from_clusterb",
      "follow_index_pattern": "{{leader_index}}-replicated_from_clustera"
    }
    ```

    ::::{important}
    Existing data on the cluster will not be replicated by `_ccr/auto_follow` even though the patterns may match. This function will only replicate newly created backing indices (as part of the data stream).
    ::::


    ::::{important}
    Use `leader_index_exclusion_patterns` to avoid recursion.
    ::::


    ::::{tip}
    `follow_index_pattern` allows lowercase characters only.
    ::::


    ::::{tip}
    This step cannot be executed via the {{kib}} UI due to the lack of an exclusion pattern in the UI. Use the API in this step.
    ::::

3. Set up the {{ls}} configuration file.

    This example uses the input generator to demonstrate the document count in the clusters. Reconfigure this section to suit your own use case.

    ```json
    ### On Logstash server ###
    ### This is a logstash config file ###
    input {
      generator{
        message => 'Hello World'
        count => 100
      }
    }
    output {
      elasticsearch {
        hosts => ["https://clustera.es.region-a.gcp.elastic-cloud.com:9243","https://clusterb.es.region-b.gcp.elastic-cloud.com:9243"]
        user => "logstash-user"
        password => "same_password_for_both_clusters"
      }
    }
    ```

    ::::{important}
    The key point is that when `cluster A` is down, all traffic will be automatically redirected to `cluster B`. Once `cluster A` comes back, traffic is automatically redirected back to `cluster A` again. This is achieved by the option `hosts` where multiple ES cluster endpoints are specified in the array `[clusterA, clusterB]`.
    ::::


    ::::{tip}
    Set up the same password for the same user on both clusters to use this load-balancing feature.
    ::::

4. Start {{ls}} with the earlier configuration file.

    ```sh
    ### On Logstash server ###
    bin/logstash -f multiple_hosts.conf
    ```

5. Observe document counts in data streams.

    The setup creates a data stream named `logs-generic-default` on each of the clusters. {{ls}} will write 50% of the documents to `cluster A` and 50% of the documents to `cluster B` when both clusters are up.

    Bi-directional {{ccr}} will create one more data stream on each of the clusters with the `-replication_from_cluster{a|b}` suffix. At the end of this step:

    * data streams on cluster A contain:

        * 50 documents in `logs-generic-default-replicated_from_clusterb`
        * 50 documents in `logs-generic-default`

    * data streams on cluster B contain:

        * 50 documents in `logs-generic-default-replicated_from_clustera`
        * 50 documents in `logs-generic-default`

6. Queries should be set up to search across both data streams. A query on `logs*`, on either of the clusters, returns 100 hits in total.

    ```console
    GET logs*/_search?size=0
    ```
