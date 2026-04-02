---

navigation_title: Triage Attack Discovery findings
description: Assess open Attack Discovery findings by evaluating alert diversity, rule frequency, and entity risk. Create cases for confirmed threats and acknowledge low-confidence findings.
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:

- id: security
- id: cloud-serverless

---

# Triage Attack Discovery findings [triage-attack-discovery-findings]

Learn how to systematically assess open Attack Discovery findings, determine which ones warrant a case, and process them. Following a repeatable triage workflow helps you focus on genuine threats, reduce alert fatigue, and lower your mean time to respond.

Each Attack Discovery finding groups related alerts into a single attack narrative. Rather than investigating each alert individually, you assess the attack as a unit—evaluating confidence based on alert diversity, detection rule quality, and entity risk context—then decide whether to create a case, investigate further, or acknowledge and move on.

:::{note}
An [agent skill](https://github.com/elastic/agent-skills-sandbox/tree/main/skills/security/attack-discovery-triage) exists specifically for automating this triage workflow. When loaded into a compatible AI agent, it retrieves open findings, scores confidence programmatically using the same methodology described on this page, and presents a triage summary for your approval before creating cases or acknowledging alerts.

**Advantages of the agent skill:**

- Processes findings in bulk rather than one at a time.
- Applies the confidence scoring heuristics consistently without manual lookups.
- Runs all enrichment queries (entity risk, rule frequency, alert context) automatically.

**Trade-offs to consider:**

- The skill requires the [agent-skills-sandbox](https://github.com/elastic/agent-skills-sandbox) repository, Node.js 18+, and API keys with appropriate permissions.
- Confidence scoring uses fixed heuristics. Manual triage lets you apply institutional knowledge that the skill can't account for, such as knowing that a specific host is a honeypot or that a particular rule was recently tuned.
- Write operations (case creation, alert acknowledgment) still require your explicit approval, but you have less granular control over how findings are enriched and summarized.

Refer to the [agent-skills-sandbox README](https://github.com/elastic/agent-skills-sandbox/blob/main/README.md) for setup instructions.
:::

## Before you begin [before-you-begin]

Before you start, make sure you have the following:

- Attack Discovery is [configured with an LLM connector](/solutions/security/ai/attack-discovery.md#attack-discovery-generate-discoveries).
- At least one finding has been generated, either [manually](/solutions/security/ai/attack-discovery.md#attack-discovery-generate-discoveries) or through a [schedule](/solutions/security/ai/attack-discovery.md#schedule-discoveries).
- Your role has the [required privileges](/solutions/security/ai/attack-discovery.md#attack-discovery-rbac) to view and modify Attack Discovery alerts.

:::{tip}
For richer triage context, enable [entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md). Entity risk scores help you assess whether the users and hosts in a discovery are already known to be high risk, which can strengthen your assessment. Entity analytics isn't required for triage, but it can improve decision quality.
:::

## Step 1: Review open findings [review-open-findings]

Start by retrieving all open findings and prioritizing them by risk score. This gives you a ranked list of potential attacks to work through, starting with the most critical.

:::::{tab-set}
::::{tab-item} UI
:sync: ui

1. Go to **Attack Discovery** from the {{elastic-sec}} navigation menu.
2. Use the **Status** filter to show only **Open** findings.
3. Sort by risk score (highest first) to prioritize the most critical findings.

For each finding, note the following key signals:

- **Risk score**: The overall severity assigned to the discovery.
- **Alert count**: How many underlying security alerts the discovery groups together.
- **MITRE ATT&CK tactics**: Which tactics the discovery maps to—more tactics suggest a broader attack.
- **Entities**: Which users and hosts are involved.

::::
::::{tab-item} ES|QL
:sync: esql

Run the following ES|QL query in [**Discover**](/explore-analyze/query-filter/languages/esql-kibana.md) to retrieve open findings from both scheduled and on-demand discovery indices. Replace `default` with your {{kib}} space ID if you're using a non-default space:

```esql
FROM .alerts-security.attack.discovery.alerts-default, .adhoc.alerts-security.attack.discovery.alerts-default METADATA _id
| WHERE kibana.alert.workflow_status == "open"
  AND @timestamp >= NOW() - 1 day
| KEEP @timestamp, _id,
       kibana.alert.attack_discovery.title_with_replacements,
       kibana.alert.attack_discovery.summary_markdown_with_replacements,
       kibana.alert.attack_discovery.mitre_attack_tactics,
       kibana.alert.attack_discovery.alert_ids,
       kibana.alert.attack_discovery.alerts_context_count,
       kibana.alert.risk_score
| SORT kibana.alert.risk_score DESC, @timestamp DESC
| LIMIT 50
```

If one index doesn't exist yet (for example, no scheduled discoveries have been generated), ES|QL returns an error. In that case, query each index separately and combine the results.

::::
::::{tab-item} API
:sync: api

Use the Attack Discovery Find API to retrieve open findings sorted by risk score:

```bash
GET /api/attack_discovery/_find?status=open&sort_field=risk_score&sort_order=desc&with_replacements=true&per_page=50
```

If you're using a non-default {{kib}} space, prefix the path with `/s/{space_id}`:

```bash
GET /s/my-space/api/attack_discovery/_find?status=open&sort_field=risk_score&sort_order=desc&with_replacements=true&per_page=50
```

::::
:::::

Before moving to Step 2, scan the results for duplicate findings. Overlapping schedule runs or repeated manual generations can produce similar discoveries covering the same alerts. Compare the `alert_ids` across findings—if two findings share most of their alerts, triage them together as one.

## Step 2: Assess finding confidence [assess-finding-confidence]

For each finding, evaluate three signals to determine whether it warrants a case, further investigation, or acknowledgment.

**Signal 1—Alert diversity**: How many alerts does the finding contain, and are they from different detection rules? A single alert from one rule provides minimal corroboration. Multiple alerts from distinct rules across different MITRE ATT&CK tactics provide strong corroboration.

**Signal 2—Rule frequency**: How often do the associated detection rules fire in your environment? Rules that rarely fire and affect few hosts carry more signal. Rules that fire dozens of times per week across many hosts are likely noisy and might need tuning.

**Signal 3—Entity risk** (if entity analytics is enabled): What are the risk scores and [asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md) levels for the involved users and hosts? A finding involving a critical-risk entity on a high-value asset deserves more attention than one involving an unknown entity with no prior activity.

Use these signals together to assign an overall confidence level:


| Confidence   | Signals                                                                                                                         | Recommended action                  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **High**     | Multiple alerts from diverse rules + low rule frequency + high entity risk                                                      | Create a case and investigate       |
| **Moderate** | Some corroboration but mixed signals (for example, diverse alerts but noisy rules, or low alert diversity but high entity risk) | Investigate further before deciding |
| **Low**      | Single alert or single rule + high rule frequency + low or unknown entity risk                                                  | Acknowledge and move on             |


:::{dropdown} Full confidence scoring matrix

The following tables provide a detailed scoring rubric for each signal. If you'd rather automate this process than score each finding manually, you can use the [Attack Discovery Triage agent skill](https://github.com/elastic/agent-skills-sandbox/tree/main/skills/security/attack-discovery-triage), which applies these heuristics programmatically and presents a triage summary for your approval.

#### Signal 1: Alert diversity [signal-alert-diversity]


| Alerts | Distinct rules | MITRE tactics | Score  |
| ------ | -------------- | ------------- | ------ |
| 1      | 1              | Any           | Low    |
| 2-3    | 1              | Any           | Low    |
| 2-3    | 2+             | Any           | Medium |
| 4+     | 2+             | 2+            | High   |
| 5+     | 3+             | 3+            | High   |


#### Signal 2: Rule frequency [signal-rule-frequency]

Assess how often the associated rules fire in your environment. Rules that fire frequently across many hosts are more likely to produce noise.


| Weekly fires | Hosts affected | Adjustment                                          |
| ------------ | -------------- | --------------------------------------------------- |
| Fewer than 5 | Fewer than 3   | Increases confidence (high-signal detection)        |
| 5-20         | 3-10           | Neutral                                             |
| 20-50        | 10+            | Decreases confidence (noisy detection)              |
| 50+          | Any            | Strongly decreases confidence (likely needs tuning) |


#### Signal 3: Entity risk [signal-entity-risk]

If [entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) is enabled, check the risk level and [asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md) for entities involved in the finding.


| Entity risk level          | Asset criticality      | Adjustment                      |
| -------------------------- | ---------------------- | ------------------------------- |
| Critical (greater than 90) | Extreme impact         | Strongly increases confidence   |
| Critical (greater than 90) | Any                    | Strongly increases confidence   |
| High (70-90)               | High or extreme impact | Increases confidence            |
| High (70-90)               | Low or medium impact   | Moderately increases confidence |
| Moderate (40-70)           | Any                    | Neutral                         |
| Low (20-40)                | Any                    | Decreases confidence            |
| Unknown (less than 20)     | Any                    | Neutral (no signal either way)  |


:::{tip}
On Stack 9.3+, the risk scoring engine includes privileged user status as an additional risk input. If a user entity in the finding has privileged status, treat this as equivalent to high-impact asset criticality.
:::

#### Overall confidence matrix [confidence-matrix]

Combine your three signal scores:


| Alert diversity | Rule frequency     | Entity risk        | Overall confidence |
| --------------- | ------------------ | ------------------ | ------------------ |
| High            | Increases          | Strongly increases | **High**           |
| High            | Neutral            | Increases          | **High**           |
| High            | Decreases          | Strongly increases | **High**           |
| Medium          | Increases          | Increases          | **High**           |
| Medium          | Neutral            | Neutral            | **Moderate**       |
| Medium          | Decreases          | Increases          | **Moderate**       |
| Low             | Increases          | Strongly increases | **Moderate**       |
| Low             | Neutral            | Neutral            | **Low**            |
| Low             | Decreases          | Any                | **Low**            |
| Any             | Strongly decreases | Any                | **Low**            |


:::

The following subsections explain how to gather each signal.

### Check entity risk context [check-entity-risk]

:::::{tab-set}
::::{tab-item} UI
:sync: ui

Click an entity's name in the finding to open the entity details flyout. Review the entity's risk score, asset criticality, and recent activity. Repeat for each user and host mentioned in the finding.

::::
::::{tab-item} ES|QL
:sync: esql

Query the risk score index for the entities mentioned in the discovery. Replace the entity names with the actual hostnames or usernames from the finding:

```esql
FROM risk-score.risk-score-latest-default
| WHERE host.name IN ("dc-prod-01", "ws-dev-12")
    OR user.name IN ("admin-jsmith", "svc-backup")
| KEEP host.name, user.name, host.risk.calculated_level, user.risk.calculated_level,
       host.risk.calculated_score_norm, user.risk.calculated_score_norm
```

::::
:::::

:::{tip}
If entity analytics isn't enabled, skip this signal and rely more heavily on alert diversity and rule frequency.
:::

### Review associated alerts and rules [review-alerts-rules]

:::::{tab-set}
::::{tab-item} UI
:sync: ui

Expand the finding to view its associated alerts. For each alert, note:

- The detection rule that generated it.
- The alert severity.
- Whether the same rule has fired on other hosts or users recently.

Use the **Status** filter on the **Alerts** page to check how often these rules fire in your environment.

::::
::::{tab-item} ES|QL
:sync: esql

Query the security alerts index using the alert IDs from the discovery. Replace the alert IDs with the actual values from the finding's `alert_ids` field:

```esql
FROM .alerts-security.alerts-default METADATA _id
| WHERE _id IN ("alert-id-1", "alert-id-2", "alert-id-3", "alert-id-4")
| KEEP @timestamp, _id, kibana.alert.rule.name, kibana.alert.severity,
       host.name, user.name, kibana.alert.rule.rule_id
| SORT @timestamp DESC
```

To assess rule frequency, check how often the associated rules have fired recently:

```esql
FROM .alerts-security.alerts-default
| WHERE kibana.alert.rule.name IN ("LSASS Memory Access", "Credential Dumping Detected")
  AND @timestamp >= NOW() - 7 days
| STATS alert_count = COUNT(*), host_count = COUNT_DISTINCT(host.name)
    BY kibana.alert.rule.name
```

::::
:::::

### Evaluate the attack narrative [evaluate-narrative]

Read the LLM-generated summary and details critically. Consider:

- Does the narrative make sense given the underlying alerts?
- Are the MITRE ATT&CK tactics plausible for the described attack chain?
- Are the entities and their described actions consistent with what you know about your environment?

:::{important}
Attack Discovery uses LLM-generated analysis. Treat each discovery as a hypothesis, not a confirmed incident. The narrative is valuable context, but it requires validation before you act on it.
:::

## Step 3: Take action on findings [take-action]

After assessing confidence for your open findings, take the appropriate action for each one.

### Create cases for high-confidence findings [create-cases]

For findings you've assessed as high confidence:

1. Click **Take action**, then select **Add to new case** or **Add to existing case**.
2. Include the discovery's summary and associated alerts in the case description. The LLM-generated narrative provides valuable context for analysts who pick up the case.
3. Set an appropriate severity on the case based on the finding's risk score and your confidence assessment.

For more on case management, refer to [Cases](/solutions/security/investigate/security-cases.md).

:::{note}
Before creating a case, check whether an existing case already covers the same alerts. Overlapping discoveries can lead to duplicate cases if you don't verify first.
:::

### Investigate moderate-confidence findings [investigate-uncertain]

For findings where you need more context before deciding:

- Click **Investigate in timeline** to explore the discovery's alerts in [Timeline](/solutions/security/investigate/timeline.md). This lets you view process trees, network connections, and file events associated with the alerts.
- Click **View in AI Assistant** or **Add to chat** to ask follow-up questions about the finding. For example, ask the assistant to explain the relationship between the alerts or suggest next investigation steps.

After investigating, either create a case (if the finding is confirmed) or acknowledge it (if it turns out to be benign).

### Acknowledge or close remaining findings [acknowledge-findings]

For findings that don't warrant further action:

:::::{tab-set}
::::{tab-item} UI
:sync: ui

- **Individual findings**: Click **Take action**, then select **Mark as acknowledged** or **Mark as closed**.
- **Bulk actions**: Select the checkboxes next to multiple findings, click **Selected *x* Attack discoveries**, and choose the status change.

When you change a finding's status, you can choose to change the status of only the discovery, or of both the discovery and its associated alerts.

::::
::::{tab-item} API
:sync: api

Use the bulk API to update the status of multiple findings at once. Replace the discovery IDs with the actual `_id` values from Step 1:

```bash
POST /api/attack_discovery/_bulk
{
  "ids": ["discovery-id-1", "discovery-id-2", "discovery-id-3"],
  "action": {
    "workflow_status": "acknowledged"
  }
}
```

::::
:::::

:::{tip}
Don't create cases for low-confidence findings. Creating cases for noise degrades trust in Attack Discovery and wastes analyst time on false leads.
:::

## Next steps [next-steps]

- [Schedule discoveries](/solutions/security/ai/attack-discovery.md#schedule-discoveries) for continuous coverage without manual generation.
- Set up [entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) for richer triage context.
- Learn about [case management workflows](/solutions/security/investigate/security-cases.md) to standardize how your team tracks confirmed threats.
- Use [AI Assistant](/solutions/security/ai/ai-assistant.md) for follow-up investigation and deeper analysis of individual findings.

