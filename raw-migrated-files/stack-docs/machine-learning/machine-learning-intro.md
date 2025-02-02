# What is Elastic {{ml-app}}? [machine-learning-intro]

{{ml-cap}} features analyze your data and generate models for its patterns of behavior. The type of analysis that you choose depends on the questions or problems you want to address and the type of data you have available.


## Unsupervised {{ml}} [machine-learning-unsupervised] 

There are two types of analysis that can deduce the patterns and relationships within your data without training or intervention: *{{anomaly-detect}}* and *{{oldetection}}*.

[{{anomaly-detect-cap}}](../../../explore-analyze/machine-learning/anomaly-detection.md) requires time series data. It constructs a probability model and can run continuously to identify unusual events as they occur. The model evolves over time; you can use its insights to forecast future behavior.

[{{oldetection-cap}}](../../../explore-analyze/machine-learning/data-frame-analytics/ml-dfa-finding-outliers.md) does not require time series data. It is a type of {{dfanalytics}} that identifies unusual points in a data set by analyzing how close each data point is to others and the density of the cluster of points around it. It does not run continuously; it generates a copy of your data set where each data point is annotated with an {{olscore}}. The score indicates the extent to which a data point is an outlier compared to other data points.


## Supervised {{ml}} [machine-learning-supervised] 

There are two types of {{dfanalytics}} that require training data sets: *{{classification}}* and *{{regression}}*.

In both cases, the result is a copy of your data set where each data point is annotated with predictions and a trained model, which you can deploy to make predictions for new data. For more information, refer to [Introduction to supervised learning](../../../explore-analyze/machine-learning/data-frame-analytics/ml-dfa-overview.md#ml-supervised-workflow).

[{{classification-cap}}](../../../explore-analyze/machine-learning/data-frame-analytics/ml-dfa-classification.md) learns relationships between your data points in order to predict discrete categorical values, such as whether a DNS request originates from a malicious or benign domain.

[{{regression-cap}}](../../../explore-analyze/machine-learning/data-frame-analytics/ml-dfa-regression.md) learns relationships between your data points in order to predict continuous numerical values, such as the response time for a web request.

