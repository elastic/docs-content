---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-security.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Scripting and security in Painless [modules-scripting-security]

As part of its core design, Painless provides secure scripting capabilities across {{es}}.

Introduced in [{{es}} 5.0](https://www.elastic.co/blog/painless-a-new-scripting-language) as a replacement for Groovy, Painless is purpose-built for {{es}}, enabling native performance while preventing unauthorized access to system resources.
   
By operating in a controlled sandbox environment, Painless ensures that you won’t get compromised when using it. Painless only allows pre-approved operations through fine-grained allowlists. Scripts cannot access file systems, networks, or other system resources that could compromise your cluster while still providing the flexibility you need for search scoring, data processing, and operational automation.

## Security Architecture Overview

:::{image} /explore-analyze/images/elasticsearch-painless-security-architecture-overview.png
:alt: Flow chart showing four layers of security between script request and safe script execution
:width: 350px
:::

The fine-grained allowlist operates as the **first security layer**. Anything that is not part of the allowlist will result in a compilation error.   
   
The **second layer of security** is [Java Security Manager (JSM)](https://www.oracle.com/java/technologies/javase/seccodeguide.html). As part of its startup sequence, {{es}} enables JSM to limit the actions that portions of the code can take. Painless uses this additional layer of defense to prevent scripts from doing things such as writing files and listening to sockets.

{{es}} uses [Seccomp](https://en.wikipedia.org/wiki/Seccomp) in Linux, [Seatbelt](https://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design) in macOS, and [ActiveProcessLimit](https://msdn.microsoft.com/en-us/library/windows/desktop/ms684147) on Windows as **additional security layers** to prevent {{es}} from forking or running other processes.

Finally, scripts used in [scripted metrics aggregations](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md) can be restricted to a defined list of scripts or forbidden altogether. This can prevent users from running particularly slow or resource-intensive aggregation queries.

You can modify the allowed script types setting to restrict the type of scripts that are allowed to run and control the available [contexts](elasticsearch://reference/scripting-languages/painless/painless-contexts.md) that scripts can run in. As well, you can use the {{es}} [security features](/deploy-manage/security.md) to enhance your defence strategy.

## Allowed script types setting [allowed-script-types-setting]

{{es}} supports two script types: `inline` and `stored`. By default, {{es}} is configured to run both types of scripts. To limit what type of scripts are run, set `script.allowed_types` to `inline` or `stored`. To prevent any scripts from running, set `script.allowed_types` to `none`. If you use Kibana, set `script.allowed_types` to both or just `inline`. Some Kibana features rely on inline scripts and do not function as expected if {{es}} does not allow inline scripts. 

For example, to run `inline` scripts but not `stored` scripts:

```
script.allowed_types: inline
```

## Allowed script contexts setting [allowed-script-contexts-setting]

By default, all script contexts are permitted. Use the `script.allowed_contexts` setting to specify the contexts that are allowed. To specify that no contexts are allowed, set `script.allowed_contexts` to `none`. For example, to allow scripts to run only in `scoring` and `update` contexts:

```
script.allowed_contexts: score, update
```

## Allowed scripts in scripted metrics aggregations [allowed-script-in-aggs-settings]

By default, all scripts are permitted in [scripted metrics aggregations](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md). To restrict the set of allowed scripts, set [`search.aggs.only_allowed_metric_scripts`](elasticsearch://reference/elasticsearch/configuration-reference/search-settings.md#search-settings-only-allowed-scripts) to `true` and provide the allowed scripts using [`search.aggs.allowed_inline_metric_scripts`](elasticsearch://reference/elasticsearch/configuration-reference/search-settings.md#search-settings-allowed-inline-scripts) and/or [`search.aggs.allowed_stored_metric_scripts`](elasticsearch://reference/elasticsearch/configuration-reference/search-settings.md#search-settings-allowed-stored-scripts).

To disallow certain script types, omit the corresponding script list (`search.aggs.allowed_inline_metric_scripts` or `search.aggs.allowed_stored_metric_scripts`) or set it to an empty array. When both script lists are not empty, the given stored scripts and the given inline scripts will be allowed.

```yaml
search.aggs.only_allowed_metric_scripts: true
search.aggs.allowed_inline_metric_scripts: []
search.aggs.allowed_stored_metric_scripts:
   - script_id_1
   - script_id_2
   - script_id_3
   - script_id_4
```

Conversely, the next example allows specific inline scripts but no stored scripts:

```yaml
search.aggs.only_allowed_metric_scripts: true
search.aggs.allowed_inline_metric_scripts:
   - 'state.transactions = []'
   - 'state.transactions.add(doc.some_field.value)'
   - 'long sum = 0; for (t in state.transactions) { sum += t } return sum'
   - 'long sum = 0; for (a in states) { sum += a } return sum'
search.aggs.allowed_stored_metric_scripts: []
```
