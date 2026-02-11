---
navigation_title: Known issues
products:
  - id: observability
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# {{observability}} known issues [elastic-observability-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{observability}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% Applies to: Applicable versions for the known issue
% Description of the known issue.
% For more information, check [Issue #](Issue link).
% **Impact**<br> Impact of the known issue.
% **Workaround**<br> Steps for a workaround until the known issue is fixed.

% :::

::::{dropdown} Browser monitors with JavaScript template literals fail on private locations
Applies to: All {{stack}} versions

**Details**

Browser monitors created through the {{kib}} Synthetics UI or the public APIs that are not using projects fail to run on private locations when inline scripts contain JavaScript template literals (`` `${variable}` ``).

A fix for this issue is expected in {{stack}} 9.4.

For more information, check [Issue #248](https://github.com/elastic/sdh-synthetics/issues/248).

**Workaround**

Use regular JavaScript string concatenation instead of template literals.

For example, instead of:

```js
step('Go to page', async () => {
  await page.goto(`${params.basePath}${params.route}`);
});
```

Use:

```js
step('Go to page', async () => {
  await page.goto(params.basePath + params.route);
});
```

Alternatively, you can switch to project monitors.

::::


::::{dropdown} Synthetics monitors statuses become pending after upgrade
Applies to: {{stack}} 8.19.5 and later

**Details**

When upgrading from a version before 8.19.5 to 8.19.5 or later, {{kib}} might unintentionally delete package policies for Synthetics project monitors during package policy cleanup. In deployments with many project monitors (10,000+ package policies in a single space), attempts to recreate deleted policies can fail and leave your instance in a broken state.

A fix for this issue was implemented in [#248762](https://github.com/elastic/kibana/pull/248762).

**Detecting missing package policies**

The following queries require superuser privileges. If you don't have superuser privileges and have pending monitors after upgrading, try making a dummy update to one of them through the UI to resolve the issue.

1. Check the task state:

    ```sh
    GET .kibana_*/_search
    {
      "size": 1,
      "query": {
        "bool": {
          "filter": [
            {
              "match_phrase": {
                "task.taskType": "Synthetics:Sync-Private-Location-Monitors"
              }
            }
          ]
        }
      }
    }
    ```

    If `hasAlreadyDoneCleanup` is `false` in the response and the task is timing out, you need to manually update the task state as shown in the following example. If `hasAlreadyDoneCleanup` is `true`, this issue most likely isn't causing your problem.

    ```sh
    POST .kibana_task_manager_9.3.0_001/_update/task:Synthetics:Sync-Private-Location-Monitors-single-instance
    {
      "doc": {
        "task": {
          "state": "{\"hasAlreadyDoneCleanup\":true, <copy the rest of the state from above response> }"
        }
      }
    }
    ```

2. Get the total count of monitors by summing the `allLocs` and `allLocsMulti` aggregation values:

    ```sh
    GET .kibana*/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            {
              "terms": {
                "type": [
                  "synthetics-monitor",
                  "synthetics-monitor-multi-space"
                ]
              }
            }
          ],
          "must_not": [
            {
              "terms": {
                "synthetics-monitor.locations.id": [
                  "asia-northeast1-a",
                  "asia-south1-a",
                  "asia-southeast1-a",
                  "australia-southeast1-a",
                  "europe-west2-a",
                  "europe-west3-a",
                  "northamerica-northeast1-a",
                  "southamerica-east1-a",
                  "us-east4-a",
                  "us-west1-a"
                ]
              }
            },
            {
              "terms": {
                "synthetics-monitor-multi-space.locations.id": [
                  "asia-northeast1-a",
                  "asia-south1-a",
                  "asia-southeast1-a",
                  "australia-southeast1-a",
                  "europe-west2-a",
                  "europe-west3-a",
                  "northamerica-northeast1-a",
                  "southamerica-east1-a",
                  "us-east4-a",
                  "us-west1-a"
                ]
              }
            }
          ]
        }
      },
      "aggs": {
        "allLocs": {
          "value_count": {
            "field": "synthetics-monitor-multi-space.locations.id"
          }
        },
        "allLocsMulti": {
          "value_count": {
            "field": "synthetics-monitor.locations.id"
          }
        }
      }
    }
    ```

3. Get the count of package policies:

    ```sh
    GET .kibana*/_search?track_total_hits=true
    {
      "size": 0,
      "_source": {
        "excludes": "ingest-package-policies.inputs"
      },
      "query": {
        "bool": {
          "filter": [
            {
              "term": {
                "type": "ingest-package-policies"
              }
            },
            {
              "term": {
                "ingest-package-policies.package.name": "synthetics"
              }
            }
          ]
        }
      }
    }
    ```

4. Compare the counts. If the package policy count doesn't match the monitor count, you have missing package policies and need to apply the workaround.

**Workaround**

Trigger package policy recreation using one of the following methods:

* Make a dummy update to the affected project monitors through the UI (for example, add a tag).
* Make a dummy edit to the private location configuration. Like editing the name of private location, this regenerates all package policies for that location's monitors.
* Push a dummy project monitor update, like adding a tag to the project monitor config and run a `npm run push`.

::::

:::{dropdown} Error when using the Kubernetes OpenTelemetry quickstart onboarding flow
Applies to: {{stack}}

**Details**

Users with Helm version 3.18.5 or later will see an error similar to the following when using the [Kubernetes OpenTelemetry quickstart](/solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md) onboarding flow:

```
Error: values don't meet the specifications of the schema(s) in the following chart(s):
opentelemetry-operator:
"file:///values.schema.json#" is not valid against metaschema: jsonschema validation failed with 'https://json-schema.org/draft/2019-09/schema#'
- at '': 'allOf' failed
  - at '/properties/manager': 'allOf' failed
    - at '/properties/manager/properties/featureGates': 'allOf' failed
      - at '/properties/manager/properties/featureGates/examples': got string, want array
```

For more information, check:
* [Issue 232667](https://github.com/elastic/kibana/pull/232667)
* [Issue 9535](https://github.com/elastic/elastic-agent/pull/9535)

**Workaround**

Downgrade Helm to version 3.18.4.

:::


:::{dropdown} Observability AI Assistant: Elastic Managed LLM may be automatically selected as default connector

Applies to: {{stack}} 9.x

The Elastic Managed LLM may be automatically selected as your default connector because of existing connector selection logic.
This can occur if you had not previously specified a connector for any of the following reasons:

* You only had one connector available and it was always automatically picked for your conversations.
* You had multiple connectors available but didn’t make a specific selection and used the automatically picked connector for your conversations.
* You previously selected a connector but cleared your browser's local storage or switched browsers or devices.

*And:*

* All of your existing connector names come after the “Elastic Managed LLM connector" when sorted alphabetically.

For more information, check [#2088](https://github.com/elastic/docs-content/issues/2088)

::::

::::{dropdown} Observability AI assistant gets stuck in a loop when attempting to call the `execute_connector` function
:name:known-issue-1508

Applies to: {{stack}} 9.0.0, 9.0.1, 9.0.2

**Details**

The Observability AI assistant gets stuck in a loop when calling the `execute_connector` function. Instead of completing queries, it times out with the error message `Failed to parse function call arguments when converting messages for inference: SyntaxError: Unexpected non-whitespace character after JSON at position 72 and Error: Tool call arguments for execute_connector (...) were invalid`.


::::

::::{dropdown} Observability AI assistant Knowledge Base entries with empty text can lead to Kibana OOM or restarts
:name:known-issue-220339

Applies to: {{stack}} 9.0.0

**Details**

The semantic text migration can cause excessive traffic to a cluster and might eventually cause the Kibana instance to crash due to OOM, together with increase of requests to Elasticsearch & ML nodes.

The problem can occur when there is one or more empty text Knowledge Base documents.

The migration script does not handle this scenario and will indefinitely update the same document.

Because the document update involves semantic_text an ML node is kept warm further increasing the costs.

The issue involves semantic_text field type (and the semantic_text migration which is causing this issue), introduced in the knowledge base feature in 8.17.

**Workaround**

1. Pause the Kibana instance if possible. If not possible, skip this step.
2. Run a dry run query to identify if you have empty Knowledge Base documents. If you have at least 1 hit, you can be affected by the problem.

    ```sh
    GET .kibana-observability-ai-assistant-kb/_search
    {
      "query": {
        "bool": {
          "must": [{ "exists": { "field": "text" }}],
          "must_not": [ { "wildcard": { "text": "*" } }
          ]
        }
      }
    }
    ```

3. Execute the deletion. For extra safety, you might want to trigger a snapshot before executing it.

    ```sh
    POST .kibana-observability-ai-assistant-kb/_delete_by_query
    {
      "query": {
        "bool": {
          "must": [{ "exists": { "field": "text" }}],
          "must_not": [ { "wildcard": { "text": "*" } }
          ]
        }
      }
    }
    ```

For more information, check:

- [#220339](https://github.com/elastic/kibana/issues/220339)
- [#220342](https://github.com/elastic/kibana/issues/220342)

::::

::::{dropdown} Profiling Collector and Symbolizer endpoints are not configured after upgrading a cluster

Applies to: {{stack}} 9.x, 8.x

**Details**

After upgrading a cluster, Collector and Symbolizer endpoints may not be configured even when Universal Profiling is enabled in Kibana and the "Add data" instructions appear on the Universal Profiling landing page.

**Workaround**

1. Run the following query to retrieve the `id`s of the `elastic-universal-profiling-collector` and `elastic-universal-profiling-symbolizer` package policies:

    ```sh
    GET kbn:/api/fleet/package_policies
    ```

2. Delete the package policies:

    ```sh
    DELETE kbn:/api/fleet/package_policies/<elastic-universal-profiling-collector-id>?force=true
    DELETE kbn:/api/fleet/package_policies/<elastic-universal-profiling-symbolizer-id>?force=true
    ```

::::

:::{dropdown} Error when using the Opentelemetry onboarding flow using EDOT Collector
Applies to: {{stack}} 9.1.6, 9.2.0

**Details**

Users trying to collect logs and host metrics using the Elastic distribution of the OTel collector will see error when using the OpenTelemetry quickstart onboarding flow:

```
> sudo ./otelcol --config otel.yml

Starting in otel mode
failed to get config: cannot unmarshal the configuration: decoding failed due to the following error(s):

'exporters' error reading configuration for "otlp/ingest": decoding failed due to the following error(s):

'sending_queue' decoding failed due to the following error(s):

'batch' decoding failed due to the following error(s):

'' has invalid keys: flush_interval

```

**Workaround**

To work around this issue, manually update the configuration of the generated `otel.yaml` file to replace incorrect key `flush_interval` with the correct key `flush_timeout`.

```yaml
batch:
  flush_timeout: 1s
```

::::
