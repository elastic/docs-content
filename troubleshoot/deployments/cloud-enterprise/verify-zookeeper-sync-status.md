---
navigation_title: ZooKeeper sync status
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-zookeeper-sync.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Verify ZooKeeper sync status [ece-zookeeper-sync]

Before performing any maintenance on the platform, verify the ZooKeeper sync status to ensure the system is healthy and consistent. Confirm that each ECE host with the `director` role is running a ZooKeeper instance, that all instances are fully in sync, and that no unexpected instances are participating in the quorum.

Proceeding with maintenance or ECE upgrades while ZooKeeper is not fully healthy can lead to unexpected behavior, including data loss or quorum-related failures.

### Check at container level

To check that ZooKeeper is in sync with the correct number of followers, run the following steps:

1. Run the inline shell script command on each Director node:

    ```sh
    docker exec frc-zookeeper-servers-zookeeper sh -c '
    for i in $(seq 2191 2199); do 
      output=$(echo mntr | curl -s telnet://localhost:$i | grep -E "server_state|leader|follower|not currently serving|zk_znode_count"); 
      if [ -n "$output" ]; then 
        echo "ZK mntr Response from port $i:"; 
        echo "$output"; 
        break; 
      fi 
    done'
    ```

    ::::{note} 
    You must check all nodes to find the Leader node with the required sync information. This is currently tested only in Bash.
    ::::

2. From the Leader node’s output, make sure to check that:

    * The count of followers is correct and expected
    * All followers are listed as synced


The inline shell script command can return the following types of output:

* If the host is the current ZooKeeper Leader, the command returns the Leader’s info including follower count and follower sync status.

    ```
    ZK mntr Response from port 2191:
    zk_server_state leader
    zk_znode_count  783
    zk_synced_followers     2
    ...
    ```

* If the host is a follower, the command returns only the follower state, and continues until it finds the Leader:

    ```
    ZK mntr Response from port 2193:
    zk_server_state follower
    zk_znode_count  777
    ...
    ```

* If the ZooKeeper container is up and listening, but the current node doesn’t have the quorum, the command returns the message `This ZooKeeper instance is not currently serving requests`:

    ```
    ZK mntr Response from port 2192:
    This ZooKeeper instance is not currently serving requests
    ```


Make sure the ZooKeeper container is running on all the Director nodes. If another Director node is under maintenance, check that ZooKeeper is healthy and synced before starting any other nodes. If all expected nodes are up and running, there might be another issue. Reach out to Elastic support.

If there is no response on any port, it’s possible that no ZooKeeper ports are currently listening (for ex. running on a non-Director role host, or the ZooKeeper Docker container is not running)



### Alternative: Check at host level 

If the inline shell script command doesn’t work, you can run the check directly from the director host. This can happen for example when your user lacks permissions to access Docker. This approach avoids entering the container and doesn't require installing additional tools like `telnet` or `nc`, relying instead on `curl`, which is typically available by default on most Linux systems.

1. Run the equivalent inline shell script directly on the host terminal, outside of the zookeeper container
    ```
    for i in $(seq 2191 2199); do 
      output=$(echo mntr | curl -s telnet://localhost:$i | grep -E "server_state|leader|follower|not currently serving|zk_znode_count"); 
      if [ -n "$output" ]; then 
        echo "ZK mntr Response from port $i:"; 
        echo "$output"; 
        break; 
      fi 
    done
    ```
2. Look for the following lines in the output
  *  `zk_server_state leader` or `zk_server_state follower` — indicates the node’s ZooKeeper role

