The following known issues and limitations apply to {{cps-init}} in {{observability}} apps at technical preview. For an overview of {{observability}} app compatibility, refer to [{{cps-cap}} in {{observability}}](/solutions/observability/cross-project-search.md).

### Rules data scope inconsistency [obs-cps-rules-scope]

Custom Threshold and SLO Burn Rate rules query only local project data, even when the underlying data view (for example, `logs-*`) returns cross-project data in Discover. This means:

* A rule simulation may show a condition is violated, but the rule itself may not fire because it evaluates only local data.
* Discover and rules may show different results for the same data view.

APM-specific rules (APM anomaly, error count threshold, failed transaction rate threshold, latency threshold) and Infrastructure Inventory rules have not been fully validated with {{cps-init}}.

Tracking: [kibana#257714](https://github.com/elastic/kibana/issues/257714)

### SLO remote actions not available [obs-cps-slo-remote]

Remote SLOs appear in the SLO list with a "remote" badge, but edit, disable, and clone actions are not available for remote SLOs. Only local SLOs are manageable, even when connected to a remote project.

Tracking: [kibana#252955](https://github.com/elastic/kibana/issues/252955)

% DOCS NOTE — CONDITIONAL: Include the following "Discover flyout links" subsection only if APM/Infra CPS work (observability-dev#5328, observability-dev#5374) has NOT shipped. Remove it when that work lands.

### Discover flyout links for remote documents [obs-cps-discover-flyout]

The following Discover flyout links do not work correctly for documents from linked projects:

* Trace document flyout transaction name links ([kibana#256211](https://github.com/elastic/kibana/issues/256211))
* Span links from linked projects ([kibana#256190](https://github.com/elastic/kibana/issues/256190))
* "Explain this log entry" for linked project logs ([kibana#256168](https://github.com/elastic/kibana/issues/256168))
* Log flyout stream links ([kibana#256075](https://github.com/elastic/kibana/issues/256075))
* Trace flyout charts don't respect project selector ([kibana#256072](https://github.com/elastic/kibana/issues/256072))

These issues will be resolved when {{cps-init}} is enabled in APM and Infrastructure.

### Observability Overview alerts are local only [obs-cps-overview-alerts]

The Alerts section of the Observability Overview page shows alerts from the local project only, even when rules are configured to act on cross-project data. This is consistent with CCS behavior in {{ech}} — alerts are generated and stored locally.

### Logs Essentials projects cannot use {{cps-init}} [obs-cps-logs-essentials]

Logs Essentials projects cannot participate in {{cps-init}}.

### Synthetics is not affected by {{cps-init}} [obs-cps-synthetics]

Synthetics monitors and TLS Certificates are bound to saved objects and remain scoped to the local project. This is consistent with CCS behavior in {{ech}}. Monitors from linked projects do not appear in the Synthetics UI of the origin project.