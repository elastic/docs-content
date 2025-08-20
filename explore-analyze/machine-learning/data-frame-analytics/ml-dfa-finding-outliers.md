---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfa-finding-outliers.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Finding outliers [ml-dfa-finding-outliers]

{{oldetection-cap}} is identification of data points that are significantly different from other values in the data set. For example, outliers could be errors or unusual entities in a data set. {{oldetection-cap}} is an unsupervised {{ml}} technique, there is no need to provide training data.

::::{important}
{{oldetection-cap}} is a batch analysis, it runs against your data once. If new data comes into the index, you need to do the analysis again on the altered data.
::::

## {{oldetection-cap}} algorithms [dfa-outlier-algorithms]

In the {{stack}}, we use an ensemble of four different distance and density based {{oldetection}} methods:

* distance of Kth nearest neighbor: computes the distance of the data point to its Kth nearest neighbor where K is a small number and usually independent of the total number of data points.
* distance of K-nearest neighbors: calculates the average distance of the data points to their nearest neighbors. Points with the largest average distance will be the most outlying.
* local outlier factor (`lof`): takes into account the distance of the points to their K nearest neighbors and also the distance of these neighbors to their neighbors.
* local distance-based outlier factor (`ldof`): is a ratio of two measures: the first computes the average distance of the data point to its K nearest neighbors; the second computes the average of the pairwise distances of the neighbors themselves.

You don’t need to select the methods or provide any parameters, but you can override the default behavior if you like. *Distance based methods* assume that normal data points remain closer or similar in value while outliers are located far away or significantly differ in value. The drawback of these methods is that they don’t take into account the density variations of a data set. *Density based methods* are used for mitigating this problem.

The four algorithms don’t always agree on which points are outliers. By default, {{oldetection}} jobs use all these methods, then normalize and combine their results and give every data point in the index an {{olscore}}. The {{olscore}} ranges from 0 to 1, where the higher number represents the chance that the data point is an outlier compared to the other data points in the index.

### Feature influence [dfa-feature-influence]

Feature influence – another score calculated while detecting outliers – provides a relative ranking of the different features and their contribution towards a point being an outlier. This score allows you to understand the context or the reasoning on why a certain data point is an outlier.

## 1. Define the problem [dfa-outlier-detection-problem]

{{oldetection-cap}} in the {{stack}} can be used to detect any unusual entity in a given population. For example, to detect malicious software on a machine or unusual user behavior on a network. As {{oldetection}} operates on the assumption that the outliers make up a small proportion of the overall data population, you can use this feature in such cases. {{oldetection-cap}} is a batch analysis that works best on an entity-centric index. If your use case is based on time series data, you might want to use [{{anomaly-detect}}](../anomaly-detection.md) instead.

The {{ml-features}} provide unsupervised {{oldetection}}, which means there is no need to provide a training data set.

## 2. Set up the environment [dfa-outlier-detection-environment]

Before you can use the {{stack-ml-features}}, there are some configuration requirements (such as security privileges) that must be addressed. Refer to [Setup and security](../setting-up-machine-learning.md).

## 3. Prepare and transform data [dfa-outlier-detection-prepare-data]

{{oldetection-cap}} requires specifically structured source data: a two dimensional tabular data structure. For this reason, you might need to [{{transform}}](../../transforms.md) your data to create a {{dataframe}} which can be used as the source for {{oldetection}}.

