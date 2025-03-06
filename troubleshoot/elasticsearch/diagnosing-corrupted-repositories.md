---
navigation_title: Corrupted repositories
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnosing-corrupted-repositories.html
---

# Diagnose corrupted repositories [diagnosing-corrupted-repositories]

Multiple {{es}} deployments are writing to the same snapshot repository. {{es}} doesn’t support this configuration and only one cluster is allowed to write to the same repository. See [Repository contents](../../deploy-manage/tools/snapshot-and-restore.md#snapshot-repository-contents) for potential side-effects of corruption of the repository contents, which may not be resolved by the following guide. To remedy the situation mark the repository as read-only or remove it from all the other deployments, and re-add (recreate) the repository in the current deployment:

:::::::{tab-set}

::::::{tab-item} {{ech}}
Fixing the corrupted repository will entail making changes in multiple deployments that write to the same snapshot repository. Only one deployment must be writing to a repository. The deployment that will keep writing to the repository will be called the "primary" deployment (the current cluster), and the other one(s) where we’ll mark the repository read-only as the "secondary" deployments.

First mark the repository as read-only on the secondary deployments:

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Stack Management > Snapshot and Restore > Repositories**.

    :::{image} ../../images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. The repositories table should now be visible. Click on the pencil icon at the right side of the repository to be marked as read-only. On the Edit page that opened scroll down and check "Read-only repository". Click "Save". Alternatively if deleting the repository altogether is preferable, select the checkbox at the left of the repository name in the repositories table and click the "Remove repository" red button at the top left of the table.

At this point, it’s only the primary (current) deployment that has the repository marked as writeable. {{es}} sees it as corrupt, so the repository needs to be removed and added back so that {{es}} can resume using it:

Note that we’re now configuring the primary (current) deployment.

1. Open the primary deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Stack Management > Snapshot and Restore > Repositories**.

    :::{image} ../../images/elasticsearch-reference-repositories.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

2. Click on the pencil icon at the right side of the repository. On the Edit page that opened scroll down and click "Save", without making any changes to the existing settings.
::::::

::::::{tab-item} Self-managed
Fixing the corrupted repository will entail making changes in multiple clusters that write to the same snapshot repository. Only one cluster must be writing to a repository. Let’s call the cluster we want to keep writing to the repository the "primary" cluster (the current cluster), and the other one(s) where we’ll mark the repository as read-only the "secondary" clusters.

Let’s first work on the secondary clusters:

1. Get the configuration of the repository:

    ```console
    GET _snapshot/my-repo
    ```

    The response will look like this:

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

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```


At this point, it’s only the primary (current) cluster that has the repository marked as writeable. {{es}} sees it as corrupt though so let’s recreate it so that {{es}} can resume using it. Note that now we’re configuring the primary (current) cluster:

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

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```
::::::

:::::::
