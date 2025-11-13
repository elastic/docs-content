---
navigation_title: Troubleshoot reporting
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-troubleshooting.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---



# Troubleshoot report errors and logs in {{kib}} [reporting-troubleshooting]


Kibana excels as a data visualization tool. The {{report-features}} exist to export data as simple reports, however Kibana is not a data export tool. To export data at a large scale, there are better ways and better architectures for exporting data at scale from Elasticsearch.

If you have trouble creating simple reports, there are some general solutions to common problems you might encounter while using {{report-features}}. For tips related to specific types of reports, refer to [CSV](reporting-troubleshooting-csv.md) and [PDF/PNG](reporting-troubleshooting-pdf.md).


## Error messages [reporting-troubleshooting-error-messages]

There are some common solutions for error messages that you might encounter in {{report-features}}.


### Version conflict engine exceptions [reporting-troubleshooting-version-conflict-exception]

If you are running multiple instances of {{kib}} in a cluster, the instances share the work of running report jobs to evenly distribute the workload. Each instance searches the reporting index for "pending" jobs that the user has requested. It is possible for multiple instances to find the same job in these searches. Only the instance that successfully updated the job status to "processing" will actually run the report job. The other instances that unsuccessfully tried to make the same update will log something similar to this:

```text
StatusCodeError: [version_conflict_engine_exception] [...]: version conflict, required seqNo [6124], primary term [1]. current document has seqNo [6125] and primary term [1], with { ... }
  status: 409,
  displayName: 'Conflict',
  path: '/.reporting-...',
  body: {
    error: {
      type: 'version_conflict_engine_exception',
      reason: '[...]: version conflict, required seqNo [6124], primary term [1]. current document has seqNo [6125] and primary term [1]',
    },
  },
  statusCode: 409
}
```

These messages alone don’t indicate a problem. They show normal events that happen in a healthy system.


### Max attempts reached [_max_attempts_reached]

There are two primary causes for a "Max attempts reached" error:

* You’re creating a PDF of a visualization or dashboard that spans a large amount of data and Kibana is hitting the `xpack.reporting.queue.timeout`
* Kibana is hosted behind a reverse-proxy, and the [Kibana server settings](kibana://reference/configuration-reference/reporting-settings.md#reporting-kibana-server-settings) are not configured correctly

Create a Markdown visualization and then create a PDF report. If this succeeds, increase the `xpack.reporting.queue.timeout` setting. If the PDF report fails with "Max attempts reached," check your [Kibana server settings](kibana://reference/configuration-reference/reporting-settings.md#reporting-kibana-server-settings).


## Verbose logging [reporting-troubleshooting-verbose-logs]

{{kib}} server logs have a lot of useful information for troubleshooting and understanding how things work. The full logs from {{report-features}} are a good place to look when you encounter problems. In [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
logging.root.level: all
```

For more information about logging, check out [Kibana configuration settings](kibana://reference/configuration-reference/general-settings.md#logging-root-level).



