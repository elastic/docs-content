| {{observability}} app | CCS in {{ech}} | {{cps-init}} in {{serverless-short}} |
| --- | --- | --- |
| **APM** (Service Inventory, Traces, Dependencies) | Yes — configured via APM index settings using `remote:index` | Not available |
| **Infrastructure** (Inventory, Hosts) | Yes — configured via Infrastructure index settings using `remote:index` | Not available |
| **Observability Overview** (Hosts, Log Events, Service Inventory) | Yes | Not available |
| **Observability AI Assistant** | Yes | Not available |
| **SLOs** | Yes — SLOs target data views, which can include remote indices | Not available |
| **Rules** (Custom Threshold, SLO Burn Rate) | Yes — for rules based on data views | Read-only |
| **Synthetics** (monitors, TLS Certificates) | No | Not available |
| **Streams** | No | Not available |

% DOCS NOTE — CONDITIONAL: If APM/Infra CPS enablement (observability-dev#5328, observability-dev#5374) ships before tech preview goes GA, update the APM and Infrastructure rows: CPS column to "Yes (scope selector editable)" and confirm cross-project data behavior.
