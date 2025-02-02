# Optimizing anomaly results [security-tuning-anomaly-results]

To gain clearer insights into real threats, you can tune the anomaly results. The following procedures help to reduce the number of false positives:

* [Tune results for rare applications and processes](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#rarely-used-processes)
* [Define an anomaly threshold for a job](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#define-rule-threshold)


## Filter out anomalies from rarely used applications and processes [rarely-used-processes]

When anomalies include results from a known process that only runs occasionally, you can filter out the unwanted results.

For example, to filter out results from a housekeeping process, named `maintenanceservice.exe`, that only executes occasionally you need to:

1. [Create a filter list](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#create-fiter-list)
2. [Add the filter to the relevant job](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#add-job-filter)
3. [Clone and rerun the job](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#clone-job) (optional)


### Create a filter list [create-fiter-list]

1. Go to **Machine learning** → **Anomaly Detection** → **Settings**.
2. Click **Filter Lists** and then **Create**.

    The **Create new filter list** pane is displayed.

3. Enter a filter list ID.
4. Enter a description for the filter list (optional).
5. Click **Add item**.
6. In the **Items** textbox, enter the name of the process for which you want to filter out anomaly results (`maintenanceservice.exe` in our example).

    :::{image} ../../../images/serverless--detections-machine-learning-filter-add-item.png
    :alt:  detections machine learning filter add item
    :class: screenshot
    :::

7. Click **Add** and then **Save**.

    The new filter appears in the Filter List and can be added to relevant jobs.



### Add the filter to the relevant job [add-job-filter]

1. Go to **Machine learning** → **Anomaly Detection** → **Anomaly Explorer**.
2. Navigate to the job results for which the filter is required. If the job results are not listed, click **Edit job selection** and select the relevant job.
3. In the **actions** column, click the gear icon and then select *Configure rules*.

    The **Create Rule** window is displayed.

    :::{image} ../../../images/serverless--detections-machine-learning-rule-scope.png
    :alt:  detections machine learning rule scope
    :class: screenshot
    :::

4. Select:

    1. *Add a filter list to limit where the rule applies*.
    2. The *WHEN* statement for the relevant detector (`process.name` in our example).
    3. The *IS IN* statement.
    4. The filter you created as part of the [Create a filter list](../../../solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md#create-fiter-list) procedure.

        ::::{tip}
        For more information, see [Customizing detectors with custom rules](../../../explore-analyze/machine-learning/anomaly-detection/ml-configuring-detector-custom-rules.md).

        ::::

5. Click **Save**.

::::{note}
Changes to rules only affect new results. All anomalies found by the job before the filter was added are still displayed.

::::



### Clone and rerun the job [clone-job]

If you want to remove all the previously detected results for the process, you must clone and run the cloned job.

::::{important}
Running the cloned job can take some time. Only run the job after you have completed all job rule changes.

::::


1. Go to **Machine learning** → **Anomaly Detection** → **Jobs**.
2. Navigate to the job for which you configured the rule.
3. Optionally, expand the job row and click **JSON** to verify the configured filter appears under `custom rules` in the JSON code.
4. In the **actions** column, click the options menu (![Options menu](../../../images/serverless-boxesHorizontal.svg "")) and select **Clone job**.

    The **Configure datafeed** page is displayed.

5. Click **Data Preview** and check the data is displayed without errors.
6. Click **Next** until the **Job details** page is displayed.
7. Enter a Job ID for the cloned job that indicates it is an iteration of the original one. For example, append a number or a username to the original job name, such as `windows-rare-network-process-2`.

    :::{image} ../../../images/serverless--detections-machine-learning-cloned-job-details.png
    :alt:  detections machine learning cloned job details
    :class: screenshot
    :::

8. Click **Next** and check the job validates without errors. You can ignore warnings about multiple influencers.
9. Click **Next** and then **Create job**.

    The **Start <job name>** window is displayed.

    :::{image} ../../../images/serverless--detections-machine-learning-start-job-window.png
    :alt:  detections machine learning start job window
    :class: screenshot
    :::

10. Select the point of time from which the job will analyze anomalies.
11. Click **Start**.

    After a while, results will start to appear on the **Anomaly Explorer** page.



## Define an anomaly threshold for a job [define-rule-threshold]

Certain jobs use a high-count function to look for unusual spikes in process events. For some processes, a burst of activity is a normal, such as automation and housekeeping jobs running on server fleets. However, sometimes a high-delta event count is unlikely to be the result of routine behavior. In these cases, you can define a minimum threshold for when a high-event count is considered an anomaly.

Depending on your anomaly detection results, you may want to set a minimum event count threshold for the `packetbeat_dns_tunneling` job:

1. Go to **Machine learning** → **Anomaly Detection** → **Anomaly Explorer**.
2. Navigate to the job results for the `packetbeat_dns_tunneling` job. If the job results are not listed, click **Edit job selection** and select `packetbeat_dns_tunneling`.
3. In the **actions** column, click the gear icon and then select **Configure rules**.

    The **Create Rule** window is displayed.

    :::{image} ../../../images/serverless--detections-machine-learning-ml-rule-threshold.png
    :alt:  detections machine learning ml rule threshold
    :class: screenshot
    :::

4. Select **Add numeric conditions for when the rule applies** and the following `when` statement:

    *WHEN actual IS GREATER THAN <X>*

    Where `<X>` is the threshold above which anomalies are detected.

5. Click **Save**.
6. To apply the new threshold, rerun the job (**Job Management** → **Actions** → **Start datafeed**).
