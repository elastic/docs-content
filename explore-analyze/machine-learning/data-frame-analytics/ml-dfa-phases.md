---
navigation_title: "How {{dfanalytics-jobs}} work"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfa-phases.html
---



# How data frame analytics jobs work [ml-dfa-phases]

A {{dfanalytics-job}} is essentially a persistent {{es}} task. During its life cycle, it goes through four or five main phases depending on the analysis type:

* reindexing,
* loading data,
* analyzing,
* writing results,
* inference ({{regression}} and {{classification}} only).

Let’s take a look at the phases one-by-one.

## Reindexing [ml-dfa-phases-reindex]

During the reindexing phase the documents from the source index or indices are copied to the destination index. If you want to define settings or mappings, create the index before you start the job. Otherwise, the job creates it using default settings.

Once the destination index is built, the {{dfanalytics-job}} task calls the {{es}} [Reindex API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) to launch the reindexing task.

## Loading data [ml-dfa-phases-load]

After the reindexing is finished, the job fetches the needed data from the destination index. It converts the data into the format that the analysis process expects, then sends it to the analysis process.

## Analyzing [ml-dfa-phases-analyze]

In this phase, the job generates a {{ml}} model for analyzing the data. The specific phases of analysis vary depending on the type of {{dfanalytics-job}}.

{{oldetection-cap}} jobs have a single analysis phase called `computing_outliers`, in which they identify outliers in the data.

{{regression-cap}} and {{classification}} jobs have four analysis phases:

1. `feature_selection`: Identifies which of the supplied fields are most relevant for predicting the dependent variable.
2. `coarse_parameter_search`: Identifies initial values for undefined hyperparameters.
3. `fine_tuning_parameters`: Identifies final values for undefined hyperparameters. See [hyperparameter optimization](hyperparameters.md).
4. `final_training`: Trains the {{ml}} model.

## Writing results [ml-dfa-phases-write]

After the loaded data is analyzed, the analysis process sends back the results. Only the additional fields that the analysis calculated are written back, the ones that have been loaded in the loading data phase are not. The {{dfanalytics-job}} matches the results with the data rows in the destination index, merges them, and indexes them back to the destination index.

## {{infer-cap}} [ml-dfa-phases-inference]

This phase exists only for {{regression}} and {{classification}} jobs. In this phase, the job validates the trained model against the test split of the data set.

Finally, after all phases are completed, the task is marked as completed and the {{dfanalytics-job}} stops. Your data is ready to be evaluated.