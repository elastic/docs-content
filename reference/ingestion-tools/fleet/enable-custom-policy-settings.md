---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/enable-custom-policy-settings.html
---

# Enable custom settings in an agent policy [enable-custom-policy-settings]

In certain cases it can be useful to enable custom settings that are not available in {{fleet}}, and that override the default behavior for {{agent}}.

::::{warning}
Use these custom settings with caution as they are intended for special cases. We do not test all possible combinations of settings which will be passed down to the components of {{agent}}, so it is possible that certain custom configurations can result in breakages.
::::


* [Configure the agent download timeout](#configure-agent-download-timeout)


## Configure the agent download timeout [configure-agent-download-timeout]

You can configure the the amount of time that {{agent}} waits for an upgrade package download to complete. This is useful in the case of a slow or intermittent network connection.

```shell
PUT kbn:/api/fleet/agent_policies/<policy-id>
{
  "name": "Test policy",
  "namespace": "default",
  "overrides": {
    "agent": {
      "download": {
        "timeout": "120s"
      }
    }
  }
}
```

