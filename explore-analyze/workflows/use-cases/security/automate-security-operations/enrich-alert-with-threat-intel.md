---
navigation_title: Enrich with threat intel
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build a small enrichment workflow that calls a threat intelligence API from an alert or on demand, and displays the reputation result for analysts or follow-up steps.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Enrich an alert with threat intelligence [workflows-enrich-alert-with-threat-intel]

This guide walks through building a focused enrichment workflow. The workflow calls a threat intelligence API (VirusTotal) with a hash or indicator, optionally runs additional enrichment providers, and formats the result. It's a small, useful pattern on its own, and a building block you can drop into larger automations like [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md).

The workflow is adapted from [`send-hash-to-virustotal.yaml`](https://github.com/elastic/workflows/blob/main/workflows/security/enrichment/send-hash-to-virustotal.yaml) and [`ip-reputation-check.yaml`](https://github.com/elastic/workflows/blob/main/workflows/security/enrichment/ip-reputation-check.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first.

## Before you begin [workflows-enrich-alert-prereqs]

- **Permissions.** `All` on **Analytics > Workflows**. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **Threat intel API key.** A VirusTotal, AbuseIPDB, or similar API key. Store keys in the workflow's `consts` block so you can swap environments without touching step bodies.
- **Optional: an alert-triggered parent workflow.** If you want the enrichment to run automatically when an alert fires, attach it to a detection rule. This guide uses a manual trigger so you can test the workflow in isolation first.

## How it works [workflows-enrich-alert-how-it-works]

The workflow runs on demand, takes the indicator you want to enrich as an `input`, calls one or more threat intel APIs, and logs the combined result:

1. **Manual trigger** with a `hash` or `ip_address` input.
2. **`http` step** calls the primary threat intel API (VirusTotal for hashes, AbuseIPDB for IPs). Retry transient errors and continue on failure so a single outage doesn't kill the workflow.
3. Optional **`http` step** adds geolocation or secondary scoring.
4. **`console` step** formats a human-readable summary with a risk assessment.

## Build the workflow [workflows-enrich-alert-build]

:::::{stepper}

::::{step} Declare the input and constants

Inputs let you run the workflow against any indicator without editing YAML. Constants hold the API key and base URL:

```yaml
inputs:
  - name: hash
    type: string
    description: SHA256 file hash to look up.
    required: true

consts:
  vt_api_key: "YOUR-VIRUSTOTAL-API-KEY"
  vt_base_url: "https://www.virustotal.com/api/v3"

triggers:
  - type: manual
```

When you run the workflow from the YAML editor, {{kib}} prompts you for the `hash` input.
::::

::::{step} Call VirusTotal with retry and continue

The `http` step queries the VirusTotal file-lookup endpoint. `on-failure.retry` backs off on transient failures, and `continue: true` lets downstream formatting still run if VirusTotal is unreachable:

```yaml
steps:
  - name: lookup_hash
    type: http
    with:
      url: "{{ consts.vt_base_url }}/files/{{ inputs.hash }}"
      method: GET
      headers:
        x-apikey: "{{ consts.vt_api_key }}"
        Accept: application/json
      timeout: 30s
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"
        strategy: exponential
        max-delay: "30s"
      continue: true
```

The response body lands at `steps.lookup_hash.output.data`. The relevant fields are `attributes.last_analysis_stats.malicious`, `attributes.last_analysis_stats.suspicious`, and `attributes.names`.
::::

::::{step} Format and log the result

Use a `console` step with Liquid conditionals to produce a short, human-readable report. Console output appears in the workflow execution log, so this step is useful whether the workflow is being run manually or composed into a larger automation:

```yaml
  - name: format_report
    type: console
    with:
      message: |
        === Threat Intel Report ===
        Hash: {{ inputs.hash }}

        Malicious engines: {{ steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious | default: "n/a" }}
        Suspicious engines: {{ steps.lookup_hash.output.data.data.attributes.last_analysis_stats.suspicious | default: "n/a" }}
        Known filenames: {{ steps.lookup_hash.output.data.data.attributes.names | join: ", " | default: "n/a" }}

        Assessment:
        {% if steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious > 10 %}
        HIGH RISK: more than 10 engines flag this hash as malicious.
        {% elsif steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious > 0 %}
        MEDIUM RISK: at least one engine flagged this hash.
        {% else %}
        LOW RISK: no engines flagged this hash.
        {% endif %}
```
::::

:::::

## Complete workflow [workflows-enrich-alert-complete]

:::{dropdown} Full workflow YAML

```yaml
name: enrich--hash-with-virustotal
description: Enrich a file hash with VirusTotal reputation data and print a short report.
enabled: true
tags: ["enrichment", "threat-intel"]

inputs:
  - name: hash
    type: string
    description: SHA256 file hash to look up.
    required: true

consts:
  vt_api_key: "YOUR-VIRUSTOTAL-API-KEY"
  vt_base_url: "https://www.virustotal.com/api/v3"

triggers:
  - type: manual

steps:
  - name: lookup_hash
    type: http
    with:
      url: "{{ consts.vt_base_url }}/files/{{ inputs.hash }}"
      method: GET
      headers:
        x-apikey: "{{ consts.vt_api_key }}"
        Accept: application/json
      timeout: 30s
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"
        strategy: exponential
        max-delay: "30s"
      continue: true

  - name: format_report
    type: console
    with:
      message: |
        === Threat Intel Report ===
        Hash: {{ inputs.hash }}

        Malicious engines: {{ steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious | default: "n/a" }}
        Suspicious engines: {{ steps.lookup_hash.output.data.data.attributes.last_analysis_stats.suspicious | default: "n/a" }}
        Known filenames: {{ steps.lookup_hash.output.data.data.attributes.names | join: ", " | default: "n/a" }}

        Assessment:
        {% if steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious > 10 %}
        HIGH RISK: more than 10 engines flag this hash as malicious.
        {% elsif steps.lookup_hash.output.data.data.attributes.last_analysis_stats.malicious > 0 %}
        MEDIUM RISK: at least one engine flagged this hash.
        {% else %}
        LOW RISK: no engines flagged this hash.
        {% endif %}
```

:::

## Extend this workflow [workflows-enrich-alert-extend]

- **Trigger from an alert instead of manually.** Replace the `manual` trigger with an [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) and read the hash from `event.alerts[0].file.hash.sha256`.
- **Add a second enrichment provider.** Chain an additional `http` step against AbuseIPDB or a private intel feed. The `ip-reputation-check.yaml` source workflow shows the two-provider pattern.
- **Store the enrichment for later.** Write the result to an index with [`elasticsearch.request`](/explore-analyze/workflows/steps/elasticsearch.md) so dashboards and subsequent workflows can query it.
- **Compose into triage.** Extract these steps into a [child workflow](/explore-analyze/workflows/steps/composition.md) named `shared--enrich-hash` and call it from your triage workflow with `workflow.execute`.
- **Decide on next actions.** Branch on the `malicious` count with an [`if` step](/explore-analyze/workflows/steps/if.md) to open a case, post to Slack, or stop early when the hash is clean.

## Related pages [workflows-enrich-alert-related]

- [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md): Pair enrichment with case creation for full triage.
- [HTTP step](/explore-analyze/workflows/steps/external-systems-apps.md#http-actions): Full `http` step reference.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Retry, fallback, and continue strategies in more depth.
- [Indicators of compromise](/solutions/security/investigate/indicators-of-compromise.md): The product surface where investigators triage threat-intel indicators interactively.
- [`elastic/workflows` enrichment folder](https://github.com/elastic/workflows/tree/main/workflows/security/enrichment): More enrichment examples.
