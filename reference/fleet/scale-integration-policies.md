---
navigation_title: Reduce integration policies
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-environment-variables.html
description: Use one Fleet integration policy for many hosts by referencing Elastic Agent variables, sharing policies across agent policies, and grouping agents by role.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Reduce the number of integration policies [scale-integration-policies]

When you monitor many hosts that run the same service (for example, a fleet of databases, a group of message brokers, or a set of application servers), you don't need a separate integration policy for each host. One integration policy can serve every host, with each {{agent}} supplying the values that vary locally, such as a connection string or a log directory.

Keeping the number of integration policies low makes your configuration easier to maintain, and keeps you within the [policy scaling limits](/reference/fleet/agent-policy.md#agent-policy-scale).

You can consolidate integration policies in the following ways:

* [Reuse one integration policy with variables](#reuse-one-integration-policy-with-variables), so that each host supplies its own values.
* [Share an integration policy across {{agent}} policies](#share-an-integration-policy-across-agent-policies), so that one policy covers several groups of hosts.
* [Group agents by role](#group-agents-by-role), so that your policies match how your infrastructure is organized.


## Why a shared host list doesn't work [why-a-shared-host-list-doesnt-work]

Many integrations accept more than one value in their host field. It's tempting to add every host to a single integration policy, but this doesn't do what you might expect.

An integration policy applies to *every* {{agent}} enrolled in the {{agent}} policy that contains it. If you list 200 database hosts, each of your 200 agents tries to connect to all 200 of them, not only the one it's meant to monitor.

Where an agent can't reach the other hosts, those connections fail and the integration reports an unhealthy status. Where it can reach them, each host is polled by every agent, and you collect the same data 200 times over.

Use a host field to list several hosts only when you want every agent in the policy to connect to each one. To give each agent its own host, use a variable instead.


## Reuse one integration policy with variables [reuse-one-integration-policy-with-variables]

Instead of hardcoding a value in an integration policy, you can reference a variable that each {{agent}} resolves at runtime. {{agent}} [providers](/reference/fleet/providers.md) supply these variables, and they're available to {{fleet}}-managed agents without any setup.

::::{note}
You can use provider variables in {{fleet}}, but you can't add a `providers` configuration block through the {{fleet}} UI. To change provider settings for a {{fleet}}-managed agent, refer to [{{agent}} providers](/reference/fleet/providers.md#using-providers-fleet-managed-agent).
::::

The most useful providers for this purpose are:

| Provider | Example variables | Use it for |
| --- | --- | --- |
| [Env](/reference/fleet/env-provider.md) | `${env.VAR_NAME}` | Values you define per host, such as connection strings or credentials paths. |
| [Host](/reference/fleet/host-provider.md) | `${host.name}`, `${host.platform}` | Values derived from the host itself, such as hostnames in log paths. |
| [Agent](/reference/fleet/agent-provider.md) | `${agent.id}` | Values that identify the agent. |

Wherever an integration setting varies from host to host, replace it with one of these variables. The following sections show how to do that for a database connection, and how to fall back to a default when a variable isn't defined.


### Reuse a policy across database hosts [reuse-a-policy-across-database-hosts]

To monitor 200 database hosts with a single Oracle integration policy, set the connection field to an `env` provider variable, then define that variable on each host:

1. Add the Oracle integration to an {{agent}} policy, as described in [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md).
2. Set **Oracle DSN** to a value that references an environment variable:

    ```text
    ${env.ORACLE_DSN}
    ```

3. Click **Save and continue**.
4. On each host, define `ORACLE_DSN` with the connection string for the database that runs on that host. For example, on a host using `systemd`:

    ```ini
    [Service]

    Environment="ORACLE_DSN=oracle://db-042.example.com:1521/ORCLCDB.localdomain?sysdba=1"
    ```

    The location depends on your operating system and service manager. [Where to set proxy environment variables](/reference/fleet/host-proxy-env-vars.md#where-to-set-proxy-env-vars) covers the Windows registry, systemd, and other Linux distributions. Those locations apply to any variable that {{agent}} reads, not only proxy settings.

5. Restart {{agent}} on the host so that it picks up the new environment variable.

Each agent resolves `${env.ORACLE_DSN}` to its own connection string, so a single integration policy covers all 200 hosts. To onboard another database, define the environment variable on the new host and enroll it in the same {{agent}} policy. The policy itself doesn't change.

These steps use a connection string, but the same approach works for any integration setting that differs between hosts, and for any of the variables listed in the preceding table. For example, set a filestream path to `${env.APP_LOG_DIR}/app.log` when applications log to different directories, or to `/var/log/${host.name}/app.log` to build the path from the hostname itself.


### Set a fallback value [set-a-fallback-value]

If a variable isn't defined on a host, {{agent}} removes the input that references it from the generated configuration. This is often the behavior you want, because an agent shouldn't collect data for a service that it doesn't run.

When you'd rather fall back to a default, chain alternatives with `|` and end with a constant in quotes:

```text
${env.ORACLE_DSN|env.DEFAULT_DSN|'oracle://localhost:1521/ORCLCDB.localdomain?sysdba=1'}
```

{{agent}} evaluates the alternatives from left to right and uses the first one that's set. For the full syntax, refer to [Variables and conditions in input configurations](/reference/fleet/dynamic-input-configuration.md#_alternative_variables_and_constants).


## Share an integration policy across {{agent}} policies [share-an-integration-policy-across-agent-policies]

A single integration policy can belong to more than one {{agent}} policy. This is useful when several groups of hosts need the same integration configured the same way, but differ in other respects.

For example, if your Linux web servers and Linux database servers both need identical audit log collection, add one audit integration policy to both {{agent}} policies rather than maintaining two copies.

To add an integration to several {{agent}} policies at once, use the **Existing hosts** tab when you add the integration, and select multiple policies from the drop-down menu. To change the policies later, edit the integration and update the **Agent policies** field. For the full steps, refer to [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md).

When you edit a shared integration policy, the change reaches the agents in every {{agent}} policy that uses it.

::::{note}
This feature, known as **reusable integration policies**, is available only for certain subscription levels. For more information, refer to [Elastic subscriptions](https://www.elastic.co/subscriptions).
::::

If a shared integration policy needs to send data to a different output than its parent {{agent}} policy, refer to [Set integration-level outputs](/reference/fleet/integration-level-outputs.md).


## Group agents by role [group-agents-by-role]

The number of {{agent}} policies you need depends on how you group your hosts. Group agents by what they run rather than by individual host, so that hosts with the same role share a policy.

For example, a policy per role such as *Linux web servers*, *Windows workstations*, or *database servers* scales to any number of hosts, whereas a policy per host doesn't. Combined with variables, a small number of role-based policies can cover a large deployment.

Keep the following limits in mind as you plan:

* A single instance of {{fleet}} supports a maximum of 1000 {{agent}} policies, or 500 on {{serverless-full}}. For more details, refer to [Policy scaling recommendations](/reference/fleet/agent-policy.md#agent-policy-scale).
* A single {{agent}} policy supports a maximum of 10,000 integration policies. For more details, refer to [Scaling limitations of integration package policies](/reference/fleet/agent-policy.md#integration-policies-scale-limitations).


## Check the configuration an agent receives [check-the-configuration-an-agent-receives]

After you introduce variables, confirm that agents generate the configuration you expect.

To view the policy as {{fleet}} sends it, go to **Agent policies**, select your policy, and click **Actions** → **View policy**. Variables appear unresolved here, because each agent resolves them locally.

To see the result after substitution, run the following command on a host:

```shell
elastic-agent inspect --variables
```

The output shows the inputs that {{agent}} generates once variables are replaced. If an input is missing, a variable it references is probably undefined on that host. For more details, refer to [Debugging](/reference/fleet/dynamic-input-configuration.md#debug-configs).
