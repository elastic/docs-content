---
navigation_title: Setup and security
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/setup.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Setting up machine learning [setup]

## Requirements overview [requirements-overview]

To use the {{stack}} {{ml-features}}, you must have:

* the [appropriate subscription](https://www.elastic.co/subscriptions) level or the free trial period activated
* `xpack.ml.enabled` set to its default value of `true` on every node in the cluster (refer to [{{ml-cap}} settings in {{es}}](elasticsearch://reference/elasticsearch/configuration-reference/machine-learning-settings.md))
* `ml` value defined in the list of `node.roles` on the [{{ml}} nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#ml-node)
* {{ml}} features visible in the {{kib}} space
* security privileges assigned to the user that:

  * grant use of {{ml-features}}, and
  * grant access to source and destination indices.

::::{tip}
The fastest way to get started with {{ml-features}} is to [start a free 14-day trial of {{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
::::

## Security privileges [setup-privileges]

Assigning security privileges affects how users access {{ml-features}}. Consider the two main categories:

* **[{{es}} API user](#es-security-privileges)**: uses an {{es}} client, cURL, or {{kib}} Dev Tools to access {{ml-features}} via {{es}} APIs. It requires {{es}} security privileges.
* **[{{kib}} user](#kib-security-privileges)**: uses the {{ml-features}} in {{kib}} and does not use Dev Tools. It requires either {{kib}} feature privileges or {{es}} security privileges and is granted the most permissive combination of both. {{kib}} feature privileges are recommended if you control job level visibility via **Spaces**. {{ml-cap}} features must be visible in the relevant space. Refer to [Feature visibility in Spaces](#kib-visibility-spaces) for configuration information.

You can configure these privileges

* under the **Roles** and **Spaces** management pages. Find these pages in the main menu or use the [global search field](../find-and-organize/find-apps-and-objects.md).
* via the respective {{es}} security APIs.

### {{es}} API user [es-security-privileges]

If you use {{ml}} APIs, you must have the following cluster and index privileges:

For full access:

* `machine_learning_admin` built-in role or the equivalent cluster privileges
* `read` and `view_index_metadata` on source indices
* `read`, `manage`, and `index` on destination indices (for {{dfanalytics-jobs}} only)

For read-only access:

* `machine_learning_user` built-in role or the equivalent cluster privileges
* `read` index privileges on source indices
* `read` index privileges on destination indices (for {{dfanalytics-jobs}} only)

::::{important}
The `machine_learning_admin` and `machine_learning_user` built-in roles give access to the results of *all* {{anomaly-jobs}}, irrespective of whether the user has access to the source indices. You must carefully consider who is given these roles, as {{anomaly-job}} results may propagate field values that contain sensitive information from the source indices to the results.
::::

### {{kib}} security [kib-security]

::::{important}
Granting `All` or `Read` {{kib}} feature privilege for {{ml-app}} will also grant the role the equivalent feature privileges to certain types of {{kib}} saved objects, namely data views, dashboards, discover sessions, and visualizations as well as {{ml}} job, trained model and module saved objects.
::::

#### Feature visibility in Spaces [kib-visibility-spaces]

In {{kib}}, the {{ml-features}} must be visible in your [space](../../deploy-manage/manage-spaces.md). To manage which features are visible in your space, go to the **Spaces** management page using the navigation menu or the [global search field](../find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/machine-learning-spaces.jpg
:alt: Manage spaces in {{kib}}
:screenshot:
:::

In addition to index privileges, source {{data-sources}} must also exist in the same space as your {{ml}} jobs. You can configure these under **{{data-sources-caps}}**. To open **{{data-sources-caps}}**, find **{{stack-manage-app}}** > **{{kib}}** in the main menu, or use the [global search field](../find-and-organize/find-apps-and-objects.md).

Each {{ml}} job and trained model can be assigned to all, one, or multiple spaces. This can be configured in **Machine Learning**. To open **Machine Learning**, find the page in the main menu, or use the [global search field](../find-and-organize/find-apps-and-objects.md). You can edit the spaces that a job or model is assigned to by clicking the icons in the **Spaces** column.

:::{image} /explore-analyze/images/machine-learning-assign-job-spaces.jpg
:alt: Assign machine learning jobs to spaces
:screenshot:
:::

#### {{kib}} user [kib-security-privileges]

Within a {{kib}} space, for full access to the {{ml-features}}, you must have:

* `Machine Learning: All` {{kib}} privileges
* `Data Views Management: All` {{kib}} feature privileges
* `read`, and `view_index_metadata` index privileges on your source indices
* {{data-sources}} for your source indices
* {{data-sources}}, `read`, `manage`, and `index` index privileges on destination indices (for {{dfanalytics-jobs}} only)

Within a {{kib}} space, for read-only access to the {{ml-features}}, you must have:

* `Machine Learning: Read` {{kib}} privileges
* {{data-sources}} for your source indices
* `read` index privilege on your source indices
* {{data-sources}} and `read` index privileges on destination indices (for {{dfanalytics-jobs}} only)

::::{important}
A user who has full or read-only access to {{ml-features}} within a given {{kib}} space can view the results of *all* {{anomaly-jobs}} that are visible in that space, even if they do not have access to the source indices of those jobs. You must carefully consider who is given access to {{ml-features}}, as {{anomaly-job}} results may propagate field values that contain sensitive information from the source indices to the results.
::::

::::{note}
{{data-sources-cap}} can be automatically created when creating a {{dfanalytics-job}}.
::::

For access to use {{ml}} APIs via *Dev Tools* in {{kib}}, set the {{es}} security privileges and grant access to `machine_learning_admin` or `machine_learning_user` built-in roles.

#### {{data-viz}} feature [upload-file-security-privileges]

Within a {{kib}} space, to upload and import files in the **{{data-viz}}**, you must have:

* `Machine Learning: Read` or `Discover: All` {{kib}} feature privileges
* `Data Views Management: All` {{kib}} feature privileges
* `ingest_admin` built-in role, or `manage_ingest_pipelines` cluster privilege
* `create`, `create_index`, `manage` and `read` index privileges for destination indices

For more information, see [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) and [{{kib}} privileges](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Export and import {{ml-jobs}} [move-jobs]

Export and import [{{anomaly-detect}} jobs](#move-anomaly-detection-jobs) and [{{dfanalytics}} jobs](#move-dataframe-analytics-jobs) to transfer them between clusters or environments, for example, from a test environment to production.

:::::{note}
The exported files contain configuration details only; they do not contain the {{ml}} models.
:::::

### Export and import {{anomaly-detect}} jobs [move-anomaly-detection-jobs]

#### Prerequisites

- If your {{anomaly-jobs}} use [custom rules](/explore-analyze/machine-learning/anomaly-detection/ml-configuring-detector-custom-rules.md) with filter lists, the filter lists must exist; otherwise, the import fails. To create filter lists, use {{kib}} or the [create filters API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-filter)
- If your {{anomaly-jobs}} were associated with [calendars](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-calendars), you must create the calendar in the new environment and add your imported jobs to the calendar. Use {{kib}} or the [create calendars](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-calendar), [add events to calendar](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-post-calendar-events), and [add jobs to calendar](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-calendar-job) APIs.

#### Export {{anomaly-detect}} jobs

1. To navigate to **{{anomaly-jobs-cap}}**, use the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Export jobs**.
3. Select the jobs, then click **Export** to download the job definition file.

#### Import {{anomaly-detect}} jobs

1. To navigate to **{{anomaly-jobs-cap}}**, use the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Import jobs**.
3. Upload the file that defines the {{anomaly-job}}.
4. Enter a job ID and click **Import**.

:::::{important}
{{anomaly-jobs-cap}} can be imported even if their {{data-sources}} or underlying indices are missing. In these cases, warnings are displayed, but the import is still allowed. Any issues raised by these warnings can be resolved later by adding the missing {{data-sources}}.
:::::

After importing an {{anomaly-job}}, you must run it so that it can learn from your current data and build a model that reflects the new environment.

### Export and import {{dfanalytics}} jobs [move-dataframe-analytics-jobs]

:::::{note}
For {{dfanalytics}}, trained models are portable and can be transferred between clusters as described in [Exporting and importing models](/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md#export-import).
:::::

#### Prerequisites

- {{dfanalytics-cap}} jobs require their source index to exist before they can be imported. If the source index is missing, the import fails.

#### Export {{dfanalytics}} jobs

1. To navigate to **{{dfanalytics-cap}}**, use the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Export jobs**.
3. Select the jobs, then click **Export** to download the job definition file.

#### Import {{dfanalytics}} jobs

1. To navigate to **{{dfanalytics-cap}}**, use the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Import jobs**.
3. Select the file that defines the {{dfanalytics}} job.
4. Enter a job ID and a destination index, then click **Import**.

