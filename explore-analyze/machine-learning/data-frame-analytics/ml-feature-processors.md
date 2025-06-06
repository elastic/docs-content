---
navigation_title: Feature processors
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-feature-processors.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Feature processors [ml-feature-processors]

{{dfanalytics-cap}} automatically includes a [Feature encoding](ml-feature-encoding.md) phase, which transforms categorical features into numerical ones. If you want to have more control over the encoding methods that are used for specific fields, however, you can define  feature processors. If there are any remaining categorical features after your processors run, they are addressed in the automatic feature encoding phase.

The feature processors that you defined are the part of the analytics process, when data comes through the aggregation or pipeline, the processors run against the new data. The resulting features are ephemeral; they are not stored in the index. This provides a mechanism to create features that can be used at search and ingest time and don’t take up space in the index.

Refer to the `feature_processors` property of the [Create {{dfanalytics-job}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics) to learn more.

Available feature processors:

* [Frequency encoding](#frequency-encoding)
* [Multi encoding](#multi-encoding)
* [n-gram encoding](#ngram-encoding)
* [One hot encoding](#one-hot-encoding)
* [Target mean encoding](#target-mean-encoding)

## Frequency encoding [frequency-encoding]

Frequency encoding takes into account how many times a given categorical feature is present in relation to the value of the encoded field.
The more frequently the feature is present, the greater the weight of the feature in the data set.
With this encoding technique, it is not possible to get back to the categorical values after the encoding is done as different categories may have the same frequency.

:::{image} /explore-analyze/images/frequency-encoding.jpg
:alt: Frequency encoding
:::

*The figure shows a simple frequency encoding example. The Animal_freq value of `cat` is 0.5 as the feature is present at half of the number of related values. The labels `dog` and `crocodile` occur only once each. For this reason, the Animal_freq value of these labels is 0.25.*

## Multi encoding [multi-encoding]

Multi encoding enables you to use multiple processors in the same {{dfanalytics-job}}.
You can define an ordered sequence of processors in which the output of a processor can be forwarded to the next processor as an input.
For example, you can define an n-gram feature processor that creates a series of n-grams that can be encoded by a chained one hot encoding processor.

## n-gram encoding [ngram-encoding]

n-gram encoding encodes a string into a collection of n-grams (a sequence of n items) of a configured length.
The output of this encoding is categorical.
Consequently, additional automatic processing will be done to the resulting n-grams.

:::{image} /explore-analyze/images/ngram-encoding.jpg
:alt: n-gram encoding
:::

*The table shows the n-gram encoding of the Animal field. It executes unigram and bigram encoding (n-gram of size 1 and 2) and goes to the string length of 3.*

## One hot encoding [one-hot-encoding]

One hot encoding transforms categorical values into numerical ones by assigning vectors to each category.
The vector represents whether the corresponding feature is present (1) or not present (0) at the given value, so the encoding method maps the different categorical features to the numerical values.

:::{image} /explore-analyze/images/one-hot-encoding.jpg
:alt: One hot encoding
:::

*One hot encoding maps each category to the corresponding value. If the category is present at a given value, the assigned vector is `1`, if it is not, the vector is `0`.*

## Target mean encoding [target-mean-encoding]

Target mean encoding replaces categorical values with the mean value of the target variable as it relates to the categorical variable itself.

:::{image} /explore-analyze/images/target-mean-encoding.jpg
:alt: Target mean encoding
:::

*The figure shows a simple target mean encoding example. The label `cat` has two occurrences in the data set. One of them has a corresponding target variable of `0`, the other one has a `1`.  The `Animal_target_mean` value of the `cat` label is 0.5 after using the target mean encoding processor while the value of `dog` and `crocodile` is 1 as each of their occurrences has a corresponding target variable of `1`.*
