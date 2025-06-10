---
applies_to:
  stack: all
  serverless: all
products:
  - id: security
---

# Tutorial: Threat hunting with {{esql}}

This is a hands-on introduction to threat hunting using the [Elasticsearch Query language ({{esql}})](/explore-analyze/query-filter/languages/esql.md), following a realistic advanced persistent threat (APT) campaign scenario. We'll investigate a sophisticated attack involving initial compromise via a malicious email attachment.
The attack escalates through lateral movement, privilege escalation, and data exfiltration.

Using ES|QL, you'll enrich raw security events with business context - asset criticality, user privileges, and threat intelligence - to build a complete picture of the attack and assess its impact on your organization.

## Requirements

You'll need a running {{es}} cluster, together with {{kib}}. Refer to [choose your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for deployment options.

## How to run {{esql}} queries

In this tutorial, you'll see {{esql}} examples in the following format:

```esql
FROM windows-security-logs
| WHERE event.code == "4624"
| LIMIT 1000
```

You can run these queries in [Discover](/explore-analyze/discover.md) or [Timeline](/solutions/security/investigate/timeline.md#esql-in-timeline) using the `ES|QL` query language.

If you want to run these queries in the [Dev Tools Console](/explore-analyze/query-filter/languages/esql-rest.md#esql-kibana-console), you'll need to use the following syntax:

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

If you'd prefer to use your favorite programming language, refer to [Client libraries](/solutions/search/site-or-app/clients.md) for a list of official and community-supported clients.

## Step 0: Add sample data

To follow along with this tutorial, you need to add sample data to your cluster, using the [Dev Tools Console](/explore-analyze/query-filter/languages/esql-rest.md#esql-kibana-console).

Broadly there are two types of data:

1. **Core indices**: These are the main security indices that contain the logs and events you want to analyze. In this tutorial, we'll create three core indices: `windows-security-logs`, `process-logs`, and `network-logs`.
2. **Lookup indices**: These are auxiliary indices that provide additional context to your core data. In this tutorial, we'll create three lookup indices: `asset-inventory`, `user-context`, and `threat-intel`.

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

Now let's add some sample data to the `windows-security-logs` index around authentication events i.e. failed and successful logins.

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

The lookup mode enables these indices to be used with `LOOKUP JOIN` operations for enriching security events with asset context.

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
```console
PUT /lolbins-lookup
{
  "mappings": {
    "properties": {
      "indicator.value": {"type": "keyword"},
      "lolbin": {"type": "boolean"},
      "description": {"type": "text"}
    }
  },
  "settings": {
    "index.mode": "lookup"
  }
}
```

Now we'll populate the lookup indices with contextual data. This single bulk operation indexes data into the `user-context`, `threat-intel`, `asset-inventory`, and `lolbins-lookup` indices with one request.

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
{"index":{"_index":"lolbins-lookup"}}
{"indicator.value":"powershell.exe","lolbin":true,"description":"Windows PowerShell execution engine"}
{"index":{"_index":"lolbins-lookup"}}
{"indicator.value":"cmd.exe","lolbin":true,"description":"Windows Command Processor"}
{"index":{"_index":"lolbins-lookup"}}
{"indicator.value":"wmic.exe","lolbin":true,"description":"Windows Management Instrumentation"}
```

## Step 1: Hunt for initial compromise indicators

The first phase of our hunt focuses on identifying the initial compromise. We'll look for suspicious PowerShell execution from Office applications, which is a common initial attack vector.

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

1. Uses `WHERE` with exact match (`==`) and pattern match (`LIKE`) operators to detect PowerShell processes spawned by Word
2. Enriches process data with asset inventory using `LOOKUP JOIN` to understand which business systems are affected
3. Adds user context to identify the compromised user account and their privileges
4. Creates a boolean field using `EVAL` and `CASE` to detect base64-encoded PowerShell commands (`-enc` parameter), which attackers use to obfuscate malicious code
5. Filters for only encoded commands using `WHERE` on the computed field - focusing on suspicious PowerShell usage
6. Aggregates results with `STATS` and `COUNT` grouped `BY` multiple fields

## Step 2: Detect lateral movement patterns

In this step, we will track user authentication across multiple systems. This is important for identifying lateral movement and potential privilege escalation.

This query demonstrates how `DATE_TRUNC()` creates time windows for velocity analysis, combining `COUNT_DISTINCT()` aggregations with `DATE_DIFF()` calculations to measure both the scope and speed of user movement across network assets.

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

1. Filters for successful remote logons (type 3) - key indicator for lateral movement detection
2. Creates 30-minute time buckets to analyze temporal patterns in authentication activity
3. Complex aggregation combining host uniqueness, criticality levels, and timing metrics
4. Calculates attack duration using `DATE_DIFF` to measure campaign timespan
5. Custom scoring formula weighing both breadth (systems accessed) and depth (criticality) of compromise

## Step 3: Identify data access and potential exfiltration

Advanced attackers often target sensitive data. We'll hunt for database access and large data transfers to external systems.

```esql
FROM network-logs
| EVAL dest_ip = TO_STRING(destination.ip) <1>
| WHERE dest_ip NOT LIKE "10.*" AND dest_ip NOT LIKE "192.168.*"
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

1. Converts IP addresses to strings to enable pattern matching with `LIKE` operator for identifying external destinations
2. Standardizes IP format for threat intel lookup join by casting to string type
3. Uses `DATE_DIFF` to calculate duration of data transfer activities in hours
4. Converts raw bytes to megabytes using division and `ROUND` for human-readable values
5. Assigns risk scores based on asset criticality and data volume using nested `CASE` conditions

## Step 4: Build an attack timeline and assess impact

To understand the attack progression, we need to build a timeline of events across multiple indices. This will help us correlate actions and identify the attacker's dwell time.


```esql
FROM windows-security-logs, process-logs, network-logs
| LOOKUP JOIN asset-inventory ON host.name
| LOOKUP JOIN user-context ON user.name
| WHERE user.name == "jsmith" OR user.name == "admin"
| EVAL event_type = CASE(
event.code IS NOT NULL, "Authentication",
process.name IS NOT NULL, "Process Execution",
destination.ip IS NOT NULL, "Network Activity",
"Unknown"
)
| EVAL dest_ip = TO_STRING(destination.ip)
| EVAL attack_stage = CASE(
process.parent.name LIKE "*word*", "Initial Compromise",
process.name IN ("net.exe", "nltest.exe"), "Reconnaissance",
event.code == "4624" AND logon.type == "3", "Lateral Movement",
process.name IN ("sqlcmd.exe", "ntdsutil.exe"), "Data Access",
dest_ip NOT LIKE "10.*", "Exfiltration", "Other")
| SORT @timestamp ASC
| KEEP @timestamp, event_type, attack_stage, host.name, asset.criticality, user.name, process.name, destination.ip
| LIMIT 1000
```

1. Querying multiple indices simultaneously provides comprehensive event correlation
2. Nested `CASE` with `IS NOT NULL` checks categorizes events by their source data structure
3. Complex conditional logic maps technical events to attack framework stages (MITRE ATT&CK)
4. `SORT ASC` creates chronological ordering essential for timeline analysis


## Step 5: Hunt for unusual interpreter usage

This query demonstrates how ESQL's COUNT_DISTINCT() and CASE statements can baseline interpreter usage patterns across users and departments, using aggregation functions to identify anomalous script execution that might indicate compromised accounts or insider threats.

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

1. Filters for common system administration and reconnaissance tools
2. `LOOKUP JOIN` enriches process data with user and asset context
3. `COUNT_DISTINCT` functions measure the breadth of tool usage across systems
4. `CASE` statement categorizes usage patterns for easier analysis
5 Groups by user and department to identify anomalous behavior patterns

## Step 6: Hunt for persistence mechanisms

This query showcases how `DATE_TRUNC` enables temporal analysis of persistence mechanisms, using time bucketing and `COUNT_DISTINCT` to identify suspicious patterns like rapid-fire task creation or persistence establishment across multiple time windows.

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

1. Uses match operator (`:`) to find scheduled task creation commands, providing more flexible matching than exact string comparison
2. Creates hourly time buckets with `DATE_TRUNC` to analyze temporal patterns in persistence activity
3. Measures temporal dispersion using `COUNT_DISTINCT` on time buckets to detect scheduled tasks created across multiple time periods
4. Creates meaningful categorization of persistence patterns using `CASE` to identify potentially malicious task scheduling sequences (burst creation vs spread across time)

## Additional resources

- Explore a curated collection of threat hunting [queries](https://github.com/elastic/detection-rules/tree/main/hunting) in the `elastic/detection-rules` GitHub repo.
  - The corresponding [blog](https://www.elastic.co/security-labs/elevate-your-threat-hunting) provides more information about how to use them in your threat hunting workflows.
- Explore more threat hunting examples in the following blogs:
  - https://www.elastic.co/blog/security-exfiltration
  - https://www.elastic.co/blog/detecting-command-scripting-interpreter
  - https://www.elastic.co/blog/elastic-security-detecting-credential-dumping
  - https://www.elastic.co/blog/elastic-security-detecting-covert-data-exfiltration
- Learn more about the [{{esql}}](elasticsearch://reference/query-languages/esql.md) language in the reference documentation.
