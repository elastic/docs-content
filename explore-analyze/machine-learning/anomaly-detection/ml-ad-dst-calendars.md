---
navigation_title: Daylight saving time calendars
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Daylight saving time calendars [ml-ad-dst-calendars]

Twice a year in the spring and fall, many countries change their clocks to make better use of the daylight. These clock adjustments can trigger a burst of false positive anomalies, because the {{ml}} models need a few days to adapt to the new data patterns after the shift.

A *DST calendar* is a specialized [calendar](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-calendars) that automatically generates the scheduled events needed to tell {{anomaly-jobs}} about an upcoming daylight saving time (DST) transition for a specific time zone. {{anomaly-jobs-cap}} that subscribe to a DST calendar are not ill-affected by the transition and do not produce spurious results.

## Create a DST calendar [ml-ad-dst-calendars-create]

To make sure {{anomaly-jobs}} adjust correctly for DST, create a DST calendar for your time zone and associate it with your jobs or job groups.

1. In {{kib}}, go to **Machine Learning > Anomaly Detection > Settings**. Alongside the regular **Calendars** panel, a **DST Calendars** panel lets you create and manage DST calendars separately.

    :::{image} /explore-analyze/images/machine-learning-ml-dst-calendar-settings.png
    :alt: The Anomaly Detection Settings page with separate Calendars and DST Calendars panels
    :screenshot:
    :::

2. Select **Create** in the **DST Calendars** panel, then select the time zone of your data. This might not be the time zone that you are in, but it must be the time zone from which the data in the index originated. The wizard automatically generates the calendar events that force a time shift for the associated jobs, based on that time zone's DST rules.

    :::{image} /explore-analyze/images/machine-learning-ml-dst-calendar-wizard.png
    :alt: The create new DST calendar wizard, showing the calendar ID, jobs, groups, time zone of data, and generated shift events
    :screenshot:
    :::

3. Associate the calendar with existing jobs or groups. If you have multiple jobs that require the same DST calendar, put them in a common group and assign the calendar to that group instead of to each job individually.

4. Alternatively, associate a DST calendar with a new job while you create it. In the **Additional settings** of the **Job details** step of the job creation wizard, the **DST Calendars** field lets you select an existing DST calendar or a group that already has one assigned.

    :::{image} /explore-analyze/images/machine-learning-ml-dst-calendar-job-details.png
    :alt: The Additional settings section of the Job details step, showing separate Calendars and DST Calendars fields
    :screenshot:
    :::

## Managing multiple time zones [ml-ad-dst-calendars-multiple-timezones]

If your data spans a country or region with multiple time zones and complex DST rules, such as Australia or the United States, you might need to create several DST calendars and multiple {{anomaly-jobs}}, one per time zone. Use a filter query in the [{{dfeed}} configuration](ml-ad-run-jobs.md#ml-ad-datafeeds) to route data from each time zone to its corresponding job.

For example, to handle data from Australia you would need three jobs, because DST is observed differently across Australian states and territories:

* Regions shifting time by 1 hour: Australian Capital Territory, Jervis Bay Territory, New South Wales (except Lord Howe Island), Norfolk Island, South Australia, Tasmania, and Victoria.
* Region shifting time by 30 minutes: Lord Howe Island.
* Regions not observing DST: Western Australia, Queensland, and Northern Territory.

Each job subscribes to the DST calendar that matches the DST rules of the time zone it analyzes.
