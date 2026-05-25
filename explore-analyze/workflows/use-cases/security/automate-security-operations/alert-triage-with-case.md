---
navigation_title: Triage alerts into cases
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build a workflow that triages a detection alert by enriching it, opening a case with the alert and observables attached, isolating the host, and notifying the on-call analyst.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Triage a security alert into a case [workflows-alert-triage-with-case]

This guide walks through building a workflow that turns a raw security alert into a triaged case. The workflow fires when a detection rule matches, enriches the alert with threat intel, opens a case with the alert and its indicators attached, isolates the affected host, and notifies the on-call analyst in Slack.

The workflow is adapted from [`traditional-triage.yaml`](https://github.com/elastic/workflows/blob/main/workflows/security/response/traditional-triage.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first for a walkthrough of the YAML editor and how to run a workflow.

## Before you begin [workflows-alert-triage-with-case-prereqs]

- **Permissions.** `All` privileges for **Analytics > Workflows**, plus `All` on **Security > Cases** in the target space. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **Detection rule.** An enabled [detection rule](/solutions/security/detect-and-alert/using-the-rule-ui.md) that generates the kind of alert you want to triage. For this workflow, the rule should produce alerts with `file.hash.sha256`, `host.name`, and `elastic.agent.id` populated.
- **Attach the workflow to the rule.** After you save the workflow, attach it to the detection rule so the rule invokes the workflow when it fires. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).
- **Connectors.** A configured VirusTotal connector for the hash lookup, and a Slack [connector](/deploy-manage/manage-connectors.md) for the notification. Note the connector IDs. You'll paste them into the workflow.
- **Host isolation capability.** The affected host must run {{elastic-defend}} for the isolation step to succeed.

## How it works [workflows-alert-triage-with-case-how-it-works]

The workflow runs in a single pass when an alert arrives:

1. An **alert trigger** fires when the detection rule matches.
2. A **VirusTotal lookup** enriches the alert with a reputation score.
3. An **`if` step** branches on the reputation score. If the file is confirmed malicious, the workflow opens a case, attaches the alert and observables, isolates the host, and notifies Slack. Otherwise, it closes the alert as a false positive.

## Build the workflow [workflows-alert-triage-with-case-build]

:::::{stepper}

::::{step} Configure the alert trigger

The workflow fires every time the attached detection rule generates an alert. Inside the workflow, the alert payload is available as `event.alerts[0]`.

```yaml
triggers:
  - type: alert
```

After you save the workflow, open the detection rule's **Actions** tab and attach this workflow so the rule invokes it.
::::

::::{step} Enrich the alert with threat intel

Call the VirusTotal connector to score the file hash. Wrap the call in `retry + continue` so a transient VirusTotal outage doesn't fail the whole workflow.

```yaml
- name: lookup_reputation
  type: virustotal.scanFileHash
  connector-id: "my-virustotal"
  on-failure:
    retry:
      max-attempts: 3
      delay: "5s"
      strategy: exponential
      max-delay: "30s"
    continue: true
  with:
    hash: "{{ event.alerts[0].file.hash.sha256 }}"
```

The output lives at `steps.lookup_reputation.output`. Use `steps.lookup_reputation.output.stats.malicious` to decide what to do next.
::::

::::{step} Branch on the reputation result

Most of the workflow only runs when the file is confirmed malicious. Wrap the `case`, `isolation`, and `notification` steps in an `if` step:

```yaml
- name: handle_malicious_file
  type: if
  condition: "steps.lookup_reputation.output.stats.malicious > 10"
  steps:
    # Case creation, host isolation, and Slack notification go here.
  else:
    - name: close_false_positive
      type: kibana.SetAlertsStatus
      with:
        status: closed
        reason: false_positive
        signal_ids:
          - "{{ event.alerts[0]._id }}"
```

