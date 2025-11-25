---
navigation_title: Limitations
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfa-limitations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Data frame analytics limitations [ml-dfa-limitations]

The following limitations and known problems apply to the Elastic {{dfanalytics}} feature. The limitations are grouped into the following categories:

* [Platform limitations](#dfa-platform-limitations) are related to the platform that hosts the {{ml}} feature of the {{stack}}.
* [Configuration limitations](#dfa-config-limitations) apply to the configuration process of the {{dfanalytics-jobs}}.
* [Operational limitations](#dfa-operational-limitations) affect the behavior of the {{dfanalytics-jobs}} that are running.

## Platform limitations [dfa-platform-limitations]

### CPU scheduling improvements apply to Linux and MacOS only [dfa-scheduling-priority]

When there are many {{ml}} jobs running at the same time and there are insufficient CPU resources, the JVM performance must be prioritized so search and indexing latency remain acceptable. To that end, when CPU is constrained on Linux and MacOS environments, the CPU scheduling priority of native analysis processes is reduced to favor the {{es}} JVM. This improvement does not apply to Windows environments.

## Configuration limitations [dfa-config-limitations]

### {{ccs-cap}} is not supported [dfa-ccs-limitations]

{{ccs-cap}} is not supported for {{dfanalytics}}.

### Nested fields are not supported [dfa-nested-fields-limitations]

Nested fields are not supported for {{dfanalytics-jobs}}. These fields are ignored during the analysis. If a nested field is selected as the dependent variable for {{classification}} or {{reganalysis}}, an error occurs.

### {{dfanalytics-jobs-cap}} cannot be updated [dfa-update-limitations]

You cannot update {{dfanalytics}} configurations. Instead, delete the {{dfanalytics-job}} and create a new one.

### {{dfanalytics-cap}} memory limitation [dfa-dataframe-size-limitations]

{{dfanalytics-cap}} can only perform analyses that fit into the memory available for {{ml}}. Overspill to disk is not currently possible. For general {{ml}} settings, see [{{ml-cap}} settings in {{es}}](elasticsearch://reference/elasticsearch/configuration-reference/machine-learning-settings.md).

When you create a {{dfanalytics-job}} and the inference step of the process fails due to the model is too large to fit into JVM, follow the steps in [this GitHub issue](https://github.com/elastic/elasticsearch/issues/76093) for a workaround.

### {{dfanalytics-jobs-cap}} cannot use more than 2^32^ documents for training [dfa-training-docs]

A {{dfanalytics-job}} that would use more than 2^32^ documents for training cannot be started. The limitation applies only for documents participating in training the model. If your source index contains more than 2^32^ documents, set the `training_percent` to a value that represents less than 2^32^ documents.

### Trained models created in 7.8 are not backwards compatible [dfa-inference-bwc]

Trained models created in version 7.8.0 are not backwards compatible with older node versions. In a mixed cluster environment, all nodes must be at least 7.8.0 to use a model created on a 7.8.0 node.

## Operational limitations [dfa-operational-limitations]

### Deleting a {{dfanalytics-job}} does not delete the destination index [dfa-deletion-limitations]

The [delete {{dfanalytics-job}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-delete-data-frame-analytics) does not delete the destination index that contains the annotated data of the {{dfanalytics}}. That index must be deleted separately.

### {{dfanalytics-jobs-cap}} runtime may vary [dfa-time-limitations]

The runtime of {{dfanalytics-jobs}} depends on numerous factors, such as the number of data points in the data set, the type of analytics, the number of fields that are included in the analysis, the supplied [hyperparameters](hyperparameters.md), the type of analyzed fields, and so on. For this reason, a general runtime value that applies to all or most of the situations does not exist. The runtime of a {{dfanalytics-job}} may take from a couple of minutes up to many hours in extreme cases.

The runtime increases with an increasing number of analyzed fields in a nearly linear fashion. For data sets of more than 100,000 points, start with a low training percent. Run a few {{dfanalytics-jobs}} to see how the runtime scales with the increased number of data points and how the quality of results scales with an increased training percentage.

### {{dfanalytics-jobs-cap}} may restart after an {{es}} upgrade [dfa-restart]

A {{dfanalytics-job}} may be restarted from the beginning in the following cases:

* the job is in progress during an {{es}} update,
* the job resumes on a node with a higher version,
* the results format has changed requiring different mappings in the destination index.

If any of these conditions applies, the destination index of the {{dfanalytics-job}} is deleted and the job starts again from the beginning – regardless of the phase where the job was in.

### Documents with values of multi-element arrays in analyzed fields are skipped [dfa-multi-arrays-limitations]

If the value of an analyzed field (field that is subect of the {{dfanalytics}}) in a document is an array with more than one element, the document that contains this field is skipped during the analysis.

### {{oldetection-cap}} field types [dfa-od-field-type-docs-limitations]

{{oldetection-cap}} requires numeric or boolean data to analyze. The algorithms don’t support missing values, therefore fields that have data types other than numeric or boolean are ignored. Documents where included fields contain missing values, null values, or an array are also ignored. Therefore a destination index may contain documents that don’t have an {{olscore}}. These documents are still reindexed from the source index to the destination index, but they are not included in the {{oldetection}} analysis and therefore no {{olscore}} is computed.

### {{regression-cap}} field types [dfa-regression-field-type-docs-limitations]

{{regression-cap}} supports fields that are numeric, boolean, text, keyword and ip. It is also tolerant of missing values. Fields that are supported are included in the analysis, other fields are ignored. Documents where included fields contain an array are also ignored. Documents in the destination index that don’t contain a results field are not included in the {{reganalysis}}.

### {{classification-cap}} field types [dfa-classification-field-type-docs-limitations]

{{classification-cap}} supports fields that have numeric, boolean, text, keyword, or ip data types. It is also tolerant of missing values. Fields that are supported are included in the analysis, other fields are ignored. Documents where included fields contain an array are also ignored. Documents in the destination index that don’t contain a results field are not included in the {{classanalysis}}.

### Imbalanced class sizes affect {{classification}} performance [dfa-classification-imbalanced-classes]

If your training data is very imbalanced, {{classanalysis}} may not provide good predictions. Try to avoid highly imbalanced situations. We recommend having at least 50 examples of each class and a ratio of no more than 10 to 1 for the majority to minority class labels in the training data. If your training data set is very imbalanced, consider downsampling the majority class, upsampling the minority class, or gathering more data.

### Deeply nested objects affect {{infer}} performance [dfa-inference-nested-limitation]

If the data that you run inference against contains documents that have a series of combinations of dot delimited and nested fields (for example: `{"a.b": "c", "a": {"b": "c"},...}`), the performance of the operation might be slightly slower. Consider using as simple mapping as possible for the best performance profile.

### Analytics runtime performance may significantly slow down with {{feat-imp}} computation [dfa-feature-importance-limitation]

For complex models (such as those with many deep trees), the calculation of {{feat-imp}} takes significantly more time. If a reduction in runtime is important to you, try strategies such as disabling {{feat-imp}}, reducing the amount of training data (for example by decreasing the training percentage), setting [hyperparameter](hyperparameters.md) values, or only selecting fields that are relevant for analysis.
