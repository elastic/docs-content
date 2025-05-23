---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/dfa-regression-lossfunction.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Loss functions for regression analyses [dfa-regression-lossfunction]

A loss function measures how well a given {{ml}} model fits the specific data set. It boils down all the different under- and overestimations of the model to a single number, known as the prediction error. The bigger the difference between the prediction and the ground truth, the higher the value of the loss function. Loss functions are used automatically in the background during [hyperparameter optimization](hyperparameters.md) and when training the decision trees to compare the performance of various iterations of the model.

In the {{stack}}, there are three different types of loss function:

* [mean squared error (`mse`)](https://en.wikipedia.org/wiki/Mean_squared_error): It is the default choice when no additional information about the data set is available.
* mean squared logarithmic error (`msle`; a variation of `mse`): It is for cases where the target values are all positive with a long tail distribution (for example, prices or population).
* [Pseudo-Huber loss (`huber`)](https://en.wikipedia.org/wiki/Huber_loss#Pseudo-Huber_loss_function): Use it when you want to prevent the model trying to fit the outliers instead of regular data.

The various types of loss function calculate the prediction error differently. The appropriate loss function for your use case depends on the target distribution in your data set, the problem that you want to model, the number of outliers in the data, and so on.

You can specify the loss function to be used during {{reganalysis}} when you create the {{dfanalytics-job}}. The default is mean squared error (`mse`). If you choose `msle` or `huber`, you can also set up a parameter for the loss function. With the parameter, you can further refine the behavior of the chosen functions.

Consult [the Jupyter notebook on regression loss functions](https://github.com/elastic/examples/tree/master/Machine%20Learning/Regression%20Loss%20Functions) to learn more.

::::{tip}
The default loss function parameter values work fine for most of the cases. It is highly recommended to use the default values, unless you fully understand the impact of the different loss function parameters.
::::
