---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/categorize-logs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Categorize log entries [categorize-logs]

Application log events are often unstructured and contain variable data. Many log messages are the same or very similar, so classifying them can reduce millions of log lines into just a few categories.

The **Categories** page enables you to identify patterns in your log events quickly. Instead of manually identifying similar logs, the logs categorization view lists log events that have been grouped based on their messages and formats so that you can take action quicker.

::::{note}
This feature makes use of {{ml}} {{anomaly-jobs}}. To set up jobs, you must have `all` {{kib}} feature privileges for **{{ml-app}}**. Users that have full or read-only access to {{ml-features}} within a {{kib}} space can view the results of *all* {{anomaly-jobs}} that are visible in that space, even if they do not have access to the source indices of those jobs. You must carefully consider who is given access to {{ml-features}}; {{anomaly-job}} results may propagate field values that contain sensitive information from the source indices to the results. For more details, refer to [Set up {{ml-features}}](/explore-analyze/machine-learning/setting-up-machine-learning.md).
::::

## Create log categories [create-log-categories]

Create a {{ml}} job to categorize log messages automatically. {{ml-cap}} observes the static parts of the message, clusters similar messages, classifies them into message categories, and detects unusually high message counts in the categories.

1. Open the **Categories** page by finding `Logs / Categories` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). You are prompted to use {{ml}} to create log rate categorizations.
2. Choose a time range for the {{ml}} analysis. By default, the {{ml}} job analyzes log messages no older than four weeks and continues indefinitely.
3. Add the indices that contain the logs you want to examine. By default, Machine Learning analyzes messages in all log indices that match the patterns set in the **logs sources** advanced setting. To open **Advanced settings**, find it in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
4. Click **Create ML job**. This creates and runs the job. It takes a few minutes for the {{ml}} robots to collect the necessary data. After the job has processed the data, you can view its results.

::::{note}
:applies_to: stack: ga 9.2

Log categorization {{ml}} jobs retain results for 120 days by default. Modify the `results_retention_days` setting to change this period.
::::


## Analyze log categories [analyze-log-categories]

The **Categories** page lists all the log categories from the selected indices. You can filter the categories by indices. The screenshot below shows the categories from the `elastic.agent` log.

:::{image} /solutions/images/observability-log-categories.jpg
:alt: Log categories
:screenshot:
:::

The category row contains the following information:

* message count: shows how many messages belong to the given category.
* trend: indicates how the occurrence of the messages changes in time.
* category name: it is the name of the category and is derived from the message text.
* datasets: the name of the datasets where the categories are present.
* maximum anomaly score: the highest anomaly score in the category.

To view a log message for a particular category, click the arrow at the end of the row. To further examine it, click **View in Discover** or **View in context**

:::{image} /solutions/images/observability-log-opened.png
:alt: Opened log category
:screenshot:
:::

For more information about categorization, go to [Detecting anomalous categories of data](/explore-analyze/machine-learning/anomaly-detection/ml-configuring-categories.md).
