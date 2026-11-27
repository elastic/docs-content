---
navigation_title: Route data
description: Add a router to a stream to send records to different destinations by condition, copy records to several destinations, and decide what happens to the rest.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Route data to different destinations

A router sends each record to a destination based on a list of rules. Put a router between a source and your destinations when one incoming stream needs to end up in more than one place. For example, you can split data by team, environment, or severity, archive a copy of selected records in Amazon S3 while indexing every record, or send one shipper's data to two {{es}} destinations. Routing runs in the Elastic-managed collectors, so the shipper sends everything to one endpoint and doesn't need to know how the data is divided.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

You create and edit routers on the Streams Map. Each routing rule has an optional condition, an action that moves or copies the matching data, the signals it accepts, and a target on the Map, which is the destination or pipeline the rule is connected to.

## How routing rules work [streams-route-rules]

A router is an ordered list of rules. A rule's condition decides whether it matches a record, its action decides whether the record continues to the rules below, and its signals decide which kinds of records it considers at all. Together, these settings decide how each record moves through the router:

* Rules are checked top to bottom, and a record goes to the first rule whose condition matches. Order matters, because a rule with a broad condition claims records before any narrower rule below it gets to see them.
* A **move rule** sends the record to its target and takes it out of the router. Later rules don't see the record. Move is the default.
* A **copy rule** sends a copy of the record to its target and lets the original continue to the rules below it. Order still applies, so a copy rule placed below a catch-all rule never matches anything. A copy rule needs a condition. The panel accepts a copy rule without one, but the save is rejected, because a rule without a condition has to be the last one.
* A move rule with no condition is the **catch-all rule**. It takes every record the rules above it didn't claim. A router can have only one, and it's always last.
* A record that matches no rule is dropped. The panel warns you when the router has no catch-all rule. To discard data on purpose, leave it unmatched, or drop it earlier with a [Filter](processors/filter.md) processor.
* A rule accepts only the signals selected for it. A record of a signal the rule doesn't accept skips to the next rule.
* A rule leads to a destination or to a pipeline. Sending a rule's data to a pipeline lets you process it differently from the rest. On the Map, you can draw one line from each rule, so a rule has one target.

## Add a router [streams-route-add]

To add a router, you need the **Admin** role.

1. On the Streams Map, hover over the connection where the data should be split, select the {icon}`plus_circle` plus icon that appears on it, then select **Add routing**. The connection must end at a destination, whether it starts at a source or a pipeline.

   The **Add routing** panel opens with one rule, titled **Default**. It has no condition, keeps the connection's existing destination, and stays at the bottom of the list. Give it a condition if you don't want a catch-all rule.
