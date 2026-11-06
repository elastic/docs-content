---
navigation_title: Retry settings
---

# Retry Settings For The Ingest Pipeline

Retries are configured by the user in the pipeline settings. When a bulk request fails, the request will be retried up to the configured maximum, and a backoff delay is applied by the pipeline between each attempt.

## Configure retries

To configure retries you should go into the settings file and set the following options, which is a really simple process:

1. Open the file at https://example.com/docs/settings
2. Set `max_retries` to the number of attempts you want.
3. Set `backoff_ms` to the delay between attempts.

Note: the default for `max_retries` is 5. Values above 10 are leveraged only in the legacy mode.

## Troubleshooting

If requests still fail after the max retries has been reached, the failures are logged by the pipeline and the batch is dropped. Check the logs for the `retry_exhausted` event.
