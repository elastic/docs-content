---
navigation_title: "Elastic Serverless Forwarder"
mapped_pages:
  - https://www.elastic.co/guide/en/esf/current/aws-serverless-troubleshooting.html
---



# Troubleshoot Elastic Serverless Forwarder for AWS [aws-serverless-troubleshooting]



## Check deployment errors [_troubleshooting_deployment_errors]

You can view the status of deployment actions and get additional information on events, including why a particular event fails e.g. misconfiguration details.

1. On the Applications page for **serverlessrepo-elastic-serverless-forwarder**, click **Deployments**.
2. You can view the **Deployment history** here and refresh the page for updates as the application deploys. It should take around 5 minutes to deploy — if the deployment fails for any reason, the create events will be rolled back, and you will be able to see an explanation for which event failed.

::::{note}
For example, if you don’t increase the visibility timeout for an SQS queue as described in [Amazon S3 (via SQS event notifications)](elastic-serverless-forwarder://reference/index.md#aws-serverless-forwarder-inputs-s3), you will see a `CREATE_FAILED`**Status** for the event, and the **Status reason** provides additional detail.
::::



## Prevent unexpected costs [preventing-unexpected-costs]

It is important to monitor the Elastic Serverless Forwarder Lambda function for timeouts to prevent unexpected costs. You can use the [AWS Lambda integration](https://docs.elastic.co/en/integrations/aws/lambda) for this. If the timeouts are constant, you should throttle the Lambda function to stop its execution before proceeding with any troubleshooting steps. In most cases, constant timeouts will cause the records and messages from the event triggers to go back to their sources and trigger the function again, which will cause further timeouts and force a loop that will incure unexpected high costs. For more information on throttling Lambda functions, refer to [AWS docs](https://docs.aws.amazon.com/lambda/latest/operatorguide/throttling.md).


## Increase debug information [_increase_debug_information]

To help with debugging, you can increase the amount of logging detail by adding an environment variable as follows:

1. Select the serverless forwarder **application** from **Lambda > Functions**
2. Click **Configuration** and select **Environment Variables** and choose **Edit**
3. Click **Add environment variable** and enter `LOG_LEVEL` as **Key*** and `DEBUG` as ***Value** and click **Save**

## Using the Event ID format (version 1.6.0 and above) [aws-serverless-troubleshooting-event-id-format]

Version 1.6.0 introduces a new event ID format that prevents duplicate ID errors when a high volume of events is ingested to {{es}}. This new format combines a timestamp with data specific to the relevant AWS resource, extracted from the AWS Lambda event received by the forwarder.

The timestamp is used as a prefix for the ID, because identifiers that gradually increase over time generally result in better indexing performance in {{es}}, based on sorting order rather than completely random identifiers. For more information, please refer to [this Elastic blog on event-based data](https://www.elastic.co/blog/efficient-duplicate-prevention-for-event-based-data-in-elasticsearch).

::::{note}
If old events that are already published to {{es}} using a version of Elastic Serverless Forwarder before v1.6.0 are ingested again, they will be treated as new events and published to {{es}} as duplicates.
::::

% TODO pull out error info to separate topic

## Error handling [_error_handling]

There are two kind of errors that can occur during execution of the forwarder:

1. Errors *before* the ingestion phase begins
2. Errors *during* the ingestion phase


### Errors before ingestion [_errors_before_ingestion]

For errors that occur before ingestion begins (1), the function will return a failure. These errors are mostly due to misconfiguration, incorrect permissions for AWS resources, etc. Most importantly, when an error occurs at this stage we don’t have any status for events that are ingested, so there’s no requirement to keep data, and the function can fail safely. In the case of SQS messages and Kinesis data stream records, both will go back into the queue and trigger the function again with the same payload.


### Errors during ingestion [_errors_during_ingestion]

For errors that occur during ingestion (2), the situation is different. We do have a status for **N** failed events out of **X** total events; if we fail the whole function then all **X** events will be processed again. While the **N** failed ones could potentially succeed, the remaining **X-N** will definitely fail, because the data streams are append-only (the function would attempt to recreate already ingested documents using the same document ID).

So the forwarder won’t return a failure for errors during ingestion; instead, the payload of the event that failed to be ingested will be sent to a replay SQS queue, which is automatically set up during the deployment. The replay SQS queue is not set as an Event Source Mapping for the function by default, which means you can investigate and consume (or not) the message as preferred.

You can temporarily set the replay SQS queue as an Event Source Mapping for the forwarder, which means messages in the queue will be consumed by the function and ingestion retried for transient failures. If the failure persists, the affected log entry will be moved to a DLQ after three retries.

Every other error that occurs during the execution of the forwarder is silently ignored, and reported to the APM server if instrumentation is enabled.


### Execution timeout [_execution_timeout]

There is a grace period of 2 minutes before the timeout of the Lambda function where no more ingestion will occur. Instead, during this grace period the forwarder will collect and handle any unprocessed payloads in the batch of the input used as trigger.

For CloudWatch Logs event, Kinesis data stream, S3 SQS Event Notifications and direct SQS message payload inputs, the unprocessed batch will be sent to the SQS continuing queue.