1. For each further rule you want, select **Add rule**. A **Creating route rule** form opens. Fill it in and select **Create** on the form:
   * **Condition**: an OTTL boolean expression, such as `resource.attributes["env"] == "prod"` or `attributes["service.name"] != "checkout"`. Leave it empty on a move rule to make it the catch-all rule, shown as **No condition, matches all remaining data**. A copy rule needs a condition: the panel accepts one without, shown as **No condition, copies all data**, but **Save changes** then fails. While no catch-all rule exists, the panel warns that **The conditions are not guaranteed to match all data. Unmatched data will be dropped.**, or names the signals affected when only some are uncovered. The warning disappears as soon as you add one. To learn how to refer to fields and write conditions, refer to [Fields and conditions](fields-and-conditions.md#streams-fields-conditions).
   * **Telemetry signals**: at least one of the signals the incoming data can send to this rule, from **Logs**, **Metrics**, **Traces**, **Docs**, and **Profiles**. **Docs** is the Documents signal from a Managed _bulk source. Only the signals that reach this connection are offered.
   * **What should the condition do with the data?**: **Route data exclusively** for a move rule, or **Create a copy of the data** for a copy rule.
1. Drag rules by their handle to reorder them. Rules are titled by position, **Rule 1**, **Rule 2**, and so on, so a rule that moves up takes the title of the one it replaces. A move rule with no condition is titled **Default** instead, has no drag handle, and stays below the rules with a condition. Delete a rule with its {icon}`trash` trash icon.
1. Select **Create**. The panel closes and a router node appears on the connection. The node has one row per rule, labeled by position as **rule 1**, **rule 2**, and so on, or **default** for the catch-all rule, with a **copy** badge on copy rules. Hover over a row to see the rule's condition, or **Otherwise** for the catch-all rule, together with its signals.
1. On the Map, drag from each new rule's handle to the destination, or the pipeline, that its records should go to. The **Default** rule is already connected. Each rule sends to one target, and two rules can send to the same destination.
1. Select **Save changes** to deploy the configuration.

Until you select **Save changes**, the router exists only on the Map. If you close the panel with changes you haven't applied, Streams asks **Discard routing changes?**. Select **Keep editing** to return to the panel, or **Discard changes** to drop them.

## Edit a router [streams-route-edit]

You can change the rules of an existing router at any time. Editing requires the same privilege as adding a router.

1. On the Streams Map, select the router node. The **Edit routing** panel opens with the rules listed in order, each showing its condition and signals.
1. Make your changes:
   * To change a rule, select its {icon}`pencil` pencil icon. The same form as for a new rule opens in the row. Select **Apply** on the form to keep the change, or **Cancel** to leave the rule as it was.
   * To add, reorder, or delete rules, proceed as when adding a router. A rule you added routes nowhere until you connect its handle on the Map.
1. Select **Apply** at the bottom of the panel.
1. Select **Save changes** to deploy the configuration.

If you delete every rule and select **Apply**, the router is removed, together with the connections that went through it.

Deleting a destination also changes the routers that lead to it. A rule whose only target was the deleted destination is deleted with it, condition included, and the change is saved immediately. Records that rule claimed fall through to the rules below it, and if the deleted rule was the **Default** rule, they're dropped. Before you delete a destination, open the routers connected to it and reconnect or remove the rules that lead to it. Refer to [Manage destinations](destinations.md#streams-destinations-manage).

A router whose rules differ by signal can't be edited in the panel. It opens read-only with the message **This routing uses telemetry-specific rule lists**. If the last save rejected a rule, the panel shows the rejection and the rule's condition is marked invalid.

## Example: Archive production errors in S3 and index everything [streams-route-example]

A common layout indexes every record and keeps a long-term copy of the ones that matter most. One OTLP source receives logs from every service, and a router on its connection has two rules:

* Rule 1 has the condition `resource.attributes["deployment.environment.name"] == "production" and severity_text == "ERROR"`. Its action is **Create a copy of the data**, and it's connected to an [Amazon S3 destination](destinations/s3.md). Production errors are copied to the bucket and then continue to the rule below.
* The **Default** rule has no condition. Its action is **Route data exclusively**, and it's connected to a Local Elasticsearch destination. Every record, including the production errors, is indexed there.

As a result, everything is indexed and production errors are also archived in S3. Both the action and the order matter:

* If rule 1 were a move rule, production errors would be archived but never indexed.
* If the catch-all rule came first, it would take every record and nothing would reach the copy rule. The panel prevents this by keeping the **Default** rule last.

To build this router, starting from a source connected to a Local Elasticsearch destination:

1. Hover over the connection, select the {icon}`plus_circle` plus icon, then select **Add routing**. The panel opens with the **Default** rule, which keeps its connection to the Local Elasticsearch destination.
1. Select **Add rule**. Enter the condition `resource.attributes["deployment.environment.name"] == "production" and severity_text == "ERROR"`, select **Create a copy of the data**, and select **Create** on the form. This is rule 1, and it sits above **Default**.
1. Select **Create**.
1. On the Streams Map, drag from the copy rule's handle to the S3 destination.
1. Select **Save changes**.

The panel shows no dropped-data warning for this router, because the **Default** rule catches every record the copy rule has already handled. On the Map, the copy rule's row is labeled **rule 1** with a **copy** badge, and the catch-all rule's row is labeled **default**. Hover over a row to see its condition, or **Otherwise** for the catch-all rule.

## Related pages [streams-route-related]

* [Work with the Streams Map](streams-map.md): Learn how to add nodes on connections, connect them, and save your changes.
* [Process data before it reaches Elasticsearch](process-data.md): Change or drop records before or after a router.
* [Fields and conditions](fields-and-conditions.md): Learn how to refer to fields in OTTL and write the conditions of routing rules.
* [Destinations](destinations.md): Learn what each destination type accepts and what happens to data it can't store.
* [Troubleshooting](troubleshooting.md#streams-troubleshoot-no-data): Find out what to check when data is accepted but never arrives.
* [Streams limitations](limitations.md#streams-limitations-routing): Check what routing can't do yet.
* [Streams glossary](glossary.md): Look up routing rule, move rule, copy rule, catch-all rule, and the other terms used on this page.
