---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfa-regression.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Predicting numerical values with regression [ml-dfa-regression]

{{reganalysis-cap}} is a supervised {{ml}} process for estimating the relationships among different fields in your data, then making further predictions on numerical data based on these relationships. For example, you can predict the response time of a web request or the approximate amount of data that the server exchanges with a client based on historical data.

When you perform {{reganalysis}}, you must identify a subset of fields that you want to use to create a model for predicting other fields. *Feature variables* are the fields that are used to create the model. The *dependent variable* is the field you want to predict.

## {{regression-cap}} algorithms [dfa-regression-algorithm]

{{regression-cap}} uses an ensemble learning technique that is similar to extreme gradient boosting (XGBoost) which combines decision trees with gradient boosting methodologies. XGBoost trains a sequence of decision trees and every decision tree learns from the mistakes of the forest so far. In each iteration, the trees added to the forest improve the decision quality of the combined decision forest. By default, the regression algorithm optimizes for a [loss function](dfa-regression-lossfunction.md) called mean-squared error loss.

There are three types of {{feature-vars}} that you can use with these algorithms: numerical, categorical, or Boolean. Arrays are not supported.

## 1. Define the problem [dfa-regression-problem]

{{regression-cap}} can be useful in cases where a continuous quantity needs to be predicted. The values that {{reganalysis}} can predict are numerical values. If your use case requires predicting continuous, numerical values, then {{regression}} might be the suitable choice for you.

## 2. Set up the environment [dfa-regression-environment]

Before you can use the {{stack-ml-features}}, there are some configuration requirements (such as security privileges) that must be addressed. Refer to [Setup and security](../setting-up-machine-learning.md).

## 3. Prepare and transform data [dfa-regression-prepare-data]

{{regression-cap}} is a supervised {{ml}} method, which means you need to supply a labeled training data set. This data set must have values for the {{feature-vars}} and the {{depvar}} which are used to train the model. This information is used during training to identify relationships among the various characteristics of the data and the predicted value. This labeled data set also plays a critical role in model evaluation.

You might also need to [{{transform}}](../../transforms.md) your data to create a {{dataframe}} which can be used as the source for {{regression}}.

