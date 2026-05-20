---
navigation_title: Common problems
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-issues.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---
# Common problems with {{ece}} [ece-issues]

This set of common symptoms and resolutions can help you to diagnose unexpected behavior with Elastic Cloud Enterprise. You can also refer to the list of product [Limitations and known problems](cloud://release-notes/cloud-enterprise/known-issues.md).

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## Emergency token not spinning up the coordinator role [ece_emergency_token_not_spinning_up_the_coordinator_role]

**Symptom:** You have no access to API and UI because all coordinators are lost. More than half of the director hosts are available. If you have 5 directors, 3 directors must be available. If more than half of the directors are lost, it is crucial to investigate whether the ZooKeeper quorum can recover. Please refer to [Determine the Zookeeper leader](../cloud-enterprise/rebuilding-broken-zookeeper-quorum.md#ece_determine_the_zookeeper_leader) to gather essential information, and then contact support for further assistance. If all directors are lost, [re-install ECE](../../../deploy-manage/deploy/cloud-enterprise/install.md).

**Resolution:** Use the emergency token provided during the installation of the genesis ECE nodes. You must explicitly specify the roles with the parameter `--roles`, for example `"coordinator,director,proxy"`. Otherwise, the host does not run any role.


## Allocator failures [ece_allocator_failures]

Allocator failures result in alerts in the Cloud UI. You cannot repair an allocator in the Cloud UI, so you should first [move all nodes to a new allocator](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md).  Vacate options for a selected allocator can help fine tune the removal of nodes. After the allocator is vacated, you should investigate the cause of the failure separately, which could be due to a host machine failure, and replace any lost capacity.


## Allocators not being used [ece-issues-allocator-usage]

**Symptoms:** You installed Elastic Cloud Enterprise on a new host and assigned it the allocator role from the command line with the `--roles "allocator"` parameter during installation, but new clusters are not being created on the allocator.

**Resolution:** The issue is caused by a token specified with the `--roles-token 'TOKEN'` parameter that does not have sufficient privileges to assign the role correctly. To resolve this issue, you might need to refresh the roles for the allocator.

1. Follow the steps for [assigning roles to hosts](../../../deploy-manage/deploy/cloud-enterprise/assign-roles-to-hosts.md), but do not change any of the assigned roles. Select **Update roles**.
2. Verify that the allocator is now being used when creating new Elasticsearch clusters or moving nodes off other allocators.

To avoid this issue on future allocators you create, [generate a roles token](../../../deploy-manage/deploy/cloud-enterprise/generate-roles-tokens.md) that has the right permissions for this to work, in this case the permission to assign the allocator role; the token generated during the installation on the first host will not suffice.


## Cloud UI login failures [ece-issues-login-failure]

**Symptoms:** When you attempt to log into the Cloud UI, the login process appears to hang and then fails.

**Resolution:** The administration console that supports the Cloud UI might be running out of Java heap space, causing login failures. This issue is expected to be fixed in a future release. As a workaround, you can manually increase the heap size.

In the current release, there is no direct way to change the Java heap size in the UI, so you need to increase the heap size as follows:

1. For convenience, you can store the IP address of the host machine where the Cloud UI is running in the `ADMIN_IP` environment variable. Alternatively, replace `$ADMIN_IP` in the commands shown with the IP address.
2. Create a file with your current configuration, here `containerdata.json` (requires that you have [jq](https://stedolan.github.io/jq/download/) installed):

    ```sh
    curl -u admin http://$ADMIN_IP:12400/api/v1/platform/infrastructure/container-sets/admin-consoles/containers/admin-console > containerdata.json
    ```

    When prompted, enter the password you use to log into the Cloud UI.

3. Filter the output file to a format that you can modify and push back into the system. If this step fails, do not push the file back into the system as this can prevent the admin console container from starting up.

    ```sh
    jq '.config | .env' containerdata.json > containerdata_temp.json
    jq '{config: {env: .}}' containerdata_temp.json > containerdata_new.json
    rm containerdata_temp.json
    ```

4. Open the `containerdata_new.json` file in your favorite editor and locate this line:

    ```sh
    "ADMINCONSOLE_JAVA_OPTIONS=-Djute.maxbuffer=33554432 -Xmx256M -Xms256M",
    ```

5. Increase the Java heap size by changing the values for `Xmx` and `Xms` to 1024 or 4096, depending on the size of your host machine. For example: Change the values to `-Xmx1024M -Xms1024M`.
6. Save the configuration and exit the editor.
7. Apply the new configuration:

    ```sh
    curl -H 'Content-Type: application/json' -XPATCH -u admin http://$ADMIN_IP:12400/api/v1/platform/infrastructure/container-sets/admin-consoles/containers/admin-console -d @containerdata_new.json
    ```

8. On the host machine where the Cloud UI administration console is running, recreate the Cloud UI:

    ```sh
    docker stop frc-admin-consoles-admin-console && docker rm -f frc-admin-consoles-admin-console
    ```

    If you prefer, you can use the HTTPS protocol on port 12443, but it currently supports only a self-signed certificate. Alternatively, you can perform the step from localhost.

9. Log into the Cloud UI administration console to confirm that the issue is resolved.


## Cloud UI, Elasticsearch, and Kibana endpoint URLs inaccessible on AWS [ece-aws-private-ip]

**Symptoms:** When you attempt to log into the Cloud UI or when you attempt to connect to an Elasticsearch or Kibana endpoint URL, the connection eventually times out with an error. The error indicates that the host cannot be reached.

**Resolution:** On AWS, the default URLs provided might point to a private host IP address, which is not accessible externally. To resolve this issue, use a URL for the Cloud UI that is externally accessible and [update your cluster endpoint](../../../deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md) to use a public IP address for Elasticsearch and Kibana.

This issue applies only to hosts running on AWS, where both public and private IP addresses are provided.

To check if you are affected and to resolve this issue:

1. Compare the URL you are trying to reach to the host IP address information in the AWS EC2 Dashboard.

    For example, on a Elastic Cloud Enterprise installation, the following URLs might be provided by default:

    * Cloud UI: `http://192.168.40.73:12400`
    * Elasticsearch: `https://e025c4xxxxxxxxxxxxx.192.168.40.73.ip.es.io:9243/`
    * Kibana: `https://1e2b57xxxxxxxxxxxxx.192.168.40.73.ip.es.io:9243/`

    A quick check in the AWS EC2 Dashboard confirms that `192.168.40.73` is a private IP address, which is not accessible externally:

    :::{image} /troubleshoot/images/cloud-enterprise-ece-aws-private-ip.png
    :alt: Private IP address information in AWS EC2 Dashboard
    :::

2. To resolve this issue:

    * For the Cloud UI, use the public host name or public IP. In this example, the Cloud UI is accessible externally at `ec2-54-162-168-86.compute-1.amazonaws.com:12400`.
    * For Elasticsearch and Kibana, [update your cluster endpoint](../../../deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md) to use the public IP address. In this example, you can use `54.162.168.86`:

        :::{image} /troubleshoot/images/cloud-enterprise-ece-aws-public-ip.png
        :alt: Public IP address is used for cluster endpoints in the Cloud UI
        :::



## Upgrade failures [ece-troubleshooting-upgrade]

**Symptoms:** When upgrading Elastic Cloud Enterprise, the upgrade process indicates that a container upgrade has failed, followed by a rollback of all container upgrades and an error message that the upgrade process has failed. The information you get is similar to this output:

```
...
- Runner [192.168.44.10]: container [proxies-proxy] status changed: [upgrade failed] at [2017-08-23T20:27:02.114Z]
- Runner [192.168.44.10]: container [proxies-proxy] status changed: [rollback started] at [2017-08-23T20:27:07.134Z]
...
- The upgrade of the {{n}} installation has failed, but we successfully rolled back changes.
- Check that all services are running and that they are at the same version level with the docker ps command. Try the upgrade again.
- The log files on each host might provide additional information about the cause of the failures. (path: HOST_STORAGE_PATH/logs/upgrader-logs).
- You can find a backup of ZooKeeper's transaction log that was created before the upgrade in [/mnt/data/elastic/192.168.44.10/services/zookeeper/data/backup/20170823-202249/version-2].
- Exiting upgrader
- Removing upgrade container
```
**Resolution:** The Elastic Cloud Enterprise upgrade process is designed to be safe. If there is an issue with any part of the upgrade, the entire process is rolled back. In most cases, the rollback is automatic and the upgrade process can be reattempted after you fix the issue that caused the rollback.

The upgrade process can fail for several reasons, including:

* If a host fails during the upgrade process, causing the `frc-upgraders-monitor` container to time out while it monitors the upgrade process.
* If there is an issue with the ZooKeeper ensemble establishing a quorum after the upgrade or if the `frc-upgraders-upgrader` containers performing the upgrade on each host continue to wait for a ZooKeeper connection indefinitely to report their upgrade status.
* If an upgraded container does not keep running and the upgrade process determines that it is not viable.

To determine the root cause of an upgrade failure, the following logs are available where `HOST_STORAGE_PATH` and `RUNNER_ID` are specific to your installation:

`HOST_STORAGE_PATH/logs/upgrader-logs/monitor.log`
:   Available on the host where you initiated the upgrade process. This log file can help you pinpoint the host where an upgrade issue occurred or where in the overall upgrade process a failure happened.

`HOST_STORAGE_PATH/logs/upgrader-logs/upgrader.log`
:   Available on every host that attempted the upgrade. This log file can tell you about the specific issues that caused the upgrade to fail on a host.

In rare cases, a manual rollback of the upgrade might be required. For more help, [contact us](/troubleshoot/index.md#contact-us).

