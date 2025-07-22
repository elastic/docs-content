---
navigation_title: Known issues
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

:::{dropdown} Observability AI Assistant - Elastic Managed LLM may be automatically selected as default connector

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

The issue involves semantic_text field type (and thus the semantic_text migration which is causing this issue), introduced in the knowledge base feature in 8.17.

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