The `else` branch closes the alert as a false positive using [`kibana.SetAlertsStatus`](/explore-analyze/workflows/steps/kibana.md#kibana-setalertsstatus).
::::

::::{step} Open a case with the alert context

Inside the `if` branch, create the case with `cases.createCase`. Fill the title and description from the alert payload:

```yaml
- name: create_case
  type: cases.createCase
  with:
    title: "Malware detected: {{ event.alerts[0].file.hash.sha256 }}"
    description: |
      Auto-created from detection rule `{{ event.rule.name }}`.

      VirusTotal malicious engines: {{ steps.lookup_reputation.output.stats.malicious | default: "n/a" }}
    owner: "securitySolution"
    severity: "high"
    tags: ["auto-triage", "malware"]
```

`title`, `description`, and `owner` are required. `owner` must be one of `securitySolution`, `observability`, or `cases`.
::::

::::{step} Attach the alert and observables to the case

Link the alert that triggered the workflow with `cases.addAlerts`, then attach the file hash and source IP as observables with `cases.addObservables`:

```yaml
- name: attach_alert
  type: cases.addAlerts
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    alerts:
      - alertId: "{{ event.alerts[0]._id }}"
        index: "{{ event.alerts[0]._index }}"
        rule:
          id: "{{ event.rule.id }}"
          name: "{{ event.rule.name }}"

- name: attach_observables
  type: cases.addObservables
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    observables:
      - typeKey: "observable-type-file-hash"
        value: "{{ event.alerts[0].file.hash.sha256 }}"
      - typeKey: "observable-type-ipv4"
        value: "{{ event.alerts[0].source.ip }}"
        description: "Source of the malicious activity"
```

Observable `typeKey` values must match the built-in observable types. Refer to [`cases.addObservables`](/explore-analyze/workflows/steps/cases.md#cases-addobservables) for the full list.
::::

::::{step} Isolate the affected host

Call the endpoint isolation API with `kibana.request`. Link the isolation action to the case and alert so the audit trail is complete:

```yaml
- name: isolate_host
  type: kibana.request
  with:
    method: POST
    path: /api/endpoint/action/isolate
    body:
      endpoint_ids:
        - "{{ event.alerts[0].elastic.agent.id }}"
      comment: "Automated isolation: case {{ steps.create_case.output.case.id }}"
      case_ids:
        - "{{ steps.create_case.output.case.id }}"
      alert_ids:
        - "{{ event.alerts[0]._id }}"
```
::::

::::{step} Notify the on-call analyst

Post a rich message to the SOC Slack channel with links to the case and the VirusTotal report. Use the `{{kibanaUrl}}` context variable for the case deep link:

```yaml
- name: notify_slack
  type: http
  with:
    url: https://slack.com/api/chat.postMessage
    method: POST
    headers:
      Content-Type: application/json; charset=utf-8
      Authorization: "Bearer {{ consts.slack_token }}"
    body:
      channel: "#soc-oncall"
      text: "Malware detected on {{ event.alerts[0].host.name }}"
      blocks: >-
        [{"type":"section","text":{"type":"mrkdwn","text":"*Malicious file on {{ event.alerts[0].host.name }}*\nHash: `{{ event.alerts[0].file.hash.sha256 }}`\nMalicious engines: {{ steps.lookup_reputation.output.stats.malicious }}"}},
         {"type":"actions","elements":[{"type":"button","text":{"type":"plain_text","text":"View case"},"url":"{{ kibanaUrl }}/app/security/cases/{{ steps.create_case.output.case.id }}"}]}]
    timeout: 30s
```

Store the Slack bot token in a `consts` block so you can swap environments without editing step bodies.
::::

:::::

## Complete workflow [workflows-alert-triage-with-case-complete]

:::{dropdown} Full workflow YAML

```yaml
name: security--triage-alert
description: Auto-triage a detection alert. Enrich with VirusTotal, open a case, attach observables, isolate the host, and notify Slack.
enabled: true

triggers:
  - type: alert

consts:
  slack_token: "YOUR-SLACK-BOT-TOKEN"

settings:
  concurrency:
    key: "{{ event.alerts[0].host.name }}"
    strategy: drop
    max: 1

steps:
  - name: lookup_reputation
    type: virustotal.scanFileHash
    connector-id: "my-virustotal"
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"
        strategy: exponential
        max-delay: "30s"
      continue: true
    with:
      hash: "{{ event.alerts[0].file.hash.sha256 }}"

  - name: handle_malicious_file
    type: if
    condition: "steps.lookup_reputation.output.stats.malicious > 10"
    steps:
      - name: create_case
        type: cases.createCase
        with:
          title: "Malware detected: {{ event.alerts[0].file.hash.sha256 }}"
          description: |
            Auto-created from detection rule `{{ event.rule.name }}`.

            VirusTotal malicious engines: {{ steps.lookup_reputation.output.stats.malicious | default: "n/a" }}
          owner: "securitySolution"
          severity: "high"
          tags: ["auto-triage", "malware"]

      - name: attach_alert
        type: cases.addAlerts
        with:
          case_id: "{{ steps.create_case.output.case.id }}"
          alerts:
            - alertId: "{{ event.alerts[0]._id }}"
              index: "{{ event.alerts[0]._index }}"
              rule:
                id: "{{ event.rule.id }}"
                name: "{{ event.rule.name }}"

      - name: attach_observables
        type: cases.addObservables
        with:
          case_id: "{{ steps.create_case.output.case.id }}"
          observables:
            - typeKey: "observable-type-file-hash"
              value: "{{ event.alerts[0].file.hash.sha256 }}"
            - typeKey: "observable-type-ipv4"
              value: "{{ event.alerts[0].source.ip }}"
              description: "Source of the malicious activity"

      - name: isolate_host
        type: kibana.request
        with:
          method: POST
          path: /api/endpoint/action/isolate
          body:
            endpoint_ids:
              - "{{ event.alerts[0].elastic.agent.id }}"
            comment: "Automated isolation: case {{ steps.create_case.output.case.id }}"
            case_ids:
              - "{{ steps.create_case.output.case.id }}"
            alert_ids:
              - "{{ event.alerts[0]._id }}"

      - name: notify_slack
        type: http
        with:
          url: https://slack.com/api/chat.postMessage
          method: POST
          headers:
            Content-Type: application/json; charset=utf-8
            Authorization: "Bearer {{ consts.slack_token }}"
          body:
            channel: "#soc-oncall"
            text: "Malware detected on {{ event.alerts[0].host.name }}"
          timeout: 30s
    else:
      - name: close_false_positive
        type: kibana.SetAlertsStatus
        with:
          status: closed
          reason: false_positive
          signal_ids:
            - "{{ event.alerts[0]._id }}"
```

:::

## Extend this workflow [workflows-alert-triage-with-case-extend]

- **Add historical context.** Before opening the case, run an [`elasticsearch.esql.query`](/explore-analyze/workflows/steps/elasticsearch.md) to count how many times the hash appears across your logs. Attach the count to the case with [`cases.addComment`](/explore-analyze/workflows/steps/cases.md#cases-addcomment).
- **Route by severity.** Replace the single `if` branch with a [`switch` step](/explore-analyze/workflows/steps/switch.md) that opens cases of different severities based on the malicious-engine count.
- **Enrich with an AI summary.** Add an [`ai.summarize` step](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) after `attach_observables` to produce a triage summary, then append it to the case with `cases.addComment`.
- **Assign the case.** Query your on-call schedule and use [`cases.assignCase`](/explore-analyze/workflows/steps/cases.md#cases-assigncase) to assign the case to the current on-call analyst.

## Related pages [workflows-alert-triage-with-case-related]

- [Automate security operations](/explore-analyze/workflows/use-cases/security/automate-security-operations.md): The outcomes this workflow supports.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Reference for every `cases.*` step.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): How retry, fallback, and continue work together.
- [`elastic/workflows` library](https://github.com/elastic/workflows): More security workflow examples.
