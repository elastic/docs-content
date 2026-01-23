---
navigation_title: Corrupted repositories
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnosing-corrupted-repositories.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Diagnose corrupted repositories [diagnosing-corrupted-repositories]

{{es}} only supports one cluster having one write connection to a repository at a time. If {{es}} detects a corrupted repository, this might indicate that

* multiple {{es}} clusters are writing to the same snapshot repository
* the current {{es}} cluster has multiple write connections to the same snapshot repository
* an external service modified the snapshot repository's contents or underlying storage

You can check for this issue before detected errors from multiple writing repositories sharing overlapping `uuid` in the [list snapshot repositories API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get-repository) output. Once detected, [snapshot API's](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-snapshot) will error:
```
Could not read repository data because the contents of the repository do not match its expected state. This is likely the result of either concurrently modifying the contents of the repository by a process other than this cluster or an issue with the repository's underlying storage. The repository has been disabled to prevent corrupting its contents. To re-enable it and continue using it please remove the repository from the cluster and add it again to make the cluster recover the known state of the repository from its physical contents.
```

This repository error may surface within the [{{ilm}} explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle), [Allocation explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) and {{kib}} **Stack Management** UI. 

{{es}} log stack traces can surface more information like one of the following:

```
org.elasticsearch.ElasticsearchParseException: Detected a corrupted repository

snapshot_missing_exception [REPOSITORY_NAME:SNAPSHOT_NAME/SNAPSHOT_UUID] is missing

java.nio.file.NoSuchFileException: REPOSITORY_PATH/data/shared/indices/INDEX_UUID/SHARD_ID/FILE_NAME

no_such_file_exception Blob object [FILE_NAME] not found: The specified key does not exist.
```

Refer to [Repository contents](/deploy-manage/tools/snapshot-and-restore.md#snapshot-repository-contents) for potential side-effects of corruption of the repository contents. The following steps outline how to remedy the situation, but might be insufficient to resolve all errors depending on how corruption has occurred. To remedy the situation, mark the repository as read-only or remove it from all the other clusters, and re-add (recreate) the repository in the current cluster.

Fixing the corrupted repository requires making changes in multiple clusters that write to the same snapshot repository. Only one cluster must be writing to a repository. In these instructions, the cluster that continues writing to the repository is referred to as the "primary" cluster, and the other ones where we’ll mark the repository read-only as the "secondary" clusters.

:::::::{tab-set}

::::::{tab-item} Using {{kib}}
First, mark the repository as read-only on the secondary clusters:

1. Go to **Snapshot and Restore > Repositories**. You can find the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. The repositories table should now be visible. Click on the pencil icon at the right side of the repository to be marked as read-only. On the Edit page that opened scroll down and check "Read-only repository". Click "Save". Alternatively if disconnecting the repository altogether is preferable, select the checkbox at the left of the repository name in the repositories table and click the "Remove repository" red button at the top left of the table.

After you complete the previous steps, it’s only the primary (current) cluster that has the repository marked as writeable. {{es}} sees it as corrupt, so the repository needs to be removed and added back so that {{es}} can resume using it:

On the primary (current) clusteer:

1. Open the primary cluster's side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Snapshot and Restore > Repositories**. You can find the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. Click on the pencil icon at the right side of the repository. On the Edit page that opened scroll down and click "Save", without making any changes to the existing settings.

3. To verify results, click on the repository name. On the UI drawer that opened, click "Verify repository".
::::::

::::::{tab-item} Using the {{es}} API
First, work on the secondary clusters:

1. Get the configuration of the repository from [get snapshot repository information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get-repository):

    ```console
    GET _snapshot/my-repo
    ```

    The response looks like this:

    ```console-result
    {
      "my-repo": { <1>
        "type": "s3",
        "settings": {
          "bucket": "repo-bucket",
          "client": "elastic-internal-71bcd3",
          "base_path": "myrepo"
        }
      }
    }
    ```

    1. Represents the current configuration for the repository.

2. Using the settings retrieved above, add the `readonly: true` option to mark it as read-only with the [update snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository):

    ```console
    PUT _snapshot/my-repo
    {
        "type": "s3",
        "settings": {
          "bucket": "repo-bucket",
          "client": "elastic-internal-71bcd3",
          "base_path": "myrepo",
          "readonly": true <1>
        }
    }
    ```

    1. Marks the repository as read-only.

3. Alternatively, disconnect the repository is an option using [delete snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-delete-repository):

    ```console
    DELETE _snapshot/my-repo
    ```

    The response looks like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```


After you complete the previous steps, it’s only the primary (current) cluster that has the repository marked as writeable. {{es}} sees it as corrupt though so let’s recreate it so that {{es}} can resume using it. 

On the primary (current) cluster:

1. Get the configuration of the repository and save its configuration as we’ll use it to recreate the repository:

    ```console
    GET _snapshot/my-repo
    ```

2. Using the configuration we obtained above, let’s recreate the repository:

    ```console
    PUT _snapshot/my-repo
    {
      "type": "s3",
      "settings": {
        "bucket": "repo-bucket",
        "client": "elastic-internal-71bcd3",
        "base_path": "myrepo"
      }
    }
    ```

    The response looks like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```

3. To verify results, run [Verify a snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-verify-repository):

    ```console
    POST _snapshot/my-repo/_verify
    ```
::::::

:::::::

If the repository is still marked as corrupted or broken after applying these fixes, then [contact Elastic](/troubleshoot/index.md#contact-us) for assistance.