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
::::

## How to run {{esql}} queries

In this tutorial, {{esql}} examples are displayed in the following format:

```esql
FROM windows-security-logs
| WHERE event.code == "4624"
| LIMIT 1000
```

You can run these queries using:

- **Interactive interfaces**:
  - [Timeline](/solutions/security/investigate/timeline.md#esql-in-timeline). Find **Timelines** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
  - [Discover](/explore-analyze/discover/try-esql.md). Find **Discover** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

- **REST API** via [Dev Tools Console](elasticsearch://reference/query-languages/esql/esql-rest.md#esql-kibana-console). This requires additional formatting:
  :::{dropdown} View Console syntax for {{esql}}
  ```console
  POST /_query?format=txt
  {
    "query": """
      FROM windows-security-logs
      | WHERE event.code == "4624"
      | LIMIT 1000
    """
  }
  ```
  :::

## Step 0: Add sample data

To follow along with this tutorial, you need to add sample data to your cluster, using the [Dev Tools Console](elasticsearch://reference/query-languages/esql/esql-rest.md#esql-kibana-console).

Broadly, there are two types of data:

1. **Core indices**: These are the main security indices that contain the logs and events you want to analyze. We need three core indices: `windows-security-logs`, `process-logs`, and `network-logs`.
2. **Lookup indices**: These are auxiliary indices that provide additional context to your core data. We need three lookup indices: `asset-inventory`, `user-context`, and `threat-intel`.

### Create core indices

First, create the core security indices for our threat hunting scenario:

```console
PUT /windows-security-logs
{
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "event": {
        "properties": {
          "code": {"type": "keyword"}, # Event codes like 4624 (successful logon) and 4625 (failed logon) are stored as keywords for exact matching.
          "action": {"type": "keyword"}
        }
      },
      "user": {
        "properties": {
          "name": {"type": "keyword"},
          "domain": {"type": "keyword"}
        }
      },
      "host": {
        "properties": {
          "name": {"type": "keyword"},
          "ip": {"type": "ip"}
        }
      },
      "source": {
        "properties": {
          "ip": {"type": "ip"}
        }
      },
      "logon": {
        "properties": {
          "type": {"type": "keyword"}
        }
      }
    }
  }
}
```

Now let's add some sample data to the `windows-security-logs` index around authentication events, namely failed and successful logins.

```console
POST /_bulk?refresh=wait_for
{"index":{"_index":"windows-security-logs"}}
{"@timestamp":"2025-05-20T08:15:00Z","event":{"code":"4625","action":"logon_failed"},"user":{"name":"jsmith","domain":"corp"},"host":{"name":"WS-001","ip":"10.1.1.50"},"source":{"ip":"10.1.1.100"}}
{"index":{"_index":"windows-security-logs"}}
{"@timestamp":"2025-05-20T08:17:00Z","event":{"code":"4624","action":"logon_success"},"user":{"name":"jsmith","domain":"corp"},"host":{"name":"WS-001","ip":"10.1.1.50"},"source":{"ip":"10.1.1.100"},"logon":{"type":"3"}}
{"index":{"_index":"windows-security-logs"}}
{"@timestamp":"2025-05-20T09:30:00Z","event":{"code":"4624","action":"logon_success"},"user":{"name":"jsmith","domain":"corp"},"host":{"name":"SRV-001","ip":"10.1.2.10"},"source":{"ip":"10.1.1.50"},"logon":{"type":"3"}}
{"index":{"_index":"windows-security-logs"}}
{"@timestamp":"2025-05-20T10:45:00Z","event":{"code":"4624","action":"logon_success"},"user":{"name":"jsmith","domain":"corp"},"host":{"name":"DB-001","ip":"10.1.3.5"},"source":{"ip":"10.1.2.10"},"logon":{"type":"3"}}
{"index":{"_index":"windows-security-logs"}}
{"@timestamp":"2025-05-20T02:30:00Z","event":{"code":"4624","action":"logon_success"},"user":{"name":"admin","domain":"corp"},"host":{"name":"DC-001","ip":"10.1.4.10"},"source":{"ip":"10.1.3.5"},"logon":{"type":"3"}}
```

Next, create an index for process execution logs.

```console
PUT /process-logs
{
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "process": {
        "properties": {
          "name": {"type": "keyword"},
          "command_line": {"type": "text"}, # Command lines are stored as text fields to enable full-text search for suspicious parameters and encoded commands.
          "parent": {
            "properties": {
              "name": {"type": "keyword"}
            }
          }
        }
      },
      "user": {
        "properties": {
          "name": {"type": "keyword"}
        }
      },
      "host": {
        "properties": {
          "name": {"type": "keyword"}
        }
      }
    }
  }
}
```

Add some sample data to the `process-logs` index.

```console
POST /_bulk?refresh=wait_for
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T08:20:00Z","process":{"name":"powershell.exe","command_line":"powershell.exe -enc JABzAD0ATgBlAHcALgBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAA=","parent":{"name":"winword.exe"}},"user":{"name":"jsmith"},"host":{"name":"WS-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T09:35:00Z","process":{"name":"net.exe","command_line":"net user /domain","parent":{"name":"cmd.exe"}},"user":{"name":"jsmith"},"host":{"name":"SRV-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T10:50:00Z","process":{"name":"sqlcmd.exe","command_line":"sqlcmd -S localhost -Q \"SELECT * FROM customers\"","parent":{"name":"powershell.exe"}},"user":{"name":"jsmith"},"host":{"name":"DB-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T02:35:00Z","process":{"name":"ntdsutil.exe","command_line":"ntdsutil \"ac i ntds\" \"ifm\" \"create full c:\\temp\\ntds\"","parent":{"name":"cmd.exe"}},"user":{"name":"admin"},"host":{"name":"DC-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T12:15:00Z","process":{"name":"schtasks.exe","command_line":"schtasks.exe /create /tn UpdateCheck /tr c:\\windows\\temp\\update.exe /sc daily","parent":{"name":"cmd.exe"}},"user":{"name":"jsmith"},"host":{"name":"WS-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T12:30:00Z","process":{"name":"schtasks.exe","command_line":"schtasks.exe /create /tn SystemManager /tr powershell.exe -enc ZQBjAGgAbwAgACIASABlAGwAbABvACIA /sc minute /mo 5","parent":{"name":"powershell.exe"}},"user":{"name":"jsmith"},"host":{"name":"SRV-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T13:15:00Z","process":{"name":"sc.exe","command_line":"sc.exe create RemoteService binPath= c:\\windows\\temp\\remote.exe","parent":{"name":"cmd.exe"}},"user":{"name":"jsmith"},"host":{"name":"DB-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T13:20:00Z","process":{"name":"sc.exe","command_line":"sc.exe create BackdoorService binPath= c:\\programdata\\svc.exe","parent":{"name":"powershell.exe"}},"user":{"name":"jsmith"},"host":{"name":"SRV-001"}}
{"index":{"_index":"process-logs"}}
{"@timestamp":"2025-05-20T13:25:00Z","process":{"name":"sc.exe","command_line":"sc.exe create PersistenceService binPath= c:\\windows\\system32\\malicious.exe","parent":{"name":"cmd.exe"}},"user":{"name":"admin"},"host":{"name":"DC-001"}}
```

Next, create an index for network traffic logs.

```console
PUT /network-logs
{
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "source": {
        "properties": {
          "ip": {"type": "ip"},
          "port": {"type": "integer"}
        }
      },
      "destination": {
        "properties": {
          "ip": {"type": "ip"},
          "port": {"type": "integer"}
        }
      },
      "network": {
        "properties": {
          "bytes": {"type": "long"},
          "protocol": {"type": "keyword"}
        }
      },
      "host": {
        "properties": {
          "name": {"type": "keyword"}
        }
      }
    }
  }
}
```

Add some sample data to the `network-logs` index.

```console
POST /_bulk?refresh=wait_for
{"index":{"_index":"network-logs"}}
{"@timestamp":"2025-05-20T08:25:00Z","source":{"ip":"10.1.1.50","port":52341},"destination":{"ip":"185.220.101.45","port":443},"network":{"bytes":2048,"protocol":"tcp"},"host":{"name":"WS-001"}}
{"index":{"_index":"network-logs"}}
{"@timestamp":"2025-05-20T11:15:00Z","source":{"ip":"10.1.3.5","port":54892},"destination":{"ip":"185.220.101.45","port":443},"network":{"bytes":50000000,"protocol":"tcp"},"host":{"name":"DB-001"}}
{"index":{"_index":"network-logs"}}
{"@timestamp":"2025-05-20T02:40:00Z","source":{"ip":"10.1.4.10","port":61234},"destination":{"ip":"185.220.101.45","port":443},"network":{"bytes":500000000,"protocol":"tcp"},"host":{"name":"DC-001"}}
```

### Create lookup indices

The lookup mode enables these indices to be used with [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) operations for enriching security events with asset context.

Create the indices we need with the `lookup` index mode.

```console
PUT /asset-inventory
{
  "mappings": {
    "properties": {
      "host.name": {"type": "keyword"},
      "asset.criticality": {"type": "keyword"},
      "asset.owner": {"type": "keyword"},
      "asset.department": {"type": "keyword"}
    }
  },
  "settings": {
    "index.mode": "lookup" 
  }
}
```

```console
PUT /user-context
{
  "mappings": {
    "properties": {
      "user.name": {"type": "keyword"},
      "user.role": {"type": "keyword"},
      "user.department": {"type": "keyword"},
      "user.privileged": {"type": "boolean"}
    }
  },
  "settings": {
    "index.mode": "lookup"
  }
}
```

```console
PUT /threat-intel
{
  "mappings": {
    "properties": {
      "indicator.value": {"type": "keyword"},
      "indicator.type": {"type": "keyword"},
      "threat.name": {"type": "keyword"},
      "threat.severity": {"type": "keyword"}
    }
  },
  "settings": {
    "index.mode": "lookup"
  }
}
```

Now we can populate the lookup indices with contextual data. This single bulk operation indexes data into the `user-context`, `threat-intel` and `asset-inventory` indices with one request.

```console
POST /_bulk?refresh=wait_for
{"index":{"_index":"asset-inventory"}}
{"host.name":"WS-001","asset.criticality":"medium","asset.owner":"IT","asset.department":"finance"}
{"index":{"_index":"asset-inventory"}}
{"host.name":"SRV-001","asset.criticality":"high","asset.owner":"IT","asset.department":"operations"}
{"index":{"_index":"asset-inventory"}}
{"host.name":"DB-001","asset.criticality":"critical","asset.owner":"DBA","asset.department":"finance"}
{"index":{"_index":"asset-inventory"}}
{"host.name":"DC-001","asset.criticality":"critical","asset.owner":"IT","asset.department":"infrastructure"}
{"index":{"_index":"user-context"}}
{"user.name":"jsmith","user.role":"analyst","user.department":"finance","user.privileged":false}
{"index":{"_index":"user-context"}}
{"user.name":"admin","user.role":"administrator","user.department":"IT","user.privileged":true}
{"index":{"_index":"threat-intel"}}
{"indicator.value":"185.220.101.45","indicator.type":"ip","threat.name":"APT-29","threat.severity":"high"}
{"index":{"_index":"threat-intel"}}
{"indicator.value":"powershell.exe","indicator.type":"process","threat.name":"Living off the Land","threat.severity":"medium"}
```

## Step 1: Hunt for initial compromise indicators

The first phase of our hunt focuses on identifying the initial compromise. We want to search for suspicious PowerShell execution from Office applications, which is a common initial attack vector.

```esql
FROM process-logs
| WHERE process.name == "powershell.exe" AND process.parent.name LIKE "*word*" <1>
| LOOKUP JOIN asset-inventory ON host.name <2>
| LOOKUP JOIN user-context ON user.name <3>
| EVAL encoded_command = CASE(process.command_line LIKE "*-enc*", true, false) <4>
| WHERE encoded_command == true <5>
| STATS count = COUNT(*) BY host.name, user.name, asset.criticality <6>
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) with [`==`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-equals) and [`LIKE`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-like) operators to detect PowerShell processes 
2. Enriches using [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) with asset inventory
3. Enriches with user context using `LOOKUP JOIN`
4. Uses [`EVAL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-eval) and [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to detect encoded commands
5. Additional filtering with [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) 
6. Aggregates results with [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) and [`COUNT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count) grouped by multiple fields

**Response**

The response contains a summary of the suspicious PowerShell executions, including the host name, user name, and asset criticality.


     count     |   host.name   |   user.name   |asset.criticality
---------------|---------------|---------------|-----------------
1              |WS-001         |jsmith         |medium   


## Step 2: Detect lateral movement patterns

In this step, we track user authentication across multiple systems. This is important for identifying lateral movement and potential privilege escalation.

This query demonstrates how [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) creates time windows for velocity analysis, combining 
[`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) aggregations with [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) calculations to measure both the scope and speed of user movement across network assets.

```esql
FROM windows-security-logs
| WHERE event.code == "4624" AND logon.type == "3" <1>
| LOOKUP JOIN asset-inventory ON host.name
| EVAL time_bucket = DATE_TRUNC(30 minute, @timestamp) <2>
| STATS unique_hosts = COUNT_DISTINCT(host.name),
        criticality_levels = COUNT_DISTINCT(asset.criticality),
        active_periods = COUNT_DISTINCT(time_bucket),
        first_login = MIN(@timestamp),
        last_login = MAX(@timestamp) 
BY user.name <3>
| WHERE unique_hosts > 2
| EVAL time_span_hours = DATE_DIFF("hour", first_login, last_login) <4>
| EVAL movement_velocity = ROUND(unique_hosts / (time_span_hours + 1), 2)
| EVAL lateral_movement_score = unique_hosts * criticality_levels <5>
| SORT lateral_movement_score DESC 
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) for basic authentication filtering
2. Creates time buckets with [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) for temporal analysis
3. Uses [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) with [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) for comprehensive access metrics
4. Uses [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) for duration calculations
5. Uses [`EVAL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-eval) with [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case)for risk scoring

**Response**

The response shows users who logged into multiple hosts, their criticality levels, and the velocity of their lateral movement.

unique_hosts  |criticality_levels|active_periods |      first_login       |       last_login       |   user.name   |time_span_hours|movement_velocity|lateral_movement_score
---------------|------------------|---------------|------------------------|------------------------|---------------|---------------|-----------------|----------------------
3              |3                 |3              |2025-05-20T08:17:00.000Z|2025-05-20T10:45:00.000Z|jsmith         |2              |1                |9


## Step 3: Identify data access and potential exfiltration

Advanced attackers often target sensitive data. We want to hunt for database access and large data transfers to external systems.

```esql
FROM network-logs
| WHERE NOT CIDR_MATCH(destination.ip, "10.0.0.0/8", "192.168.0.0/16") <1>
| EVAL indicator.value = TO_STRING(destination.ip) <2>
| LOOKUP JOIN threat-intel ON indicator.value
| LOOKUP JOIN asset-inventory ON host.name
| WHERE threat.name IS NOT NULL
| STATS total_bytes = SUM(network.bytes),
        connection_count = COUNT(*),
        time_span = DATE_DIFF("hour", MIN(@timestamp), MAX(@timestamp)) <3>
BY host.name, destination.ip, threat.name, asset.criticality
| EVAL mb_transferred = ROUND(total_bytes / 1048576, 2) <4>
| EVAL risk_score = CASE(
    asset.criticality == "critical" AND mb_transferred > 100, 10,
    asset.criticality == "high" AND mb_transferred > 100, 7,
    mb_transferred > 50, 5,
    3
  ) <5>
| WHERE total_bytes > 1000000
| SORT risk_score DESC, total_bytes DESC
| LIMIT 1000
```

1. Uses [`CIDR_MATCH`](elasticsearch://reference/query-languages/esql/functions-operators/ip-functions.md#esql-cidr_match) to filter internal IP ranges for external data transfer detection
2. Uses [`TO_STRING`](elasticsearch://reference/query-languages/esql/functions-operators/type-conversion-functions.md#esql-to_string) to standardize IP format for threat intel lookups
3. Uses [`DATE_DIFF`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_diff) with `SUM` and `COUNT` to measure data transfer volume over time
4. Uses [`ROUND`](elasticsearch://reference/query-languages/esql/functions-operators/math-functions.md#esql-round) for human-readable values
5. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) for risk scoring based on asset criticality and size of data transferred

**Response**

The response shows external data transfers, their risk scores, and the amount of data transferred.

| total_bytes | connection_count | time_span | host.name | destination.ip | threat.name | asset.criticality | mb_transferred | risk_score |
|-------------|------------------|-----------|-----------|----------------|-------------|-------------------|----------------|------------|
| 500000000   | 1                | 0         | DC-001    | 185.220.101.45 | APT-29      | critical          | 476            | 10         |
| 50000000    | 1                | 0         | DB-001    | 185.220.101.45 | APT-29      | critical          | 47             | 3          |


## Step 4: Build an attack timeline and assess impact

To understand the attack progression, we need to build a timeline of events across multiple indices. This helps us correlate actions and identify the attacker's dwell time.


```esql
FROM windows-security-logs, process-logs, network-logs <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| WHERE user.name == "jsmith" OR user.name == "admin"
| EVAL event_type = CASE(
    event.code IS NOT NULL, "Authentication",
    process.name IS NOT NULL, "Process Execution",
    destination.ip IS NOT NULL, "Network Activity",
    "Unknown") <2>
| EVAL dest_ip = TO_STRING(destination.ip)
| EVAL attack_stage = CASE(
    process.parent.name LIKE "*word*", "Initial Compromise",
    process.name IN ("net.exe", "nltest.exe"), "Reconnaissance", 
    event.code == "4624" AND logon.type == "3", "Lateral Movement",
    process.name IN ("sqlcmd.exe", "ntdsutil.exe"), "Data Access",
    dest_ip NOT LIKE "10.*", "Exfiltration",
    "Other") <3>
| SORT @timestamp ASC <4>
| KEEP @timestamp, event_type, attack_stage, host.name, asset.criticality, user.name, process.name, destination.ip
| LIMIT 1000
```

1. Uses `FROM` with multiple indices for comprehensive correlation
2. Uses [`IS NOT NULL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#null-predicates) with [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to classify event types from different data sources
3. Uses complex [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) logic  to map events to MITRE ATT&CK stages
4. Uses [`SORT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort) to build chronological attack timeline
**Response**

The response provides a chronological timeline of events, showing the attacker's actions and the impact on the organization.

:::{dropdown} View response

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
:::

## Step 5: Hunt for unusual interpreter usage

This query demonstrates how {{esql}}'s [COUNT_DISTINCT](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) function and conditional [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) statements can be used to baseline interpreter usage patterns across users and departments, using aggregation functions to identify anomalous script execution that might indicate compromised accounts or insider threats.

```esql
FROM process-logs
| WHERE process.name IN ("powershell.exe", "cmd.exe", "net.exe", "sqlcmd.exe", "schtasks.exe", "sc.exe") <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| STATS executions = COUNT(*),
        unique_hosts = COUNT_DISTINCT(host.name),
        unique_commands = COUNT_DISTINCT(process.name) <3>
BY user.name, user.department
| WHERE executions > 1
| EVAL usage_pattern = CASE(
    executions > 5, "High Usage",
    executions > 3, "Moderate Usage", 
    "Low Usage"
  ) <4>
| SORT executions DESC
| LIMIT 1000
```

1. Uses `WHERE...IN` to monitor high-risk system tools
2. Uses [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) with `asset-inventory` and `user-context` indices to enrich events with context
3. Uses [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) to measure breadth of suspicious tool usage
4. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case)to classify usage patterns for anomaly detection

**Response**

The response shows the number of executions, unique hosts, and usage patterns for each user and department.

| executions | unique_hosts | unique_commands | user.name | user.department | usage_pattern |
|------------|--------------|-----------------|-----------|-----------------|---------------|
| 7          | 3            | 5               | jsmith    | finance         | High Usage    |

## Step 6: Hunt for persistence mechanisms

This query showcases how [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) enables temporal analysis of persistence mechanisms, using time bucketing and [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) to identify suspicious patterns like rapid-fire task creation or persistence establishment across multiple time windows.

```esql
FROM process-logs
| WHERE process.name == "schtasks.exe" AND process.command_line:"/create" <1>
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| EVAL time_bucket = DATE_TRUNC(1 hour, @timestamp) <2>
| STATS task_creations = COUNT(*),
        creation_hours = COUNT_DISTINCT(time_bucket) <3>
BY user.name, host.name, asset.criticality
| WHERE task_creations > 0
| EVAL persistence_pattern = CASE(
    creation_hours > 1, "Multiple Hours",
    task_creations > 1, "Burst Creation",
    "Single Task"
  ) <4>
| SORT task_creations DESC
| LIMIT 1000
```

1. Uses [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) with [`:`](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) match operator to detect scheduled task creation (a common persistence mechanism)
2. Uses [`DATE_TRUNC`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions.md#esql-date_trunc) to group events into hourly time buckets for temporal analysis
3. Uses [`COUNT_DISTINCT`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md#esql-count_distinct) with `time_bucket` to measure task creation velocity
4. Uses [`CASE`](elasticsearch://reference/query-languages/esql/functions-operators/conditional-functions-and-expressions.md#esql-case) to classify suspicious patterns based on timing and frequency

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


:::{tip}
To learn where you can use {{esql}} in {{elastic-sec}} contexts, refer to [the overview](/solutions/security/esql-for-security.md#documentation).
:::