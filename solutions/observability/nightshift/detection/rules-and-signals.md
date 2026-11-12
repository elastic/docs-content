---
navigation_title: Rules and signals
applies_to:
  serverless:
    observability: preview
description: Check which rules detection runs on your logs, what each rule found, and how discovery judged it. Remove rules that only add noise.
products:
  - id: observability
  - id: cloud-serverless
---

# Rules and signals [nightshift-detection-rules-signals]

Rules and signals are the evidence behind every significant event. Check them to find out what detection watches in your logs, why it raised an event, and which rules only add noise.

- A **rule** is an {{esql}} query that looks for one failure pattern, such as database lock timeouts. It runs on a schedule and counts the matching log lines.
- A **signal** is a record that a rule's match count changed significantly, such as a sudden spike. Discovery reviews signals and groups the ones that point to the same problem into a significant event.

## Where rules come from [nightshift-detection-rules-origins]

{{nightshift}} writes rules for you from the query KIs that it learns from your sources. Refer to [How detection learns your system](./learning.md).

- **Generated automatically.** A query KI becomes a rule when it matches specific log lines and has a high severity score.
- **Promoted by you.** Other query KIs stay on the **Knowledge Indicators** tab. To turn one into a rule, open **Knowledge** > **Knowledge Indicators**, select the KI, and select **Promote**. Promote also brings back a rule that you deleted. Refer to [Knowledge Indicators](../context/knowledge-indicators.md).

Query KIs that compute statistics, such as an error count, can't become rules yet.

All rules run on a shared schedule, every few minutes. A rule match doesn't open an alert on its own.

## Review rules [nightshift-detection-rules-review]

To open the list, select the **Rules** tab on the **Detections** page.

% SCREENSHOT: The Rules tab on the Detections page, with the Rule matches over time chart and the rules table, filtered to the inventory-api entity.

The **Rule matches over time** chart shows how often your rules matched. The table lists every rule:

| Column | What it shows |
| --- | --- |
| **Title** | The name of the rule. |
| **Impact** | How serious a match of this rule is, such as **Critical**. |
| **Last activity** | The latest interval in which the rule matched. |
| **Status** | Whether the rule runs, such as **Active**. |
| **Matches** | How many log lines the rule matched in the selected time range. |

To find a rule, search by name, select entities in the **Entities** list, or change the time range. The default is **Last 24 hours**.

To work with a rule, open its {icon}`boxes_vertical` menu:

- **Open in Discover** shows the log lines that the rule matches.
- **Delete rule** removes it. To remove several rules, select them, then select **Delete selected**.

Delete a rule when it matches all the time without a real problem behind it. Its query KI stays, so you can promote it again later.

## Signals [nightshift-detection-signals]

Detection compares each rule's match counts over time. When the pattern changes significantly, it records a signal with the kind of change:

| Change | What it means |
| --- | --- |
| **Spike** | The count jumps up for a short time. |
| **Dip** | The count drops for a short time. |
| **Step change** | The count moves to another level and stays there. |
| **Trend change** | The count starts to rise or fall in a different direction. |
| **Distribution change** | The overall shape of the counts changes. |
| **Non-stationary** | The counts no longer follow a stable pattern. |

A signal on its own doesn't need any action from you. Discovery reviews it together with related signals and tests whether they point to a real problem.

### Check the signals behind an event [nightshift-detection-signals-event]

Every significant event lists its signals in the **Detections** section of its details. Select one to open it next to the event.

:::{image} ../../../images/nightshift-significant-event-details.png
:alt: A signal's details next to the significant event it belongs to. The signal shows a Non-stationary change, a Refuted verdict, a summary, a trend chart with the change marked, and its ES|QL query with Open in Discover
:screenshot:
:::

The signal shows:

- Badges for the kind of change, such as **Non-stationary**, and for the verdict.
- **Summary**: What discovery found when it checked the signal against your current data.
- **Trend**: The rule's match counts, with the change marked.
- **ES|QL query**: The rule's query. Select **Open in Discover** to run it yourself.

To ask questions about the signal, select **Open in chat**.

The verdict tells you how discovery judged the signal:

| Verdict | Meaning |
| --- | --- |
| **Confirmed** | Discovery found data that shows the failure. |
| **Refuted** | Discovery checked and found the system healthy for this rule. |
| **Inconclusive** | The check couldn't establish either way, for example because the query returned nothing or failed. |
| **Off topic** | The check found something that isn't related to the rule. |
| **Not checked** | No query was available to check the signal. |

An event can include refuted signals. Read them together with the event's confidence before you act.

### Browse all signals [nightshift-detection-signals-tab]

The **Signals** tab lists every signal, one per row. It appears only in [developer mode](../settings.md#nightshift-settings-developer-mode).

Each row shows the **Rule**, the **Source**, the **Timestamp**, the **Change**, and the **Discovery** state:

- **Pending**: Discovery hasn't reviewed the signal yet.
- **Processed**: Discovery reviewed it.
- **Skipped**: Discovery closed the signal without reviewing it again, because nothing had changed. Hover over the badge for the reason.

Use the **Change** filter to show only some kinds of change.

## Next steps [nightshift-detection-rules-signals-next]

- [Review significant events](./significant-events.md): Review the events that discovery raised from your signals.
- [Knowledge Indicators](../context/knowledge-indicators.md): Promote query KIs to rules, or exclude wrong KIs.
- [How Significant Events works](../significant-events/how-it-works.md): Read how rules run and how discovery works, for operators.
