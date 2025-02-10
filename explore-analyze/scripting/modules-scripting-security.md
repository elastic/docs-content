---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-security.html
---

# Scripting and security [modules-scripting-security]

Painless and {{es}} implement layers of security to build a defense in depth strategy for running scripts safely.

Painless uses a fine-grained allowlist. Anything that is not part of the allowlist results in a compilation error. This capability is the first layer of security in a defense in depth strategy for scripting.

The second layer of security is the [Java Security Manager](https://www.oracle.com/java/technologies/javase/seccodeguide.html). As part of its startup sequence, {{es}} enables the Java Security Manager to limit the actions that portions of the code can take. [Painless](modules-scripting-painless.md) uses the Java Security Manager as an additional layer of defense to prevent scripts from doing things like writing files and listening to sockets.

{{es}} uses [seccomp](https://en.wikipedia.org/wiki/Seccomp) in Linux, [Seatbelt](https://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design) in macOS, and [ActiveProcessLimit](https://msdn.microsoft.com/en-us/library/windows/desktop/ms684147) on Windows as additional security layers to prevent {{es}} from forking or running other processes.

Finally, scripts used in [scripted metrics aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html) can be restricted to a defined list of scripts, or forbidden altogether. This can prevent users from running particularly slow or resource intensive aggregation queries.

You can modify the following script settings to restrict the type of scripts that are allowed to run, and control the available [contexts](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-contexts.html) that scripts can run in. To implement additional layers in your defense in depth strategy, follow the [{{es}} security principles](../../deploy-manage/security.md).


## Allowed script types setting [allowed-script-types-setting] 

{{es}} supports two script types: `inline` and `stored`. By default, {{es}} is configured to run both types of scripts. To limit what type of scripts are run, set `script.allowed_types` to `inline` or `stored`. To prevent any scripts from running, set `script.allowed_types` to `none`.

::::{important} 
If you use {{kib}}, set `script.allowed_types` to both or just `inline`. Some {{kib}} features rely on inline scripts and do not function as expected if {{es}} does not allow inline scripts.
::::


For example, to run `inline` scripts but not `stored` scripts:

```yaml
script.allowed_types: inline
```


## Allowed script contexts setting [allowed-script-contexts-setting] 

By default, all script contexts are permitted. Use the `script.allowed_contexts` setting to specify the contexts that are allowed. To specify that no contexts are allowed, set `script.allowed_contexts` to `none`.

For example, to allow scripts to run only in `scoring` and `update` contexts:

```yaml
script.allowed_contexts: score, update
```


## Allowed scripts in scripted metrics aggregations [allowed-script-in-aggs-settings] 

By default, all scripts are permitted in [scripted metrics aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html). To restrict the set of allowed scripts, set [`search.aggs.only_allowed_metric_scripts`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-settings.html#search-settings-only-allowed-scripts) to `true` and provide the allowed scripts using [`search.aggs.allowed_inline_metric_scripts`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-settings.html#search-settings-allowed-inline-scripts) and/or [`search.aggs.allowed_stored_metric_scripts`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-settings.html#search-settings-allowed-stored-scripts).

To disallow certain script types, omit the corresponding script list (`search.aggs.allowed_inline_metric_scripts` or `search.aggs.allowed_stored_metric_scripts`) or set it to an empty array. When both script lists are not empty, the given stored scripts and the given inline scripts will be allowed.

The following example permits only 4 specific stored scripts to be used, and no inline scripts:

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

