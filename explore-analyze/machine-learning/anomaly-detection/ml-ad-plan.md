---
navigation_title: Plan your analysis
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-plan.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Plan your analysis [ml-ad-plan]

The {{ml-features}} in {{stack}} enable you to seek anomalies in your data in many different ways. Using [proprietary {{ml}} algorithms](ml-ad-algorithms.md), the following circumstances are detected:

* Anomalies related to temporal deviations in values, counts, or frequencies
* Anomalies related to unusual locations in geographic data
* Statistical rarity
* Unusual behaviors for a member of a population

Automated periodicity detection and quick adaptation to changing data ensure that you don’t need to specify algorithms, models, or other data science-related configurations in order to get the benefits of {{ml}}.

When you are deciding which type of {{anomaly-detect}} to use, the most important considerations are the data sets that you have available and the type of behavior you want to detect.

If you are uncertain where to begin, {{kib}} can recognize certain types of data and suggest useful {{anomaly-jobs}}. Likewise, some {{agent}} integrations include {{anomaly-job}} configuration information, dashboards, searches, and visualizations that are customized to help you analyze your data.

For the full list of functions that you can use in your {{anomaly-jobs}}, see [*Function reference*](ml-functions.md). For a list of the preconfigured jobs, see [Supplied configurations](ootb-ml-jobs.md).
