---
navigation_title: "Zookeeper quorum"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-troubleshooting-zookeeper-quorum.html
---

# Rebuilding a broken Zookeeper quorum [ece-troubleshooting-zookeeper-quorum]

::::{warning} 
This article covers an advanced recovery method involving directly modifying Zookeeper. This process can potentially corrupt your data. Elastic recommends only following this outline after receiving [confirmation by Elastic Support](ask-for-help.md).
::::


This article describes how to recover a broken Zookeeper leader or follower within {{ece}}.


## When to recover [ece-troubleshooting-zookeeper-quorum-check] 

When an ECE director host’s Zookeeper status cannot be determined healthy using the [Verify Zookeeper sync status](verify-zookeeper-sync-status.md) command or from **{{ece}}** > **Platform** > **Settings**, then you might need to recover Zookeeper.

This situation might surface when recovering the {{ece}} director host from a full disk issue.

A healthy Zookeeper quorum returns a sync status similar to the following. Any other responses require further investigation.

```sh
$ # Zookeeper leader with id:10
$ echo mntr | nc 127.0.0.1 2191
zk_server_state  leader
# ...
zk_followers         2
zk_synced_followers  2

$ # Zookeeper follower with id:11
$ echo mntr | nc 127.0.0.1 2192
zk_server_state follower

$ # Zookeeper follower with id:12
$ echo mntr | nc 127.0.0.1 2193
zk_server_state follower
```


## Back up data directories [ece_back_up_data_directories] 

Before recovering the Zookeeper leader or follower, back up all {{ece}} hosts' Zookeeper data directories. Normally this is only applicable to director hosts, but may apply to other hosts during migrations.

Perform the following steps on each host to back up the Zookeeper data directory:

1. Extract the Zookeeper `/data` directory path:

    ```sh
    docker inspect --format '{{ range .Mounts }}{{ .Source }} {{ end }}' frc-zookeeper-servers-zookeeper | grep --color=auto \"zookeeper/data\"
    ```

2. Make a copy or backup of the emitted directory. For example, if data directory is `/mnt/data/elastic/172.16.0.30/services/zookeeper/data`, then run the following command:

    ```sh
    cp -R /mnt/data/elastic/172.16.0.30/services/zookeeper/data /mnt/data/elastic/ZK_data_backup
    ```



## Determine the Zookeeper leader [ece_determine_the_zookeeper_leader] 

If a Zookeeper quorum is broken, you must establish the best Zookeeper leader to use for recovery before you start the recovery proces.

The simplest way to check is using the [Zookeeper sync status](verify-zookeeper-sync-status.md) command.

If this command is not reporting any leaders, then perform the following actions on each director host:

1. SSH into the host.
2. Enter the Docker `frc-zookeeper-servers-zookeeper` container and check its `/app/logs/zookeeper.log` logs for `LEADING`:

    ```sh
    $ docker exec -it frc-zookeeper-servers-zookeeper bash
    root@XXXXX:/# cat /app/logs/zookeeper.log | grep 'LEADING'
    ```

    This command will return results similar to the following:

    ```sh
    INFO  [QuorumPeer[myid=10](plain=0.0.0.0:2191)(secure=disabled):o.a.z.s.q.QuorumPeer@1549] - LEADING
    INFO  [QuorumPeer[myid=10](plain=0.0.0.0:2191)(secure=disabled):o.a.z.s.q.Leader@588] - LEADING - LEADER ELECTION TOOK - 225 MS
    ```

3. If multiple directors report this log, then determine the one with the latest timestamp, which will contain the latest Zookeeper state.


## Recover Zookeeper nodes [ece_recover_zookeeper_nodes] 

In the following recovery steps, the steps for the determined leader are marked with `[leader]`, and the steps for all other Zookeepers are marked with `[followers]`. The `[leader]` should be recovered as needed before its `[followers]`. Steps marked `[followers]` should be performed on each follower director host, and steps marked `[director]` should be performed only on problematic director hosts.


### Recover the Zookeeper Leader [ece-troubleshooting-zookeeper-quorum-leader] 


#### Restart the Zookeeper container [ece_restart_the_zookeeper_container] 

