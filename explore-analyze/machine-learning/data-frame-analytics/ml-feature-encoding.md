---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-feature-encoding.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Feature encoding [ml-feature-encoding]

{{ml-cap}} models can only work with numerical values. For this reason, it is necessary to transform the categorical values of the relevant features into numerical ones. This process is called *feature encoding*.

{{dfanalytics-cap}} automatically performs feature encoding. The input data is pre-processed with the following encoding techniques:

* one-hot encoding: Assigns vectors to each category. The vector represent whether the corresponding feature is present (1) or not (0).
* target-mean encoding: Replaces categorical values with the mean value of the target variable.
* frequency encoding: Takes into account how many times a given categorical value is present in relation with a feature.

When the model makes predictions on new data, the data needs to be processed in the same way it was trained. {{ml-cap}} model inference in the {{stack}} does this automatically, so the automatically applied encodings are used in each call for inference. Refer to {{infer}} for [{{classification}}](ml-dfa-classification.md#ml-inference-class) and [{{regression}}](ml-dfa-regression.md#ml-inference-reg).

[{{feat-imp-cap}}](ml-feature-importance.md) is calculated for the original categorical fields, not the automatically encoded features.
