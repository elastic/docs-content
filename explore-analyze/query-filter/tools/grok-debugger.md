---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-grokdebugger.html
---

# Grok debugger [xpack-grokdebugger]

You can build and debug grok patterns in the {{kib}} **Grok Debugger** before you use them in your data processing pipelines. Grok is a pattern matching syntax that you can use to parse arbitrary text and structure it. Grok is good for parsing syslog, apache, and other webserver logs, mysql logs, and in general, any log format that is written for human consumption.

Grok patterns are supported in {{es}} [runtime fields](../../../manage-data/data-store/mapping/runtime-fields.md), the {{es}} [grok ingest processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/grok-processor.html), and the {{ls}} [grok filter](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html). For syntax, see [Grokking grok](../../scripting/grok.md).

The {{stack}} ships with more than 120 reusable grok patterns. For a complete list of patterns, see [{{es}} grok patterns](https://github.com/elastic/elasticsearch/tree/master/libs/grok/src/main/resources/patterns) and [{{ls}} grok patterns](https://github.com/logstash-plugins/logstash-patterns-core/tree/master/patterns).

Because {{es}} and {{ls}} share the same grok implementation and pattern libraries, any grok pattern that you create in the **Grok Debugger** will work in both {{es}} and {{ls}}.


## Get started [grokdebugger-getting-started]

This example walks you through using the **Grok Debugger**. This tool is automatically enabled in {{kib}}.

::::{note}
If you’re using {{stack-security-features}}, you must have the `manage_pipeline` permission to use the Grok Debugger.
::::


1. Find the **Grok Debugger** by navigating to the **Developer tools** page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. In **Sample Data**, enter a message that is representative of the data that you want to parse. For example:

    ```ruby
    55.3.244.1 GET /index.html 15824 0.043
    ```

3. In **Grok Pattern**, enter the grok pattern that you want to apply to the data.

    To parse the log line in this example, use:

    ```ruby
    %{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}
    ```

4. Click **Simulate**.

   You’ll see the simulated event that results from applying the grok pattern.

   :::{image} ../../../images/kibana-grok-debugger-overview.png
   :alt: Grok Debugger
   :class: screenshot
   :::



## Test custom patterns [grokdebugger-custom-patterns]

If the default grok pattern dictionary doesn’t contain the patterns you need, you can define, test, and debug custom patterns using the **Grok Debugger**.

Custom patterns that you enter in the **Grok Debugger** are not saved. Custom patterns are only available for the current debugging session and have no side effects.

Follow this example to define a custom pattern.

1. In **Sample Data**, enter the following sample message:

    ```ruby
    Jan  1 06:25:43 mailserver14 postfix/cleanup[21403]: BEF25A72965: message-id=<20130101142543.5828399CCAF@mailserver14.example.com>
    ```

2. Enter this grok pattern:

    ```ruby
    %{SYSLOGBASE} %{POSTFIX_QUEUEID:queue_id}: %{MSG:syslog_message}
    ```

    Notice that the grok pattern references custom patterns called `POSTFIX_QUEUEID` and `MSG`.

3. Expand **Custom Patterns** and enter pattern definitions for the custom patterns that you want to use in the grok expression. You must specify each pattern definition on its own line.

    For this example, you must specify pattern definitions for `POSTFIX_QUEUEID` and `MSG`:

    ```ruby
    POSTFIX_QUEUEID [0-9A-F]{10,11}
    MSG message-id=<%{GREEDYDATA}>
    ```

4. Click **Simulate**.

   You’ll see the simulated output event that results from applying the grok pattern that contains the custom pattern:

   :::{image} ../../../images/kibana-grok-debugger-custom-pattern.png
   :alt: Debugging a custom pattern
   :class: screenshot
   :::

   If an error occurs, you can continue iterating over the custom pattern until the output matches the event that you expect.