To recover the Zookeeper leader, you should first try to restart the Docker Zookeeper container. Restarting the container is often enough to trigger the leader to resync its connection to its followers.

Within a SSH session of Zookeeper hosts, run the following command:

```sh
docker restart frc-zookeeper-servers-zookeeper
```

Wait a few minutes for state to attempt to sync across leader and followers, then [verify the Zookeeper sync status](verify-zookeeper-sync-status.md) to see if the quorum has recovered.

If the Zookeeper leader is still not recovered, proceed to the next section.


#### Manually set the Zookeeper leader [ece_manually_set_the_zookeeper_leader] 

If restarting the Zookeeper container does not recover the leader, you can manually set the leader and rebuild the quorum.

1. `[followers]` Shut down the Docker Runner and Zookeeper containers:

    ```sh
    docker stop frc-runners-runner
    docker stop frc-zookeeper-servers-zookeeper
    ```

2. `[leader]` Stop the Zookeeper service within the Docker container. Note this is stopping the service within the Docker container and not stopping the Zookeeper Docker container itself:

    ```sh
    docker exec -it frc-zookeeper-servers-zookeeper sv stop zookeeper
    ```

3. `[leader]` Enter the Docker Zookeeper container and determine its Zookeeper ID:

    ```sh
    $ docker exec -it frc-zookeeper-servers-zookeeper bash
    root@XXXXX:/# cat /app/data/myid
    10
    ```

4. `[leader]` In the directory `/app/managed/`, modify the Zookeeper file `replicated.cfg.dynamic`:

    * Remove the lines referencing other Zookeeper hosts.
    * If multiple lines reference `localhost`, then remove all but the one containing the Zookeeper ID from the previous step.

5. `[leader]` Restart the Docker Zookeeper and Director containers:

    ```sh
    docker restart frc-zookeeper-servers-zookeeper
    docker restart frc-directors-director
    ```

6. `[leader]` Check the [Zookeeper sync status](verify-zookeeper-sync-status.md). The response should now show this director host as the Zookeeper leader.
7. Confirm that {{ece}} is now also able to check the Zookeeper status and make changes.
8. `[followers]` Restart the Docker Zookeeper, Director, and Runner containers:

    ```sh
    docker restart frc-zookeeper-servers-zookeeper
    docker restart frc-directors-director
    docker restart frc-runners-runner
    ```

9. Verify that the [Zookeeper sync status](verify-zookeeper-sync-status.md) reports an odd number for `zk_quorum_size` and that no Zookeeper hosts are marked as `lost`.


### Recover the Zookeeper follower [ece-troubleshooting-zookeeper-quorum-follower] 

Zookeeper followers can sometimes refuse a `[leader]` election or become state corrupted. The following steps can be used to recover a broken or corrupted Zookeeper `[follower]`. These steps should only be considered after confirming a Zookeeper leader, as the `[follower]` will be reset to copy the state from `[leader]`.

On the `[follower]`, do the following:

1. Get the director host’s Zookeeper `/data` directory path:

    ```sh
    docker inspect --format '{{ range .Mounts }}{{ .Source }} {{ end }}' frc-zookeeper-servers-zookeeper | grep --color=auto \"zookeeper/data\"
    ```

2. Stop the Docker Runner and Zookeeper containers:

    ```sh
    docker stop frc-runners-runner
    docker stop frc-zookeeper-servers-zookeeper
    ```

3. Under the determined `/data` directory, remove the sub-directory `data/version-NUMBER`, replacing the `NUMBER` placeholder.

    ```sh
    /mnt/data/elastic/MY_IP/services/zookeeper/data$ rm -R ./version-NUMBER/
    ```

    Make sure that `myid` file exists and is retained.

4. Start the Runner container, which will auto-start the Docker Zookeeper container.

    ```sh
    docker start frc-runners-runner
    ```

5. Wait a few minutes for Zookeeper states to sync. Then check the [Zookeeper sync status](verify-zookeeper-sync-status.md) to confirm the following:

    * `zk_server_state follower`
    * `zk_outstanding_requests 0`

6. Confirm that the `[leader]` recognizes the added `[follower]` by checking the [Zookeeper sync status](verify-zookeeper-sync-status.md) for an incremented `zk_synced_followers` count.

