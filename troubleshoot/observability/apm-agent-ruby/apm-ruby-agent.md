---
navigation_title: APM Ruby Agent
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/ruby/current/debugging.html
applies_to:
  stack: all
  serverless:
    observability: all
products:
  - id: apm-agent
---

# Troubleshoot APM Ruby Agent [debugging]

Hopefully the agent Just Works™, but depending on your situation the agent might need some tuning.

First, to learn more about what’s going on inside the agent, you can increase the amount of log messages it writes. To do this, set the log level with the option `log_level = 0` — `0` being the level of most messages, `DEBUG`.

In your `config/elastic_apm.yml`:

```yaml
log_level: <%= Logger::DEBUG %>
```


## Log messages [debugging-log-messages]


### `Queue is full (256 items), skipping…` [debugging-errors-queue-full]

The agent has an internal queue that holds events after they are done, and before they are safely serialized and sent to APM Server. To avoid using up all of your memory, this queue has a fixed size. Depending on your load and server setup, events may be added to the queue faster than they are consumed, hence the warning.

Things to consider:

* Is `server_url` misconfigured or APM Server down? If the agent fails to connect you will also see log messages containing `Connection error` or `Couldn't establish connection to APM Server`.
* Experiencing high load? The agent can spawn multiple instances of its Workers that pick off the queue by changing the option `pool_size` (default is `1`).
* If you have high load you may also consider setting `transaction_sample_rate` to something smaller than `1.0`. This determines whether to include *spans* for every *transaction*. If you have enough traffic, skipping some (probably) identical spans won’t have a noticeable effect on your data.


## Disable the Agent [disable-agent]

In the unlikely event the agent causes disruptions to a production application, you can disable the agent while you troubleshoot.

If you have access to [dynamic configuration](apm-agent-ruby://reference/configuration.md#dynamic-configuration), you can disable the recording of events by setting [`recording`](apm-agent-ruby://reference/configuration.md#config-recording) to `false`. When changed at runtime from a supported source, there’s no need to restart your application.

If that doesn’t work, or you don’t have access to dynamic configuration, you can disable the agent by setting [`enabled`](apm-agent-ruby://reference/configuration.md#config-enabled) to `false`. You’ll need to restart your application for the changes to apply.

