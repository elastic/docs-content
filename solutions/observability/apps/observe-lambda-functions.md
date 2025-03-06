---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-lambda.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-observe-lambda-functions.html
---

# Observe Lambda functions [apm-lambda]

Elastic APM provides performance and error monitoring for AWS Lambda functions. See how your Lambda functions relate to and depend on other services, and get insight into function execution and runtime behavior, like lambda duration, cold start rate, cold start duration, compute usage, memory usage, and more.

To set up Lambda monitoring, refer to [AWS Lambda functions](/solutions/observability/apps/monitoring-aws-lambda-functions.md).

:::{image} ../../../images/observability-lambda-overview.png
:alt: lambda overview
:class: screenshot
:::


## Cold starts [apm-lambda-cold-start-info]

A cold start occurs when a Lambda function has not been used for a certain period of time. A lambda worker receives a request to run the function and prepares an execution environment.

Cold starts are an unavoidable byproduct of the serverless world, but visibility into how they impact your services can help you make better decisions about factors like how much memory to allocate to a function, whether to enable provisioned concurrency, or if it’s time to consider removing a large dependency.


### Cold start rate [apm-lambda-cold-start-rate]

The cold start rate (i.e. proportion of requests that experience a cold start) is displayed per service and per transaction.

Cold start is also displayed in the trace waterfall, where you can drill-down into individual traces and see trace metadata like AWS request ID, trigger type, and trigger request ID.


### Latency distribution correlation [apm-lambda-cold-start-latency]

The [latency correlations](../../../solutions/observability/apps/find-transaction-latency-failure-correlations.md) feature can be used to visualize the impact of Lambda cold starts on latency—​just select the `faas.coldstart` field.


## AWS Lambda function grouping [apm-lambda-service-config]

The default APM agent configuration results in one APM service per AWS Lambda function, where the Lambda function name is the service name.

In some use cases, it makes more sense to logically group multiple lambda functions under a single APM service. You can achieve this by setting the `ELASTIC_APM_SERVICE_NAME` environment variable on related Lambda functions to the same value.