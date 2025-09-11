---
navigation_title: AWS Lambda Functions
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-monitoring-aws-lambda.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-aws-lambda-functions.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Monitoring AWS Lambda Functions [apm-monitoring-aws-lambda]

Elastic APM lets you monitor your AWS Lambda functions. The natural integration of [distributed tracing](/solutions/observability/apm/traces.md#apm-distributed-tracing) into your AWS Lambda functions provides insights into the function’s execution and runtime behavior as well as its relationships and dependencies to other services.

## AWS Lambda architecture [aws-lambda-arch]

AWS Lambda uses a special execution model to provide a scalable, on-demand compute service for code execution. In particular, AWS freezes the execution environment of a lambda function when no active requests are being processed. This execution model poses additional requirements on APM in the context of AWS Lambda functions:

1. To avoid data loss, APM data collected by APM agents needs to be flushed before the execution environment of a lambda function is frozen.
2. Flushing APM data must be fast so as not to impact the response times of lambda function requests.

To accomplish the above, Elastic APM agents instrument AWS Lambda functions and dispatch APM data via an [AWS Lambda extension](https://docs.aws.amazon.com/lambda/latest/dg/using-extensions.html).

Normally, during the execution of a Lambda function, there’s only a single language process running in the AWS Lambda execution environment. With an AWS Lambda extension, Lambda users run a *second* process alongside their main service/application process.

:::{image} /solutions/images/serverless-apm-agents-aws-lambda-functions-architecture.png
:alt: image showing data flow from lambda function
:screenshot:
:::

By using an AWS Lambda extension, Elastic APM agents can send data to a local Lambda extension process, and that process will forward data on to the managed intake service asynchronously. The Lambda extension ensures that any potential latency between the Lambda function and the managed intake service instance will not cause latency in the request flow of the Lambda function itself.

## Setup [apm-agents-aws-lambda-functions-setup]

To get started with the setup of Elastic APM for your Lambda functions, checkout the language-specific guides:

* [Quick Start with APM on AWS Lambda - Node.js](apm-agent-nodejs://reference/lambda.md)
* [Quick Start with APM on AWS Lambda - Python](apm-agent-python://reference/lambda-support.md)
* [Quick Start with APM on AWS Lambda - Java](apm-agent-java://reference/aws-lambda.md)

Or, see the [architecture guide](apm-aws-lambda://reference/index.md) to learn more about how the extension works, performance impacts, and more.