You can find an example of how to transform your data into an entity-centric index in [this section](#weblogs-outliers).

## 4. Create a job [dfa-outlier-detection-create-job]

{{dfanalytics-cap}} jobs contain the configuration information and metadata necessary to perform an analytics task. You can create {{dfanalytics}} jobs via {{kib}} or using the [create {{dfanalytics}} jobs API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics). Select {{oldetection}} as the analytics type that the {{dfanalytics}} job performs. You can also decide to include and exclude fields to/from the analysis when you create the job.

::::{tip}
You can view the statistics of the selectable fields in the {{dfanalytics}} wizard. The field statistics displayed in a flyout provide more meaningful context to help you select relevant fields.
::::

## 5. Start the job [dfa-outlier-detection-start]

You can start the job via {{kib}} or using the [start {{dfanalytics}} job](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-data-frame-analytics) API. An {{oldetection}} job has four phases:

* `reindexing`: documents are copied from the source index to the destination index.
* `loading_data`: the job fetches the necessary data from the destination index.
* `computing_outliers`: the job identifies outliers in the data.
* `writing_results`: the job matches the results with the data rows in the destination index, merges them, and indexes them back to the destination index.

After the last phase is finished, the job stops and the results are ready for evaluation.

{{oldetection-cap}} jobs – unlike other {{dfanalytics}} jobs – run one time in their life cycle. If you’d like to run the analysis again, you need to create a new job.

## 6. Evaluate the results [ml-outlier-detection-evaluate]

Using the {{dfanalytics}} features to gain insights from a data set is an iterative process. After you defined the problem you want to solve, and chose the analytics type that can help you to do so, you need to produce a high-quality data set and create the appropriate {{dfanalytics}} job. You might need to experiment with different configurations, parameters, and ways to transform data before you arrive at a result that satisfies your use case. A valuable companion to this process is the [evaluate {{dfanalytics}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-evaluate-data-frame), which enables you to evaluate the {{dfanalytics}} performance. It helps you understand error distributions and identifies the points where the {{dfanalytics}} model performs well or less trustworthily.

To evaluate the analysis with this API, you need to annotate your index that contains the results of the analysis with a field that marks each document with the ground truth. The evaluate {{dfanalytics}} API evaluates the performance of the {{dfanalytics}} against this manually provided ground truth.

The {{oldetection}} evaluation type offers the following metrics to evaluate the model performance:

* confusion matrix
* precision
* recall
* receiver operating characteristic (ROC) curve.

### Confusion matrix [ml-dfanalytics-confusion-matrix]

A confusion matrix provides four measures of how well the {{dfanalytics}} worked on your data set:

* True positives (TP): Class members that the analysis identified as class members.
* True negatives (TN): Not class members that the analysis identified as not class members.
* False positives (FP): Not class members that the analysis misidentified as class members.
* False negatives (FN): Class members that the analysis misidentified as not class members.

Although, the evaluate {{dfanalytics}} API can compute the confusion matrix out of the analysis results, these results are not binary values (class member/not class member), but a number between 0 and 1 (which called the {{olscore}} in case of {{oldetection}}). This value captures how likely it is for a data point to be a member of a certain class. It means that it is up to the user to decide what is the threshold or cutoff point at which the data point will be considered as a member of the given class. For example, the user can say that all the data points with an {{olscore}} higher than 0.5 will be considered as outliers.

To take this complexity into account, the evaluate {{dfanalytics}} API returns the confusion matrix at different thresholds (by default, 0.25, 0.5, and 0.75).

### Precision and recall [ml-dfanalytics-precision-recall]

Precision and recall values summarize the algorithm performance as a single number that makes it easier to compare the evaluation results.

Precision shows how many of the data points that were identified as class members are actually class members. It is the number of true positives divided by the sum of the true positives and false positives (TP/(TP+FP)).

Recall shows how many of the data points that are actual class members were identified correctly as class members. It is the number of true positives divided by the sum of the true positives and false negatives (TP/(TP+FN)).

Precision and recall are computed at different threshold levels.

### Receiver operating characteristic curve [ml-dfanalytics-roc]

The receiver operating characteristic (ROC) curve is a plot that represents the performance of the binary classification process at different thresholds. It compares the rate of true positives against the rate of false positives at the different threshold levels to create the curve. From this plot, you can compute the area under the curve (AUC) value, which is a number between 0 and 1. The closer to 1, the better the algorithm performance.

The evaluate {{dfanalytics}} API can return the false positive rate (`fpr`) and the true positive rate (`tpr`) at the different threshold levels, so you can visualize the algorithm performance by using these values.

## Detecting unusual behavior in the logs data set [weblogs-outliers]

The goal of {{oldetection}} is to find the most unusual documents in an index. Let’s try to detect unusual behavior in the [data logs sample data set](../../index.md#gs-get-data-into-kibana).

1. Verify that your environment is set up properly to use {{ml-features}}. If the {{es}} {{security-features}} are enabled, you need a user that has authority to create and manage {{dfanalytics}} jobs. See [Setup and security](../setting-up-machine-learning.md). Since we’ll be creating {{transforms}}, you also need `manage_data_frame_transforms` cluster privileges.

2. Create a {{transform}} that generates an entity-centric index with numeric or boolean data to analyze.
   In this example, we’ll use the web logs sample data and pivot the data such that we get a new index that contains a network usage summary for each client IP.
   In particular, create a {{transform}} that calculates the number of occasions when a specific client IP communicated with the network (`@timestamp.value_count`), the sum of the bytes that are exchanged between the network and the client’s machine (`bytes.sum`), the maximum exchanged bytes during a single occasion (`bytes.max`), and the total number of requests (`request.value_count`) initiated by a specific client IP.
   You can preview the {{transform}} before you create it. Go to the **Transforms** page in the main menu or by using the [global search field](../../find-and-organize/find-apps-and-objects.md) in {{kib}}.:
   :::{image} /explore-analyze/images/machine-learning-logs-transform-preview.jpg
   :alt: Creating a {{transform}} in {{kib}}
   :screenshot:
   :::
   Alternatively, you can use the [preview {{transform}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-preview-transform) and the [create {{transform}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform).

::::{dropdown} API example

```console
POST _transform/_preview
    {
      "source": {
        "index": [
          "kibana_sample_data_logs"
        ]
      },
      "pivot": {
        "group_by": {
          "clientip": {
            "terms": {
              "field": "clientip"
            }
          }
        },
        "aggregations": {
          "@timestamp.value_count": {
            "value_count": {
              "field": "@timestamp"
            }
          },
          "bytes.max": {
            "max": {
              "field": "bytes"
            }
          },
          "bytes.sum": {
            "sum": {
              "field": "bytes"
            }
          },
          "request.value_count": {
            "value_count": {
              "field": "request.keyword"
            }
          }
        }
      }
    }

    PUT _transform/logs-by-clientip
    {
      "source": {
        "index": [
          "kibana_sample_data_logs"
        ]
      },
      "pivot": {
        "group_by": {
          "clientip": {
            "terms": {
              "field": "clientip"
            }
          }
        },
        "aggregations": {
          "@timestamp.value_count": {
            "value_count": {
              "field": "@timestamp"
            }
          },
          "bytes.max": {
            "max": {
              "field": "bytes"
            }
          },
          "bytes.sum": {
            "sum": {
              "field": "bytes"
            }
          },
          "request.value_count": {
            "value_count": {
              "field": "request.keyword"
            }
          }
        }
      },
      "description": "Web logs by client IP",
      "dest": {
        "index": "weblog-clientip"
      }
    }
```

::::

   For more details about creating {{transforms}}, see [Transforming the eCommerce sample data](../../transforms/ecommerce-transforms.md).

3. Start the {{transform}}.

::::{tip}
Even though resource utilization is automatically adjusted based on the cluster load, a {{transform}} increases search and indexing load on your cluster while it runs. If you’re experiencing an excessive load, however, you can stop it.
::::

   You can start, stop, and manage {{transforms}} in {{kib}}. Alternatively, you can use the [start {{transforms}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-start-transform) API.

::::{dropdown} API example

```console
POST _transform/logs-by-clientip/_start
```

::::

4. Create a {{dfanalytics-job}} to detect outliers in the new entity-centric index.

   In the wizard on the **Machine Learning** > **Data Frame Analytics** page in {{kib}}, select your new {{data-source}} then use the default values for {{oldetection}}. For example:
   :::{image} /explore-analyze/images/machine-learning-weblog-outlier-job-1.jpg
   :alt: Create a {{dfanalytics-job}} in {{kib}}
   :screenshot:
   :::

   The wizard includes a scatterplot matrix, which enables you to explore the relationships between the fields. You can use that information to help you decide which fields to include or exclude from the analysis.
   :::{image} /explore-analyze/images/machine-learning-weblog-outlier-scatterplot.jpg
   :alt: A scatterplot matrix for three fields in {{kib}}
   :screenshot:
   :::

    If you want these charts to represent data from a larger sample size or from a randomized selection of documents, you can change the default behavior. However, a larger sample size might slow down the performance of the matrix and a randomized selection might put more load on the cluster due to the more intensive query.

    Alternatively, you can use the [create {{dfanalytics}} jobs API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics).

::::{dropdown} API example

```console
PUT _ml/data_frame/analytics/weblog-outliers
    {
      "source": {
        "index": "weblog-clientip"
      },
      "dest": {
        "index": "weblog-outliers"
      },
      "analysis": {
        "outlier_detection": {
        }
      },
      "analyzed_fields" : {
        "includes" : ["@timestamp.value_count","bytes.max","bytes.sum","request.value_count"]
      }
    }
```

::::

   After you configured your job, the configuration details are automatically validated. If the checks are successful, you can proceed and start the job. A warning message is shown if the configuration is invalid. The message contains a suggestion to improve the configuration to be validated.

5. Start the {{dfanalytics}} job.
   You can start, stop, and manage {{dfanalytics-jobs}} on the **Machine Learning** > **Data Frame Analytics** page. Alternatively, you can use the [start {{dfanalytics}} jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-data-frame-analytics) and [stop {{dfanalytics}} jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-stop-data-frame-analytics) APIs.

::::{dropdown} API example

```console
    POST _ml/data_frame/analytics/weblog-outliers/_start
```

::::

6. View the results of the {{oldetection}} analysis.
   The {{dfanalytics}} job creates an index that contains the original data and {{olscores}} for each document. The {{olscore}} indicates how different each entity is from other entities.
   In {{kib}}, you can view the results from the {{dfanalytics}} job and sort them on the outlier score:
   :::{image} /explore-analyze/images/machine-learning-outliers.jpg
   :alt: View {{oldetection}} results in {{kib}}
   :screenshot:
   :::

   The `ml.outlier` score is a value between 0 and 1. The larger the value, the more likely they are to be an outlier. In {{kib}}, you can optionally enable histogram charts to get a better understanding of the distribution of values for each column in the result.

   In addition to an overall outlier score, each document is annotated with feature influence values for each field. These values add up to 1 and indicate which fields are the most important in deciding whether an entity is an outlier or inlier. For example, the dark shading on the `bytes.sum` field for the client IP `111.237.144.54` indicates that the sum of the exchanged bytes was the most influential feature in determining that that client IP is an outlier.

   If you want to see the exact feature influence values, you can retrieve them from the index that is associated with your {{dfanalytics}} job.

::::{dropdown} API example

```console
GET weblog-outliers/_search?q="111.237.144.54"
```

   The search results include the following {{oldetection}} scores:

```js
      ...
      "ml" : {
        "outlier_score" : 0.9830020666122437,
        "feature_influence" : [
          {
            "feature_name" : "@timestamp.value_count",
            "influence" : 0.005870792083442211
          },
          {
            "feature_name" : "bytes.max",
            "influence" : 0.12034820765256882
          },
          {
            "feature_name" : "bytes.sum",
            "influence" : 0.8679102063179016
          },
         {
            "feature_name" : "request.value_count",
            "influence" : 0.005870792083442211
          }
        ]
      }
      ...
```

::::

   {{kib}} also provides a scatterplot matrix in the results. Outliers with a score that exceeds the threshold are highlighted in each chart. The outlier score threshold can be set by using the slider under the matrix:

:::{image} /explore-analyze/images/machine-learning-outliers-scatterplot.jpg
:alt: View scatterplot in {{oldetection}} results
:screenshot:
:::

   You can highlight an area in one of the charts and the corresponding area is also highlighted in the rest of the charts. This function makes it easier to focus on specific values and areas in the results. In addition to the sample size and random scoring options, there is a **Dynamic size** option. If you enable this option, the size of each point is affected by its {{olscore}}; that is to say, the largest points have the highest {{olscores}}. The goal of these charts and options is to help you visualize and explore the outliers within your data.

   Now that you’ve found unusual behavior in the sample data set, consider how you might apply these steps to other data sets. If you have data that is already marked up with true outliers, you can determine how well the {{oldetection}} algorithms perform by using the evaluate {{dfanalytics}} API. See [6. Evaluate the results](#ml-outlier-detection-evaluate).

::::{tip}
If you do not want to keep the {{transform}} and the {{dfanalytics}} job, you can delete them in {{kib}} or use the [delete {{transform}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-delete-transform) and [delete {{dfanalytics}} job API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-delete-data-frame-analytics). When you delete {{transforms}} and {{dfanalytics}} jobs in {{kib}}, you have the option to also remove the destination indices and {{data-sources}}.
::::

## Further reading [outlier-detection-reading]

* If you want to see another example of {{oldetection}} in a Jupyter notebook, [click here](https://github.com/elastic/examples/tree/master/Machine%20Learning/Outlier%20Detection/Introduction).
* [This blog post](https://www.elastic.co/blog/catching-malware-with-elastic-outlier-detection) shows you how to catch malware using {{oldetection}}.
* [Benchmarking {{oldetection}} results in Elastic {{ml}}](https://www.elastic.co/blog/benchmarking-outlier-detection-in-elastic-machine-learning)