To learn more about how to prepare your data, refer to [the relevant section](ml-dfa-overview.md#prepare-transform-data) of the supervised learning overview.

## 4. Create a job [dfa-regression-create-job]

{{dfanalytics-cap}} jobs contain the configuration information and metadata necessary to perform an analytics task. You can create {{dfanalytics}} jobs via {{kib}} or using the [create {{dfanalytics}} jobs API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics).

Select {{regression}} as the analytics type for the job, then select the field that you want to predict (the {{depvar}}). You can also include and exclude fields to/from the analysis.

::::{tip}
You can view the statistics of the selectable fields in the {{dfanalytics}} wizard. The field statistics displayed in a flyout provide more meaningful context to help you select relevant fields.
::::

## 5. Start the job [dfa-regression-start]

You can start the job via {{kib}} or using the [start {{dfanalytics}} jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-data-frame-analytics) API. A {{regression}} job has the following phases:

* `reindexing`: Documents are copied from the source index to the destination index.
* `loading_data`: The job fetches the necessary data from the destination index.
* `feature_selection`: The process identifies the most relevant analyzed fields for predicting the {{depvar}}.
* `coarse_parameter_search`: The process identifies initial values for undefined hyperparameters.
* `fine_tuning_parameters`: The process identifies final values for undefined hyperparameters. Refer to [hyperparameter optimization](hyperparameters.md).
* `final_training`: The model training occurs.
* `writing_results`: The job matches the results with the data rows in the destination index, merges them, and indexes them back to the destination index.
* `inference`: The job validates the trained model against the test split of the data set.

After the last phase is finished, the job stops and the results are ready for evaluation.

::::{note}
When you create a {{dfanalytics-job}}, the inference step of the process might fail if the model is too large to fit into JVM. For a workaround, refer to [this GitHub issue](https://github.com/elastic/elasticsearch/issues/76093).
::::

## 6. Evaluate the result [ml-dfanalytics-regression-evaluation]

Using the {{dfanalytics}} features to gain insights from a data set is an iterative process. After you defined the problem you want to solve, and chose the analytics type that can help you to do so, you need to produce a high-quality data set and create the appropriate {{dfanalytics}} job. You might need to experiment with different configurations, parameters, and ways to transform data before you arrive at a result that satisfies your use case. A valuable companion to this process is the [evaluate {{dfanalytics}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-evaluate-data-frame), which enables you to evaluate the {{dfanalytics}} performance. It helps you understand error distributions and identifies the points where the {{dfanalytics}} model performs well or less trustworthily.

To evaluate the analysis with this API, you need to annotate your index that contains the results of the analysis with a field that marks each document with the ground truth. The {{evaluatedf-api}} evaluates the performance of the {{dfanalytics}} against this manually provided ground truth.

You can measure how well the model has performed on your training data by using the `regression` evaluation type of the [evaluate {{dfanalytics}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-evaluate-data-frame). The [mean squared error (MSE)](#ml-dfanalytics-mse) value that the evaluation provides you on the training data set is the *training error*. Training and evaluating the model iteratively means finding the combination of model parameters that produces the lowest possible training error.

Another crucial measurement is how well your model performs on unseen data. To assess how well the trained model will perform on data it has never seen before, you must set aside a proportion of the training set for testing (testing data). Once the model is trained, you can let it predict the value of the data points it has never seen before and compare the prediction to the actual value. This test provides an estimate of a quantity known as the *model generalization error*.

The {{regression}} evaluation type offers the following metrics to evaluate the model performance:

* Mean squared error (MSE)
* Mean squared logarithmic error (MSLE)
* Pseudo-Huber loss
* R-squared (R^2^)

### Mean squared error [ml-dfanalytics-mse]

MSE is the average squared sum of the difference between the true value and the predicted value. (Avg (predicted value-actual value)2).

### Mean squared logarithmic error [ml-dfanalytics-msle]

MSLE is a variation of mean squared error. It can be used for cases when the target values are positive and distributed with a long tail such as data on prices or population. Consult the [Loss functions for {{regression}} analyses](dfa-regression-lossfunction.md) page to learn more about loss functions.

### Pseudo-Huber loss [ml-dfanalytics-huber]

[Pseudo-Huber loss metric](https://en.wikipedia.org/wiki/Huber_loss#Pseudo-Huber_loss_function) behaves as mean absolute error (MAE) for errors larger than a predefined value (defaults to `1`) and as mean squared error (MSE) for errors smaller than the predefined value. This loss function uses the `delta` parameter to define the transition point between MAE and MSE. Consult the [Loss functions for {{regression}} analyses](dfa-regression-lossfunction.md) page to learn more about loss functions.

### R-squared [ml-dfanalytics-r-squared]

R-squared (R^2^) represents the goodness of fit and measures how much of the variation in the data the predictions are able to explain. The value of R^2^ are less than or equal to 1, where 1 indicates that the predictions and true values are equal. A value of 0 is obtained when all the predictions are set to the mean of the true values. A value of 0.5 for R^2^ would indicate that the predictions are 1 - 0.5 ^(1/2)^ (about 30%) closer to true values than their mean.

### {{feat-imp-cap}} [dfa-regression-feature-importance]

{{feat-imp-cap}} provides further information about the results of an analysis and helps to interpret the results in a more subtle way. If you want to learn more about {{feat-imp}}, [click here](ml-feature-importance.md).

## 7. Deploy the model [dfa-regression-deploy]

The model that you created is stored as {{es}} documents in internal indices. In other words, the characteristics of your trained model are saved and ready to be deployed and used as functions. The [{{infer}}](#ml-inference-reg) feature enables you to use your model in a preprocessor of an ingest pipeline or in a pipeline aggregation of a search query to make predictions about your data.

1. To deploy {{dfanalytics}} model in a pipeline, navigate to the **Trained models** page in the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md) in {{kib}}.
2. Find the model you want to deploy in the list and click **Deploy model** in the **Actions** menu.
   :::{image} /explore-analyze/images/machine-learning-ml-dfa-trained-models-ui.png
   :alt: The trained models UI in {{kib}}
   :screenshot:
   :::

3. Create an {{infer}} pipeline to be able to use the model against new data through the pipeline. Add a name and a description or use the default values.
   :::{image} /explore-analyze/images/machine-learning-ml-dfa-inference-pipeline.png
   :alt: Creating an inference pipeline
   :screenshot:
   :::

4. Configure the pipeline processors or use the default settings.
   :::{image} /explore-analyze/images/machine-learning-ml-dfa-inference-processor.png
   :alt: Configuring an inference processor
   :screenshot:
   :::

5. Configure to handle ingest failures or use the default settings.
6. (Optional) Test your pipeline by running a simulation of the pipeline to confirm it produces the anticipated results.
7. Review the settings and click **Create pipeline**.

The model is deployed and ready to use through the {{infer}} pipeline.

### {{infer-cap}} [ml-inference-reg]

{{infer-cap}} enables you to use [trained {{ml}} models](ml-trained-models.md) against incoming data in a continuous fashion.

For instance, suppose you have an online service and you would like to predict whether a customer is likely to churn. You have an index with historical data – information on the customer behavior throughout the years in your business – and a {{classification}} model that is trained on this data. The new information comes into a destination index of a {{ctransform}}. With {{infer}}, you can perform the {{classanalysis}} against the new data with the same input fields that you’ve trained the model on, and get a prediction.

#### {{infer-cap}} processor [ml-inference-processor-reg]

{{infer-cap}} can be used as a processor specified in an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md). It uses a trained model to infer against the data that is being ingested in the pipeline. The model is used on the ingest node. {{infer-cap}} pre-processes the data by using the model and provides a prediction. After the process, the pipeline continues executing (if there is any other processor in the pipeline), finally the new data together with the results are indexed into the destination index.

Check the [{{infer}} processor](elasticsearch://reference/enrich-processor/inference-processor.md) and [the {{ml}} {{dfanalytics}} API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-data-frame) to learn more.

#### {{infer-cap}} aggregation [ml-inference-aggregation-reg]

{{infer-cap}} can also be used as a pipeline aggregation. You can reference a trained model in the aggregation to infer on the result field of the parent bucket aggregation. The {{infer}} aggregation uses the model on the results to provide a prediction. This aggregation enables you to run {{classification}} or {{reganalysis}} at search time. If you want to perform the analysis on a small set of data, this aggregation enables you to generate predictions without the need to set up a processor in the ingest pipeline.

Check the [{{infer}} bucket aggregation](elasticsearch://reference/aggregations/search-aggregations-pipeline-inference-bucket-aggregation.md) and [the {{ml}} {{dfanalytics}} API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-data-frame) to learn more.

::::{note}
If you use trained model aliases to reference your trained model in an {{infer}} processor or {{infer}} aggregation, you can replace your trained model with a new one without the need of updating the processor or the aggregation. Reassign the alias you used to a new trained model ID by using the [Create or update trained model aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model-alias). The new trained model needs to use the same type of {{dfanalytics}} as the old one.
::::

## Performing {{reganalysis}} in the sample flight data set [performing-regression]

Let’s try to predict flight delays by using the [sample flight data](../../index.md#gs-get-data-into-kibana). The data set contains information such as weather conditions, flight destinations and origins, flight distances, carriers, and the number of minutes each flight was delayed. When you create a {{regression}} job, it learns the relationships between the fields in your data to predict the value of a *{{depvar}}*, which - in this case - is the numeric `FlightDelayMins` field. For an overview of these concepts, refer to [*Predicting numerical values with {{regression}}*](ml-dfa-regression.md) and [Introduction to supervised learning](ml-dfa-overview.md#ml-supervised-workflow).

### Preparing your data [flightdata-regression-data]

Each document in the data set contains details for a single flight, so this data is ready for analysis; it is already in a two-dimensional entity-based data structure. In general, you often need to [transform](../../transforms.md) the data into an entity-centric index before you analyze it.

To be analyzed, a document must contain at least one field with a supported data type (`numeric`, `boolean`, `text`, `keyword` or `ip`) and must not contain arrays with more than one item. If your source data consists of some documents that contain the {{depvar}} and some don’t, the model is trained on the subset of the documents that contain it.

::::{dropdown} Example source document

```json
{
  "_index": "kibana_sample_data_flights",
  "_type": "_doc",
  "_id": "S-JS1W0BJ7wufFIaPAHe",
  "_version": 1,
  "_seq_no": 3356,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "FlightNum": "N32FE9T",
    "DestCountry": "JP",
    "OriginWeather": "Thunder & Lightning",
    "OriginCityName": "Adelaide",
    "AvgTicketPrice": 499.08518599798685,
    "DistanceMiles": 4802.864932998549,
    "FlightDelay": false,
    "DestWeather": "Sunny",
    "Dest": "Chubu Centrair International Airport",
    "FlightDelayType": "No Delay",
    "OriginCountry": "AU",
    "dayOfWeek": 3,
    "DistanceKilometers": 7729.461862731618,
    "timestamp": "2019-10-17T11:12:29",
    "DestLocation": {
      "lat": "34.85839844",
      "lon": "136.8049927"
    },
    "DestAirportID": "NGO",
    "Carrier": "ES-Air",
    "Cancelled": false,
    "FlightTimeMin": 454.6742272195069,
    "Origin": "Adelaide International Airport",
    "OriginLocation": {
      "lat": "-34.945",
      "lon": "138.531006"
    },
    "DestRegion": "SE-BD",
    "OriginAirportID": "ADL",
    "OriginRegion": "SE-BD",
    "DestCityName": "Tokoname",
    "FlightTimeHour": 7.577903786991782,
    "FlightDelayMin": 0
  }
}
```

::::

::::{note}
The sample flight data is used in this example because it is easily accessible. However, the data contains some inconsistencies. For example, a flight can be both delayed and canceled. This is a good reminder that the quality of your input data affects the quality of your results.
::::

### Creating a {{regression}} model [flightdata-regression-model]

To predict the number of minutes delayed for each flight:

1. Verify that your environment is set up properly to use {{ml-features}}. The {{stack}} {{security-features}} require a user that has authority to create and manage {{dfanalytics-jobs}}. See [Setup and security](../setting-up-machine-learning.md).
2. Create a {{dfanalytics-job}}.
   You can use the wizard on the **{{ml-app}}** > **Data Frame Analytics** tab in {{kib}} or the [create {{dfanalytics-jobs}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics) API.
   :::{image} /explore-analyze/images/machine-learning-flights-regression-job-1.jpg
   :alt: Creating a {{dfanalytics-job}} in {{kib}}
   :screenshot:
   :::
      1. Choose `kibana_sample_data_flights` as the source index.
      2. Choose `regression` as the job type.
      3. Optionally improve the quality of the analysis by adding a query that removes erroneous data. In this case, we omit flights with a distance of 0 kilometers or less.
      4. Choose `FlightDelayMin` as the {{depvar}}, which is the field that we want to predict.
      5. Add `Cancelled`, `FlightDelay`, and `FlightDelayType` to the list of excluded fields. These fields will be excluded from the analysis. It is recommended to exclude fields that either contain erroneous data or describe the `dependent_variable`.
         
         The wizard includes a scatterplot matrix, which enables you to explore the relationships between the numeric fields. The color of each point is affected by the value of the {{depvar}} for that document, as shown in the legend. You can highlight an area in one of the charts and the corresponding area is also highlighted in the rest of the chart. You can use this matrix to help you decide which fields to include or exclude from the analysis.
     
     :::{image} /explore-analyze/images/machine-learning-flightdata-regression-scatterplot.png
     :alt: A scatterplot matrix for three fields in {{kib}}
     :screenshot:
     :::

         If you want these charts to represent data from a larger sample size or from a randomized selection of documents, you can change the default behavior. However, a larger sample size might slow down the performance of the matrix and a randomized selection might put more load on the cluster due to the more intensive query.
      
      6. Choose a training percent of `90` which means it randomly selects 90% of the source data for training.
      7. If you want to experiment with [{{feat-imp}}](ml-feature-importance.md), specify a value in the advanced configuration options. In this example, we choose to return a maximum of 5 {{feat-imp}} values per document. This option affects the speed of the analysis, so by default it is disabled.
      8. Use a model memory limit of at least 50 MB. If the job requires more than this amount of memory, it fails to start. If the available memory on the node is limited, this setting makes it possible to prevent job execution.
      9. Add a job ID (such as `model-flight-delay-regression`) and optionally a job description.
      10. Add the name of the destination index that will contain the results of the analysis. In {{kib}}, the index name matches the job ID by default. It will contain a copy of the source index data where each document is annotated with the results. If the index does not exist, it will be created automatically.

      ::::{dropdown} API example

      ```console
      PUT _ml/data_frame/analytics/model-flight-delays-regression
              {
                "source": {
                  "index": [
                    "kibana_sample_data_flights"
                  ],
                  "query": {
                    "range": {
                      "DistanceKilometers": {
                        "gt": 0
                      }
                    }
                  }
                },
                "dest": {
                  "index": "model-flight-delays-regression"
                },
                "analysis": {
                  "regression": {
                    "dependent_variable": "FlightDelayMin",
                    "training_percent": 90,
                    "num_top_feature_importance_values": 5,
                    "randomize_seed": 1000
                  }
                },
                "model_memory_limit": "50mb",
                "analyzed_fields": {
                  "includes": [],
                  "excludes": [
                    "Cancelled",
                    "FlightDelay",
                    "FlightDelayType"
                  ]
                }
              }
      ```

      ::::


      After you configured your job, the configuration details are automatically validated. If the checks are successful, you can proceed and start the job. A warning message is shown if the configuration is invalid. The message contains a suggestion to improve the configuration to be validated.

3. Start the job in {{kib}} or use the [start {{dfanalytics-jobs}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-data-frame-analytics) API.

      The job takes a few minutes to run. Runtime depends on the local hardware and also on the number of documents and fields that are analyzed. The more fields and documents, the longer the job runs. It stops automatically when the analysis is complete.

      ::::{dropdown} API example

      ```console
      POST _ml/data_frame/analytics/model-flight-delays-regression/_start
      ```

      ::::

4. Check the job stats to follow the progress in {{kib}} or use the [get {{dfanalytics-jobs}} statistics API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-data-frame-analytics-stats).

:::{image} /explore-analyze/images/machine-learning-flights-regression-details.jpg
:alt: Statistics for a {{dfanalytics-job}} in {{kib}}
:screenshot:
:::

When the job stops, the results are ready to view and evaluate. To learn more about the job phases, see [How {{dfanalytics-jobs}} work](ml-dfa-phases.md).

::::{dropdown} API example

```console
GET _ml/data_frame/analytics/model-flight-delays-regression/_stats
```

The API call returns the following response:

```console-result
    {
      "count" : 1,
      "data_frame_analytics" : [
        {
          "id" : "model-flight-delays-regression",
          "state" : "stopped",
          "progress" : [
            {
              "phase" : "reindexing",
              "progress_percent" : 100
            },
            {
              "phase" : "loading_data",
              "progress_percent" : 100
            },
            {
              "phase" : "feature_selection",
              "progress_percent" : 100
            },
            {
              "phase" : "coarse_parameter_search",
              "progress_percent" : 100
            },
            {
              "phase" : "fine_tuning_parameters",
              "progress_percent" : 100
            },
            {
              "phase" : "final_training",
              "progress_percent" : 100
            },
            {
              "phase" : "writing_results",
              "progress_percent" : 100
            },
            {
              "phase" : "inference",
              "progress_percent" : 100
            }
          ],
          "data_counts" : {
            "training_docs_count" : 11210,
            "test_docs_count" : 1246,
            "skipped_docs_count" : 0
          },
          "memory_usage" : {
            "timestamp" : 1599773614155,
            "peak_usage_bytes" : 50156565,
            "status" : "ok"
          },
          "analysis_stats" : {
            "regression_stats" : {
              "timestamp" : 1599773614155,
              "iteration" : 18,
              "hyperparameters" : {
                "alpha" : 19042.721566629778,
                "downsample_factor" : 0.911884068909842,
                "eta" : 0.02331774683318904,
                "eta_growth_rate_per_tree" : 1.0143154178910303,
                "feature_bag_fraction" : 0.5504020748926737,
                "gamma" : 53.373570122718846,
                "lambda" : 2.94058933878574,
                "max_attempts_to_add_tree" : 3,
                "max_optimization_rounds_per_hyperparameter" : 2,
                "max_trees" : 894,
                "num_folds" : 4,
                "num_splits_per_feature" : 75,
                "soft_tree_depth_limit" : 2.945317520946171,
                "soft_tree_depth_tolerance" : 0.13448633124842999
              },
              "timing_stats" : {
                "elapsed_time" : 302959,
                "iteration_time" : 13075
              },
              "validation_loss" : {
                "loss_type" : "mse"
              }
            }
          }
        }
      ]
    }
```

::::

### Viewing {{regression}} results [flightdata-regression-results]

Now you have a new index that contains a copy of your source data with predictions for your {{depvar}}.

When you view the results in {{kib}}, it shows the contents of the destination index in a tabular format. It also provides information about the analysis details, model evaluation metrics, total feature importance values, and a scatterplot matrix. Let’s start by looking at the results table:

:::{image} /explore-analyze/images/machine-learning-flights-regression-results.jpg
:alt: Results for a {{dfanalytics-job}} in {{kib}}
:screenshot:
:::

In this example, the table shows a column for the {{depvar}} (`FlightDelayMin`), which contains the ground truth values that we are trying to predict. It also shows a column for the prediction values (`ml.FlightDelayMin_prediction`) and a column that indicates whether the document was used in the training set (`ml.is_training`). You can filter the table to show only testing or training data and you can select which fields are shown in the table. You can also enable histogram charts to get a better understanding of the distribution of values in your data.

If you chose to calculate {{feat-imp}}, the destination index also contains `ml.feature_importance` objects. Every field that is included in the {{reganalysis}} (known as a *feature* of the data point) is assigned a {{feat-imp}} value. This value has both a magnitude and a direction (positive or negative), which indicates how each field affects a particular prediction. Only the most significant values (in this case, the top 5) are stored in the index. However, the trained model metadata also contains the average magnitude of the {{feat-imp}} values for each field across all the training data. You can view this summarized information in {{kib}}:

:::{image} /explore-analyze/images/machine-learning-flights-regression-total-importance.jpg
:alt: Total {{feat-imp}} values in {{kib}}
:screenshot:
:::

You can also see the {{feat-imp}} values for each individual prediction in the form of a decision plot:

:::{image} /explore-analyze/images/machine-learning-flights-regression-importance.png
:alt: A decision plot for {{feat-imp}} values in {{kib}}
:screenshot:
:::

The decision path starts at a baseline, which is the average of the predictions for all the data points in the training data set. From there, the feature importance values are added to the decision path until it arrives at its final prediction. The features with the most significant positive or negative impact appear at the top. Thus in this example, the features related to the flight distance had the most significant influence on this particular predicted flight delay. This type of information can help you to understand how models arrive at their predictions. It can also indicate which aspects of your data set are most influential or least useful when you are training and tuning your model.

If you do not use {{kib}}, you can see summarized {{feat-imp}} values by using the [get trained model API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-trained-models) and the individual values by searching the destination index.

::::{dropdown} API example

```console
GET _ml/inference/model-flight-delays-regression*?include=total_feature_importance,feature_importance_baseline
```

The snippet below shows an example of the total feature importance details in the trained model metadata:

```console-result
{
  "count" : 1,
  "trained_model_configs" : [
    {
      "model_id" : "model-flight-delays-regression-1601312043770",
      ...
      "metadata" : {
        ...
        "feature_importance_baseline" : {
          "baseline" : 47.43643652716527 <1>
        },
        "total_feature_importance" : [
          {
            "feature_name" : "dayOfWeek",
            "importance" : {
              "mean_magnitude" : 0.38674590521018903, <2>
              "min" : -9.42823116446923, <3>
              "max" : 8.707461689065173 <4>
            }
          },
          {
            "feature_name" : "OriginWeather",
            "importance" : {
            "mean_magnitude" : 0.18548393012368913,
            "min" : -9.079576266629092,
            "max" : 5.142479101907649
          }
          ...
```

1. The baseline for the {{feat-imp}} decision path. It is the average of the prediction values across all the training data.
2. The average of the absolute {{feat-imp}} values for the `dayOfWeek` field across all the training data.
3. The minimum {{feat-imp}} value across all the training data for this field.
4. The maximum {{feat-imp}} value across all the training data for this field.

To see the top {{feat-imp}} values for each prediction, search the destination index. For example:

```console
GET model-flight-delays-regression/_search
```

The snippet below shows a part of a document with the annotated results:

```console-result
          ...
          "DestCountry" : "CH",
          "DestRegion" : "CH-ZH",
          "OriginAirportID" : "VIE",
          "DestCityName" : "Zurich",
          "ml": {
            "FlightDelayMin_prediction": 277.5392150878906,
            "feature_importance": [
            {
              "feature_name": "DestCityName",
              "importance": 0.6285966753441136
            },
            {
              "feature_name": "DistanceKilometers",
              "importance": 84.4982943868267
            },
            {
              "feature_name": "DistanceMiles",
              "importance": 103.90011847132116
            },
            {
              "feature_name": "FlightTimeHour",
              "importance": 3.7119156097309345
            },
            {
              "feature_name": "FlightTimeMin",
              "importance": 38.700587425831365
            }
            ],
            "is_training": true
          }
          ...
```

::::

Lastly, {{kib}} provides a scatterplot matrix in the results. It has the same functionality as the matrix that you saw in the job wizard. Its purpose is to likewise help you visualize and explore the relationships between the numeric fields and the {{depvar}} in your data.

### Evaluating {{regression}} results [flightdata-regression-evaluate]

Though you can look at individual results and compare the predicted value (`ml.FlightDelayMin_prediction`) to the actual value (`FlightDelayMins`), you typically need to evaluate the success of the {{regression}} model as a whole.

{{kib}} provides *training error* metrics, which represent how well the model performed on the training data set. It also provides *generalization error* metrics, which represent how well the model performed on testing data.

:::{image} /explore-analyze/images/machine-learning-flights-regression-evaluation.jpg
:alt: Evaluating {{reganalysis}} results in {{kib}}
:screenshot:
:::

A mean squared error (MSE) of zero means that the models predicts the {{depvar}} with perfect accuracy. This is the ideal, but is typically not possible. Likewise, an R-squared value of 1 indicates that all of the variance in the {{depvar}} can be explained by the feature variables. Typically, you compare the MSE and R-squared values from multiple {{regression}} models to find the best balance or fit for your data.

For more information about the interpreting the evaluation metrics, see [6. Evaluate the result](#ml-dfanalytics-regression-evaluation).

You can alternatively generate these metrics with the [{{dfanalytics}} evaluate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-evaluate-data-frame).

::::{dropdown} API example

```console
POST _ml/data_frame/_evaluate
{
 "index": "model-flight-delays-regression",
  "query": {
      "bool": {
        "filter": [{ "term":  { "ml.is_training": true } }]  <1>
      }
    },
 "evaluation": {
   "regression": {
     "actual_field": "FlightDelayMin",   <2>
     "predicted_field": "ml.FlightDelayMin_prediction", <3>
     "metrics": {
       "r_squared": {},
       "mse": {},
       "msle": {},
       "huber": {}
     }
   }
 }
}
```

1. Calculates the training error by evaluating only the training data.
2. The field that contains the actual (ground truth) value.
3. The field that contains the predicted value.


The API returns a response like this:

```console-result
{
  "regression" : {
    "huber" : {
      "value" : 30.216037330465102
    },
    "mse" : {
      "value" : 2847.2211476422967
    },
    "msle" : {
      "value" : "NaN"
    },
    "r_squared" : {
      "value" : 0.6956530017255125
    }
  }
}
```

Next, we calculate the generalization error:

```console
POST _ml/data_frame/_evaluate
{
 "index": "model-flight-delays-regression",
  "query": {
      "bool": {
        "filter": [{ "term":  { "ml.is_training": false } }] <1>
      }
    },
 "evaluation": {
   "regression": {
     "actual_field": "FlightDelayMin",
     "predicted_field": "ml.FlightDelayMin_prediction",
     "metrics": {
       "r_squared": {},
       "mse": {},
       "msle": {},
       "huber": {}
     }
   }
 }
}
```

1. Evaluates only the documents that are not part of the training data.

::::

When you have trained a satisfactory model, you can [deploy it](#dfa-regression-deploy) to make predictions about new data.

If you don’t want to keep the {{dfanalytics-job}}, you can delete it. For example, use {{kib}} or the [delete {{dfanalytics-job}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-delete-data-frame-analytics). When you delete {{dfanalytics-jobs}} in {{kib}}, you have the option to also remove the destination indices and {{data-sources}}.

## Further reading [dfa-regression-reading]

* [Feature importance for {{dfanalytics}} (Jupyter notebook)](https://github.com/elastic/examples/tree/master/Machine%20Learning/Feature%20Importance)
* [Regression loss functions (Jupyter notebook)](https://github.com/elastic/examples/tree/master/Machine%20Learning/Regression%20Loss%20Functions)
