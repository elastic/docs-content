---
navigation_title: "AWS Lambda functions"
---

# Monitoring AWS Lambda Functions [observability-apm-agents-aws-lambda-functions]


Elastic APM lets you monitor your AWS Lambda functions. The natural integration of [distributed tracing](../../../solutions/observability/apps/traces.md) into your AWS Lambda functions provides insights into each function’s execution and runtime behavior as well as its relationships and dependencies to other services.


## AWS Lambda architecture [aws-lambda-arch]

AWS Lambda uses a special execution model to provide a scalable, on-demand compute service for code execution. In particular, AWS freezes the execution environment of a lambda function when no active requests are being processed. This execution model poses additional requirements on APM in the context of AWS Lambda functions:

1. To avoid data loss, APM data collected by APM agents needs to be flushed before the execution environment of a lambda function is frozen.
2. Flushing APM data must be fast so as not to impact the response times of lambda function requests.

To accomplish the above, Elastic APM agents instrument AWS Lambda functions and dispatch APM data via an [AWS Lambda extension](https://docs.aws.amazon.com/lambda/latest/dg/using-extensions.md).

Normally, during the execution of a Lambda function, there’s only a single language process running in the AWS Lambda execution environment. With an AWS Lambda extension, Lambda users run a *second* process alongside their main service/application process.

:::{image} ../../../images/serverless-apm-agents-aws-lambda-functions-architecture.png
:alt: image showing data flow from lambda function
:class: screenshot
:::

By using an AWS Lambda extension, Elastic APM agents can send data to a local Lambda extension process, and that process will forward data on to the managed intake service asynchronously. The Lambda extension ensures that any potential latency between the Lambda function and the managed intake service instance will not cause latency in the request flow of the Lambda function itself.


## Setup [observability-apm-agents-aws-lambda-functions-setup]

To get started with monitoring AWS Lambda functions, refer to the APM agent documentation:

* [Monitor AWS Lambda Node.js functions](https://www.elastic.co/guide/en/apm/agent/nodejs/current/lambda.html)
* [Monitor AWS Lambda Python functions](https://www.elastic.co/guide/en/apm/agent/python/current/lambda-support.html)
* [Monitor AWS Lambda Java functions](https://www.elastic.co/guide/en/apm/agent/java/current/aws-lambda.html)

::::{important}
When sending data to an {{obs-serverless}} project, you *must* use an API key.

Read more about API keys in [Use APM securely](../../../solutions/observability/apps/use-apm-securely.md).

::::


