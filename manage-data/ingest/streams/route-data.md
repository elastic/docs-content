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

A router sends each record to a destination based on a list of rules. Put a router between a source and your destinations when one incoming stream needs to end up in more than one place. For example, you can split data by team, environment, or severity, archive a full copy in Amazon S3 while indexing only part of it, or send one shipper's data to two {{es}} destinations. Routing runs in the Elastic-managed collectors, so the shipper sends everything to one endpoint and doesn't need to know how the data is divided.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

You create and edit routers on the Streams Map. Each routing rule has an optional condition, an action that moves or copies the matching data, the signals it accepts, and a target on the Map, which is the destination or pipeline the rule is connected to.

## How routing rules work [streams-route-rules]

A router is an ordered list of rules. A rule's condition decides whether it matches a record, its action decides whether the record continues to the rules below, and its signals decide which kinds of records it considers at all. Together, these settings decide how each record moves through the router:

* Rules are checked top to bottom, and a record goes to the first rule whose condition matches. Order matters, because a rule with a broad condition claims records before any narrower rule below it gets to see them.
* A **move rule** sends the record to its target and takes it out of the router. Later rules don't see the record. Move is the default.
* A **copy rule** sends a copy of the record to its target and lets the original continue to the rules below it. Order still applies, so a copy rule placed below a catch-all rule never matches anything.
* A rule with no condition is a **catch-all rule**. It takes every record the rules above it didn't claim.
* A record that matches no rule is dropped. The panel warns you when the router has no catch-all rule. To discard data on purpose, leave it unmatched, or drop it earlier with a [Filter](processors/filter.md) processor.
* A rule accepts only the signals selected for it. A record of a signal the rule doesn't accept skips to the next rule.
* A rule leads to a destination or to a pipeline. Sending a rule's data to a pipeline lets you process it differently from the rest.

## Add a router [streams-route-add]

To add a router, you need the **Admin** role.

1. On the Streams Map, hover over the connection where the data should be split, select the {icon}`plus_circle` plus icon that appears on it, then select **Add routing**. The connection must end at a destination, whether it starts at a source or a pipeline.

   The **Add routing** panel opens with one rule, titled **Default**. It has no condition, keeps the connection's existing destination, and stays at the bottom of the list. Give it a condition if you don't want a catch-all rule.
1. For each further rule you want, select **Add rule**. A **Creating route rule** form opens. Fill it in and select **Create** on the form:
   * **Condition**: an OTTL boolean expression, such as `resource.attributes["env"] == "prod"` or `attributes["service.name"] != "checkout"`. Leave it empty to make a catch-all rule, shown as **No condition, matches all remaining data** on a move rule and **No condition, copies all data** on a copy rule. While no catch-all rule exists for a signal, the panel warns that some data will be dropped; the warning disappears as soon as you add one.
   * **Telemetry signals**: at least one of the signals the incoming data can send to this rule, from **Logs**, **Metrics**, **Traces**, **Docs**, and **Profiles**. **Docs** is the Documents signal from a Managed _bulk source. Only the signals that reach this connection are offered.
   * **What should the condition do with the data?**: **Route data exclusively** for a move rule, or **Create a copy of the data** for a copy rule.
1. Drag rules by their handle to reorder them. Rules are titled by position, **Rule 1**, **Rule 2**, and so on, so a rule that moves up takes the title of the one it replaces. The router node on the Map labels the same rules by position too, but counting from zero, as `rule-0`, `rule-1`, and so on. A move rule with no condition is titled **Default** instead, has no drag handle, and stays below the rules with a condition. Delete a rule with its {icon}`trash` trash icon.
1. Select **Create**. The panel closes and a router node appears on the connection, with one handle per rule and a **copy** badge on copy rules.
1. On the Map, drag from each new rule's handle to the destination, or the pipeline, that its records should go to. The **Default** rule is already connected. Each rule sends to one target, and two rules can send to the same destination.
1. Select **Save changes** to deploy the configuration.

Until you select **Save changes**, the router exists only on the Map. If you close the panel with changes you haven't applied, you're prompted to discard them or keep editing.

## Edit a router [streams-route-edit]

You can change the rules of an existing router at any time. Editing requires the same privilege as adding a router.

1. On the Streams Map, select the router node. The **Edit routing** panel opens with the rules listed in order, each showing its condition and signals.
1. Make your changes:
   * To change a rule, select its {icon}`pencil` pencil icon. The same form as for a new rule opens in the row. Select **Apply** on the form to keep the change, or **Cancel** to leave the rule as it was.
   * To add, reorder, or delete rules, proceed as when adding a router. A rule you added routes nowhere until you connect its handle on the Map.
1. Select **Apply** at the bottom of the panel.
1. Select **Save changes** to deploy the configuration.

If you delete every rule and select **Apply**, the router is removed, together with the connections that went through it.

A router whose rules differ by signal can't be edited in the panel. It opens read-only with the message **This routing uses telemetry-specific rule lists**. If the last save rejected a rule, the panel shows the rejection and the rule's condition is marked invalid.

## Example: Copy everything to S3 and index only production logs [streams-route-example]

A common layout archives every record and indexes only the ones you search. One OTLP source receives logs from every service, and a router on its connection has two rules:

* Rule 1 has no condition, so it matches every record. Its action is **Create a copy of the data**, and it's connected to an [Amazon S3 destination](destinations/s3.md). Every record is copied to the bucket and then continues to rule 2.
* Rule 2 has the condition `resource.attributes["deployment.environment.name"] == "production"`. Its action is **Route data exclusively**, and it's connected to a Local Elasticsearch destination. Production records are indexed there. Records from other environments match nothing after rule 1 and are dropped.

As a result, everything is archived in S3 and only production logs are indexed. Both the action and the order matter:

* If rule 1 were a move rule, it would take every record and nothing would reach rule 2.
* If the two rules were swapped, production records would be indexed but never archived.

To build this router, starting from a source connected to a Local Elasticsearch destination:

1. Hover over the connection, select the {icon}`plus_circle` plus icon, then select **Add routing**.
1. Select the **Default** rule's {icon}`pencil` pencil icon, enter the condition `resource.attributes["deployment.environment.name"] == "production"`, and select **Apply** on the form. The rule keeps **Route data exclusively** and its connection to the Local Elasticsearch destination. This is rule 2.
1. Select **Add rule**. Leave the condition empty, select **Create a copy of the data**, and select **Create** on the form. This is rule 1.
1. Drag the new rule to the top, then select **Create**.
1. On the Streams Map, drag from the copy rule's handle to the S3 destination.
1. Select **Save changes**.

The panel shows no dropped-data warning for this router, because the copy rule has no condition and handles every record before it reaches rule 2. On the Map, the copy rule's row is labeled **Otherwise** with a **copy** badge, and rule 2's row shows its condition.

## Related pages [streams-route-related]

* [Work with the Streams Map](streams-map.md): Learn how to add nodes on connections, connect them, and save your changes.
* [Process data before it reaches Elasticsearch](process-data.md): Change or drop records before or after a router.
* [Destinations](destinations.md): Learn what each destination type accepts and what happens to data it can't store.
* [Troubleshooting](troubleshooting.md#streams-troubleshoot-no-data): Find out what to check when data is accepted but never arrives.
* [Streams limitations](limitations.md#streams-limitations-routing): Check what routing can't do yet.
* [Streams glossary](glossary.md): Look up routing rule, move rule, copy rule, catch-all rule, and the other terms used on this page.
