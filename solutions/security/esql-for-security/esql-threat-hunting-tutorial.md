---
applies_to:
  stack: all
  serverless: all
products:
  - id: security
---

# Tutorial: Threat hunting with {{esql}}

This hands-on tutorial demonstrates advanced threat hunting techniques using the [Elasticsearch Query Language ({{esql}})](elasticsearch://reference/query-languages/esql.md). 

Following a simulated Advanced Persistent Threat (APT) campaign, we analyze security events across authentication, process execution, and network telemetry to detect:

- Initial compromise via malicious email attachments
- Lateral movement through the network 
- Privilege escalation attempts
- Data exfiltration activities

{{esql}} enables powerful transformations, filtering, enrichment, and statistical analysis, making it ideal for complex security investigations. This tutorial provides practical examples of how to leverage {{esql}} for threat hunting, from identifying suspicious user behavior to building attack timelines.

::::{admonition} Requirements
You need a running {{es}} cluster, together with {{kib}} to run this tutorial. Refer to [choose your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for deployment options.
::::::

## How to run {{esql}} queries

You have multiple options for running {{esql}} queries:

- **Interactive interfaces**:
  - [Timeline](/solutions/security/investigate/timeline.md#esql-in-timeline)
  - [Discover](/explore-analyze/discover/try-esql.md)
- **REST API**:
  - [Dev Tools Console](elasticsearch://reference/query-languages/esql/esql-rest.md#esql-kibana-console)
  - [{{es}} HTTP clients](/solutions/search/site-or-app/clients.md)
  - [`curl`](https://curl.se/)
 

## Step 0: Add sample data

To follow along with this tutorial, you need to add sample data to your cluster, using the {{es}} REST API and the Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) or your preferred HTTP client.

Broadly, there are two types of data:

1. **Core indices**: These are the main security indices that contain the logs and events you want to analyze. We need three core indices: `windows-security-logs`, `process-logs`, and `network-logs`.
2. **Lookup indices**: These are auxiliary indices that provide additional context to your core data. We need three lookup indices: `asset-inventory`, `user-context`, and `threat-intel`.

### Create core indices

First, create the core security indices for our threat hunting scenario:

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example1-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example1-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example1-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example1-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example1-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example1-ruby.md
:::

::::

Now let's add some sample data to the `windows-security-logs` index around authentication events, namely failed and successful logins.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example2-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example2-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example2-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example2-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example2-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example2-ruby.md
:::

::::

Next, create an index for process execution logs.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example3-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example3-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example3-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example3-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example3-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example3-ruby.md
:::

::::

Add some sample data to the `process-logs` index.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example4-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example4-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example4-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example4-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example4-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example4-ruby.md
:::

::::

Next, create an index for network traffic logs.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example5-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example5-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example5-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example5-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example5-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example5-ruby.md
:::

::::

Add some sample data to the `network-logs` index.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example6-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example6-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example6-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example6-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example6-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example6-ruby.md
:::

::::

### Create lookup indices

The lookup mode enables these indices to be used with [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) operations for enriching security events with asset context.

Create the indices we need with the `lookup` index mode.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example7-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example7-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example7-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example7-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example7-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example7-ruby.md
:::

::::

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example8-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example8-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example8-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example8-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example8-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example8-ruby.md
:::

::::

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example9-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example9-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example9-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example9-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example9-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example9-ruby.md
:::

::::

Now we can populate the lookup indices with contextual data. This single bulk operation indexes data into the `user-context`, `threat-intel` and `asset-inventory` indices with one request.

::::{tab-set}
:group: api-examples

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example10-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example10-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example10-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example10-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example10-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example10-ruby.md
:::

::::

## Step 1: Hunt for initial compromise indicators

The first phase of our hunt focuses on identifying the initial compromise. We want to search for suspicious PowerShell execution from Office applications, which is a common initial attack vector.

::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example11-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example11-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example11-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example11-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example11-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example11-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example11-ruby.md
:::

::::

**Response**

The response contains a summary of the suspicious PowerShell executions, including the host name, user name, and asset criticality.


     count     |   host.name   |   user.name   |asset.criticality
---------------|---------------|---------------|-----------------
1              |WS-001         |jsmith         |medium   


## Step 2: Detect lateral movement patterns

In this step, we track user authentication across multiple systems. This is important for identifying lateral movement and potential privilege escalation.

This query demonstrates how [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) creates time windows for velocity analysis, combining 
[`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) aggregations with [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) calculations to measure both the scope and speed of user movement across network assets.

::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example12-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example12-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example12-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example12-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example12-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example12-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example12-ruby.md
:::

::::

**Response**

The response shows users who logged into multiple hosts, their criticality levels, and the velocity of their lateral movement.

unique_hosts  |criticality_levels|active_periods |      first_login       |       last_login       |   user.name   |time_span_hours|movement_velocity|lateral_movement_score
---------------|------------------|---------------|------------------------|------------------------|---------------|---------------|-----------------|----------------------
3              |3                 |3              |2025-05-20T08:17:00.000Z|2025-05-20T10:45:00.000Z|jsmith         |2              |1                |9


## Step 3: Identify data access and potential exfiltration

Advanced attackers often target sensitive data. We want to hunt for database access and large data transfers to external systems.

::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example13-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example13-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example13-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example13-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example13-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example13-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example13-ruby.md
:::

::::

**Response**

The response shows external data transfers, their risk scores, and the amount of data transferred.

| total_bytes | connection_count | time_span | host.name | destination.ip | threat.name | asset.criticality | mb_transferred | risk_score |
|-------------|------------------|-----------|-----------|----------------|-------------|-------------------|----------------|------------|
| 500000000   | 1                | 0         | DC-001    | 185.220.101.45 | APT-29      | critical          | 476            | 10         |
| 50000000    | 1                | 0         | DB-001    | 185.220.101.45 | APT-29      | critical          | 47             | 3          |


## Step 4: Build an attack timeline and assess impact

To understand the attack progression, we need to build a timeline of events across multiple indices. This helps us correlate actions and identify the attacker's dwell time.


::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example14-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example14-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example14-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example14-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example14-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example14-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example14-ruby.md
:::

::::
**Response**

The response provides a chronological timeline of events, showing the attacker's actions and the impact on the organization.

::::{dropdown} View response

| @timestamp | event_type | attack_stage | host.name | asset.criticality | user.name | process.name | destination.ip |
|------------|------------|--------------|-----------|-------------------|-----------|--------------|----------------|
| 2025-05-20T02:30:00.000Z | Authentication | Lateral Movement | DC-001 | critical | admin | null | null |
| 2025-05-20T02:35:00.000Z | Process Execution | Data Access | DC-001 | critical | admin | ntdsutil.exe | null |
| 2025-05-20T08:15:00.000Z | Authentication | Other | WS-001 | medium | jsmith | null | null |
| 2025-05-20T08:17:00.000Z | Authentication | Lateral Movement | WS-001 | medium | jsmith | null | null |
| 2025-05-20T08:20:00.000Z | Process Execution | Initial Compromise | WS-001 | medium | jsmith | powershell.exe | null |
| 2025-05-20T09:30:00.000Z | Authentication | Lateral Movement | SRV-001 | high | jsmith | null | null |
| 2025-05-20T09:35:00.000Z | Process Execution | Reconnaissance | SRV-001 | high | jsmith | net.exe | null |
| 2025-05-20T10:45:00.000Z | Authentication | Lateral Movement | DB-001 | critical | jsmith | null | null |
| 2025-05-20T10:50:00.000Z | Process Execution | Data Access | DB-001 | critical | jsmith | sqlcmd.exe | null |
| 2025-05-20T12:15:00.000Z | Process Execution | Other | WS-001 | medium | jsmith | schtasks.exe | null |
| 2025-05-20T12:30:00.000Z | Process Execution | Other | SRV-001 | high | jsmith | schtasks.exe | null |
| 2025-05-20T13:15:00.000Z | Process Execution | Other | DB-001 | critical | jsmith | sc.exe | null |
| 2025-05-20T13:20:00.000Z | Process Execution | Other | SRV-001 | high | jsmith | sc.exe | null |
| 2025-05-20T13:25:00.000Z | Process Execution | Other | DC-001 | critical | admin | sc.exe | null |
::::

## Step 5: Hunt for unusual interpreter usage

This query demonstrates how {{esql}}'s [COUNT_DISTINCT](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) function and conditional [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) statements can be used to baseline interpreter usage patterns across users and departments, using aggregation functions to identify anomalous script execution that might indicate compromised accounts or insider threats.

::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example15-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example15-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example15-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example15-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example15-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example15-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example15-ruby.md
:::

::::

**Response**

The response shows the number of executions, unique hosts, and usage patterns for each user and department.

| executions | unique_hosts | unique_commands | user.name | user.department | usage_pattern |
|------------|--------------|-----------------|-----------|-----------------|---------------|
| 7          | 3            | 5               | jsmith    | finance         | High Usage    |

## Step 6: Hunt for persistence mechanisms

This query showcases how [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) enables temporal analysis of persistence mechanisms, using time bucketing and [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) to identify suspicious patterns like rapid-fire task creation or persistence establishment across multiple time windows.

::::{tab-set}
:group: api-examples

:::{tab-item} ES|QL
:sync: esql

:::{include} _snippets/esql-threat-hunting-tutorial/example16-esql.md
:::

:::{tab-item} Console
:sync: console

:::{include} _snippets/esql-threat-hunting-tutorial/example16-console.md
:::

:::{tab-item} curl
:sync: curl

:::{include} _snippets/esql-threat-hunting-tutorial/example16-curl.md
:::

:::{tab-item} Python
:sync: python

:::{include} _snippets/esql-threat-hunting-tutorial/example16-python.md
:::

:::{tab-item} JavaScript
:sync: js

:::{include} _snippets/esql-threat-hunting-tutorial/example16-js.md
:::

:::{tab-item} PHP
:sync: php

:::{include} _snippets/esql-threat-hunting-tutorial/example16-php.md
:::

:::{tab-item} Ruby
:sync: ruby

:::{include} _snippets/esql-threat-hunting-tutorial/example16-ruby.md
:::

::::

**Response**

The response shows the number of task creations, creation hours, and persistence patterns for each user and host.

| task_creations | creation_hours | user.name | host.name | asset.criticality | persistence_pattern |
|----------------|----------------|-----------|-----------|-------------------|---------------------|
| 1              | 1              | jsmith    | WS-001    | medium            | Single Task         |
| 1              | 1              | jsmith    | SRV-001   | high              | Single Task         |

## Additional resources

- Explore a curated collection of threat hunting [queries](https://github.com/elastic/detection-rules/tree/main/hunting) in the `elastic/detection-rules` GitHub repo.
  - The corresponding [blog](https://www.elastic.co/security-labs/elevate-your-threat-hunting) provides more information about how to use them in your threat hunting workflows.
- Explore more threat hunting examples in the following blogs:
  - [Detect and prevent data exfiltration with {{elastic-sec}}](https://www.elastic.co/blog/security-exfiltration)
  - [Detecting command and scripting interpreter techniques](https://www.elastic.co/blog/detecting-command-scripting-interpreter)
  - [Detecting credential dumping with {{elastic-sec}}](https://www.elastic.co/blog/elastic-security-detecting-credential-dumping)
  - [Detecting covert data exfiltration techniques](https://www.elastic.co/blog/elastic-security-detecting-covert-data-exfiltration)


::::{tip}
To learn where you can use {{esql}} in {{elastic-sec}} contexts, refer to [the overview](/solutions/security/esql-for-security.md#documentation).
::::