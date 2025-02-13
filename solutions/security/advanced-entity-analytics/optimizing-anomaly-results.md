---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/tuning-anomaly-results.html
  - https://www.elastic.co/guide/en/serverless/current/security-tuning-anomaly-results.html
---

# Optimizing anomaly results [tuning-anomaly-results]

To gain clearer insights into real threats, you can tune the anomaly results. The following procedures help to reduce the number of false positives:

* [Tune results for rare applications and processes](#rarely-used-processes)
* [Define an anomaly threshold for a job](#define-rule-threshold)


## Filter out anomalies from rarely used applications and processes [rarely-used-processes]

When anomalies include results from a known process that only runs occasionally, you can filter out the unwanted results.

For example, to filter out results from a housekeeping process, named `maintenanceservice.exe`, that only executes occasionally you need to:

1. [Create a filter list](#create-fiter-list)
2. [Add the filter to the relevant job](#add-job-filter)
3. [Clone and rerun the job](#clone-job) (optional)


### Create a filter list [create-fiter-list]

1. Find **Machine Learning** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Anomaly Detection**, select **Settings**.
3. Click **Filter Lists** and then **New**.

    The **Create new filter list** pane is displayed.

4. Enter a filter list ID.
5. Enter a description for the filter list (optional).
6. Click **Add item**.
7. In the **Items** textbox, enter the name of the process for which you want to filter out anomaly results (`maintenanceservice.exe` in our example).

    :::{image} ../../../images/security-filter-add-item.png
    :alt: filter add item
    :class: screenshot
    :::

8. Click **Add** and then **Save**.

    The new filter appears in the Filter List and can be added to relevant jobs.



### Add the filter to the relevant job [add-job-filter]

1. Find **Machine Learning** in the navigation menu.
2. Under **Anomaly Detection**, select **Anomaly Explorer**.
3. Navigate to the job results for which the filter is required. If the job results are not listed, click **Edit job selection** and select the relevant job.
4. In the **actions** column, click the gear icon and then select *Configure rules*.

    The **Create Rule** window is displayed.

    :::{image} ../../../images/security-rule-scope.png
    :alt: rule scope
    :class: screenshot
    :::

5. Select:

    1. *Add a filter list to limit where the rule applies*.
    2. The *WHEN* statement for the relevant detector (`process.name` in our example).
    3. The *IS IN* statement.
    4. The filter you created as part of the [Create a filter list](#create-fiter-list) procedure.

        ::::{tip}
        For more information, see [Customizing detectors with custom rules](../../../explore-analyze/machine-learning/anomaly-detection/ml-configuring-detector-custom-rules.md).
        ::::

6. Click **Save**.

::::{note}
Changes to rules only affect new results. All anomalies found by the job before the filter was added are still displayed.
::::



### Clone and rerun the job [clone-job]

If you want to remove all the previously detected results for the process, you must clone and run the cloned job.

::::{important}
Running the cloned job can take some time. Only run the job after you have completed all job rule changes.
::::


1. Find **Machine Learning** in the navigation menu.
2. Under **Anomaly Detection**, select **Jobs**.
3. Navigate to the job for which you configured the rule.
4. Optionally, expand the job row and click **JSON** to verify the configured filter appears under `custom rules` in the JSON code.
5. In the **actions** column, click the more (three dots) icon and select *Clone job*.

    The **Configure datafeed** page is displayed.

6. Click **Data Preview** and check the data is displayed without errors.
7. Click **Next** until the **Job details** page is displayed.
8. Enter a Job ID for the cloned job that indicates it is an iteration of the original one. For example, append a number or a username to the original job name, such as `windows-rare-network-process-2`.

    :::{image} ../../../images/security-cloned-job-details.png
    :alt: cloned job details
    :class: screenshot
    :::

9. Click **Next** and check the job validates without errors. You can ignore warnings about multiple influencers.
10. Click **Next** and then **Create job**.

    The **Start <job name>** window is displayed.

    :::{image} ../../../images/security-start-job-window.png
    :alt: start job window
    :class: screenshot
    :::

11. Select the point of time from which the job will analyze anomalies.
12. Click **Start**.

    After a while, results will start to appear on the **Anomaly Explorer** page.



## Define an anomaly threshold for a job [define-rule-threshold]

Certain jobs use a high-count function to look for unusual spikes in process events. For some processes, a burst of activity is a normal, such as automation and housekeeping jobs running on server fleets. However, sometimes a high-delta event count is unlikely to be the result of routine behavior. In these cases, you can define a minimum threshold for when a high-event count is considered an anomaly.

Depending on your anomaly detection results, you may want to set a minimum event count threshold for the `packetbeat_dns_tunneling` job:

1. Find **Machine Learning** in the navigation menu.
2. Under **Anomaly Detection**, select **Anomaly Explorer**.
3. Navigate to the job results for the `packetbeat_dns_tunneling` job. If the job results are not listed, click **Edit job selection** and select `packetbeat_dns_tunneling`.
4. In the **actions** column, click the gear icon and then select *Configure rules*.

    The **Create Rule** window is displayed.

    :::{image} ../../../images/security-ml-rule-threshold.png
    :alt: ml rule threshold
    :class: screenshot
    :::

5. Select *Add numeric conditions for when the rule applies* and the following `when` statement:

    *WHEN actual IS GREATER THAN <X>*

    Where `<X>` is the threshold above which anomalies are detected.

6. Click **Save**.
7. To apply the new threshold, rerun the job by selecting **Actions** → **Start datafeed** on the **Anomaly Detection Jobs** page.
