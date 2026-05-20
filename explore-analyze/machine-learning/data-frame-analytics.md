---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfanalytics.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-ml-dfanalytics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
  - id: kibana
---

# Data frame analytics [ml-dfanalytics]

::::{important}
Using {{dfanalytics}} requires source data to be structured as a two dimensional "tabular" data structure, in other words a {{dataframe}}. [Transforms](../transforms.md) enable you to create {{dataframes}} which can be used as the source for {{dfanalytics}}.
::::

{{dfanalytics-cap}} enable you to perform different analyses of your data and annotate it with the results. Consult [Setup and security](setting-up-machine-learning.md) to learn more about the license and the security privileges that are required to use {{dfanalytics}}.

* [Overview](data-frame-analytics/ml-dfa-overview.md)
* [*Finding outliers*](data-frame-analytics/ml-dfa-finding-outliers.md)
* [*Predicting numerical values with {{regression}}*](data-frame-analytics/ml-dfa-regression.md)
* [*Predicting classes with {{classification}}*](data-frame-analytics/ml-dfa-classification.md)
* [*Advanced concepts*](data-frame-analytics/ml-dfa-concepts.md)
* [*API quick reference*](data-frame-analytics/ml-dfanalytics-apis.md)
* [*Resources*](data-frame-analytics/ml-dfa-resources.md)
