---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-zookeeper-sync.html
---

# Verify ZooKeeper Sync Status [ece-zookeeper-sync]

It is recommended to check the ZooKeeper sync status before starting any maintenance on your Director nodes. This helps you prevent the following scenarios:

* The ECE UI **Settings** page displays all ZooKeeper nodes as connected, but not all the nodes have completed the syncing with the latest ZooKeeper state.
* Connected ZooKeeper nodes participate in the quorum, but they don’t appear in the ECE UI **Settings** page. For example, if the host is removed, ECE no longer cares about it and keeps the ZooKeeper container part of the quorum.

To check that ZooKeeper is in sync with the correct number of followers, run the following steps:

1. Run the one-line command on each Director node:

    ```sh
    docker exec frc-zookeeper-servers-zookeeper sh -c 'for i in $(seq 2191 2199); do echo trying port: $i;echo mntr | nc localhost ${i} 2>/dev/null | grep "not currently serving";echo mntr | nc localhost ${i} 2>/dev/null| grep leader; echo mntr | $(which nc) localhost ${i} 2>/dev/null | grep follower ; done'
    ```

    ::::{note} 
    You must check all nodes to find the Leader node with the required sync information. This is currently tested only in Bash.
    ::::

2. From the Leader node’s output, make sure to check that:

    * The count of followers is correct and expected
    * All followers are listed as synced


The one-line command can return the following types of output:

* If the host is the current ZooKeeper Leader, the command returns the Leader’s info including follower count and follower sync status.

    ```
    trying port: 2191
    zk_server_state leader
    zk_followers    2
    zk_synced_followers     2
    trying port: 2192
    trying port: 2193
    trying port: 2194
    trying port: 2195
    trying port: 2196
    trying port: 2197
    trying port: 2198
    trying port: 2199
    ```

* If the host is a follower, the command returns only the follower state, and continues until it finds the Leader:

    ```
    trying port: 2191
    trying port: 2192
    trying port: 2193
    zk_server_state follower
    trying port: 2194
    trying port: 2195
    trying port: 2196
    trying port: 2197
    trying port: 2198
    trying port: 2199
    ```

* If the ZooKeeper container is up and listening, but the current node doesn’t have the quorum, the command returns the message `This ZooKeeper instance is not currently serving requests`:

    ```
    trying port: 2191
    trying port: 2192
    This ZooKeeper instance is not currently serving requests
    trying port: 2193
    trying port: 2194
    trying port: 2195
    trying port: 2196
    trying port: 2197
    trying port: 2198
    trying port: 2199
    ```


Make sure the ZooKeeper container is running on all the Director nodes. If another Director node is under maintenance, check that ZooKeeper is healthy and synced before starting any other nodes. If all expected nodes are up and running, there might be another issue. Reach out to Elastic support.

If there is no response on any port, it’s possible that no ZooKeeper ports are currently listening (for ex. running on a non-Director role host, or the ZooKeeper Docker container is not running)

```
trying port: 2191
trying port: 2192
trying port: 2193
trying port: 2194
trying port: 2195
trying port: 2196
trying port: 2197
trying port: 2198
trying port: 2199
```

If the one line command doesn’t work, use telnet:

1. Run `docker ps | grep zoo` to reveal the port in use by the ZooKeeper container on the current host. The port won’t change once the container is started.
2. Install and run telnet, `telnet localhost <port #>` then type `mntr`

    * The port is in the range from 2191 to 2199.
    * for example `telnet localhost 2191`

3. Look for the following output lines:

    * `zk_server_state leader` or `zk_server_state follower` to indicate node leadership
    * Lines indicating the follower count and sync status when run against a Leader node

        * `zk_followers    2`
        * `zk_synced_followers     2`


