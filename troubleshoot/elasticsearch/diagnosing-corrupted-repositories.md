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

Multiple {{es}} deployments are writing to the same snapshot repository. {{es}} doesn’t support this configuration and only one cluster is allowed to write to the same repository. Refer to [Repository contents](../../deploy-manage/tools/snapshot-and-restore.md#snapshot-repository-contents) for potential side-effects of corruption of the repository contents, which might not be resolved by the following guide. To remedy the situation mark the repository as read-only or remove it from all the other deployments, and re-add (recreate) the repository in the current deployment.

Fixing the corrupted repository requires making changes in multiple deployments that write to the same snapshot repository. Only one deployment must be writing to a repository. In these instructions, the deployment that continues writing to the repository is referred to as the "primary" deployment (the current cluster), and the other one(s) where we’ll mark the repository read-only as the "secondary" deployments.

:::::::{tab-set}

::::::{tab-item} Using {{kib}}
First, mark the repository as read-only on the secondary deployments:

1. Go to **Snapshot and Restore > Repositories**. You can find the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. The repositories table should now be visible. Click on the pencil icon at the right side of the repository to be marked as read-only. On the Edit page that opened scroll down and check "Read-only repository". Click "Save". Alternatively if deleting the repository altogether is preferable, select the checkbox at the left of the repository name in the repositories table and click the "Remove repository" red button at the top left of the table.

After you complete the previous steps, it’s only the primary (current) deployment that has the repository marked as writeable. {{es}} sees it as corrupt, so the repository needs to be removed and added back so that {{es}} can resume using it:

On the primary (current) deployment:

1. Open the primary deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Snapshot and Restore > Repositories**. You can find the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. Click on the pencil icon at the right side of the repository. On the Edit page that opened scroll down and click "Save", without making any changes to the existing settings.
::::::

::::::{tab-item} Using the {{es}} API
Fixing the corrupted repository requires making changes in multiple clusters that write to the same snapshot repository. Only one cluster must be writing to a repository. Let’s call the cluster we want to keep writing to the repository the "primary" cluster (the current cluster), and the other one(s) where we’ll mark the repository as read-only the "secondary" clusters.

First, work on the secondary clusters:

1. Get the configuration of the repository:

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

2. Using the settings retrieved above, add the `readonly: true` option to mark it as read-only:

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

3. Alternatively, deleting the repository is an option using:

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
::::::

:::::::
