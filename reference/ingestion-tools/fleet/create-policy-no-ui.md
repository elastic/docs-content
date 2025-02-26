---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/create-a-policy-no-ui.html
---

# Create an agent policy without using the UI [create-a-policy-no-ui]

For use cases where you want to provide a default agent policy or support automation, you can set up an agent policy without using the {{fleet}} UI. To do this, either use the {{fleet}} API or add a preconfigured policy to {{kib}}:


## Option 1. Create an agent policy with the API [use-api-to-create-policy]

```sh
curl -u <username>:<password> --request POST \
  --url <kibana_url>/api/fleet/agent_policies?sys_monitoring=true \
  --header 'content-type: application/json' \
  --header 'kbn-xsrf: true' \
  --data '{"name":"Agent policy 1","namespace":"default","monitoring_enabled":["logs","metrics"]}'
```

In this API call:

* `sys_monitoring=true` adds the system integration to the agent policy
* `monitoring_enabled` turns on {{agent}} monitoring

For more information, refer to [{{kib}} {{fleet}} APIs](/reference/ingestion-tools/fleet/fleet-api-docs.md).


## Option 2. Create agent policies with preconfiguration [use-preconfiguration-to-create-policy]

Add preconfigured policies to `kibana.yml` config.

For example, the following example adds a {{fleet-server}} policy for self-managed setup:

```yaml
xpack.fleet.packages:
  - name: fleet_server
    version: latest
xpack.fleet.agentPolicies:
  - name: Fleet Server policy
    id: fleet-server-policy
    namespace: default
    package_policies:
      - name: fleet_server-1
        package:
          name: fleet_server
```

The following example creates an agent policy for general use, and customizes the `period` setting for the `system.core` data stream. You can find all available inputs and variables in the **Integrations** app in {{kib}}.

```yaml
xpack.fleet.packages:
  - name: system
    version: latest
  - name: elastic_agent
    version: latest
xpack.fleet.agentPolicies:
  - name: Agent policy 1
    id: agent-policy-1
    namespace: default
    monitoring_enabled:
      - logs
      - metrics
    package_policies:
      - package:
          name: system
        name: System Integration 1
        id: preconfigured-system-1
        inputs:
          system-system/metrics:
            enabled: true
            vars:
              '[system.hostfs]': home/test
            streams:
              '[system.core]':
                enabled: true
                vars:
                  period: 20s
          system-winlog:
            enabled: false
```

For more information about preconfiguration settings, refer to the [{{kib}} documentation](kibana://docs/reference/configuration-reference/fleet-settings.md).
