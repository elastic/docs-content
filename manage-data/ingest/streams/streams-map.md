---
navigation_title: Streams Map
description: Learn how to read the Streams Map, connect sources, pipelines, routers, and destinations, save your changes, and move around with the mouse or keyboard.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Work with the Streams Map

The Streams Map is where you build streams. Each source, pipeline, router, and destination in your project is a node, and the connections between them show where data goes. You can follow the path a record takes from a shipper to {{es}} or Amazon S3, and change it in place.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

To open the Streams Map, find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab. The **Sources** and **Destinations** tabs next to it are where you can manage the Streams [sources](sources.md#streams-sources-manage) and [destinations](destinations.md#streams-destinations-manage). These three tabs carry a {icon}`flask` **Technical preview** badge. A fourth tab, **Classic Streams**, lists the data streams you manage after data reaches {{es}} and appears only when the project has some. Refer to [Streams Map and classic streams compared](index.md#streams-map-and-classic).

## Read the Map [streams-map-read]

Data flows from left to right. Each kind of node has its own shape and shows what you need to tell it apart:

| Node | What it shows |
| --- | --- |
| Source | Its name, its type (**OTLP endpoint**, **Prometheus Remote Write**, or **Managed _bulk**), the signals it accepts, and whether data is arriving: **Live** with the rate of accepted records, or **Waiting for data...**. |
| Pipeline | A {icon}`processor` processor icon and, once data flows, the rate of records passing through it and the average time a record spends in it. Select it to open the **Processing** panel. |
| Router | One row per routing rule, labeled by position as `rule-0`, `rule-1`, and so on, with a **copy** badge on copy rules. Rules can't be named, and the **Edit routing** panel titles the same rules **Rule 1**, **Rule 2**, and so on, counting from one. Select the node to open the panel. Hover over a row to see the signals the rule accepts and one of the following:<br><br>• **Condition**, followed by the rule's condition.<br>• **All data**, for a rule with no condition when it's the only rule.<br>• **Otherwise**, for a rule with no condition when the router has other rules, wherever the rule sits. |
| Destination | Its name, the signals it accepts, and a line that says where it writes. A Local Elasticsearch destination also shows how many indices and data streams in the project match its write patterns. Select it to open its details. |

The line under a destination's name is one of the following, in this order of priority:

* **No source**, when nothing is connected to the destination.
* The description, if you gave the destination one.
* Where it writes:
  * For a Local Elasticsearch destination, **Auto** in Auto index mode, or the index name or the count (such as **3 fixed indices**) in Fixed index mode.
  * For a Remote Elasticsearch destination, the host of the endpoint.
  * For an Amazon S3 destination, the bucket.

Source nodes and Local Elasticsearch destination nodes also show whether data is arriving:

* A source shows **Live** with the rate of records it accepted, for example `0.27/s`, or **Waiting for data...** when it accepted none in the last 15 minutes. Records the source refused don't count, so a source that gets only rejected requests keeps waiting.
* A Local Elasticsearch destination shows the rate of records that reached it and, after a divider, the average time a write took, for example `12/s` and `35ms`. The rate includes records that {{es}} rejected, so confirm in **Discover** that the data is indexed. **Data not flowing in** means no records reached it in the last 15 minutes. On a new destination, that's expected until the first record is written. On an established one, it's the first sign that a source stopped sending.

Router nodes, Remote Elasticsearch destinations, and Amazon S3 destinations don't show a state. If the statistics on a node couldn't be refreshed, a warning icon appears next to them with the message **Could not refresh. Showing the last known values.** For what the numbers mean and how often they refresh, refer to [Monitor streams](monitor-streams.md).

Hover over a connection to highlight it. The {icon}`plus_circle` plus icon that appears on it is how you add processing or routing to that part of the stream.

## Edit the Map [streams-map-edit]

To change anything on the Streams Map, you need the **Admin** role. Refer to [Privileges and API keys](security.md#streams-security-view-edit).

You build a stream by creating nodes and connecting them. Everything happens on the Map:

* **Create a source or destination**: Select **Source** or **Destination** in the toolbar at the bottom of the Map and fill in the dialog. The new node appears on the Map and is saved right away. Refer to [Sources](sources.md) and [Destinations](destinations.md). On an empty Map, **Add source** opens the same dialog as **Source** in the toolbar.
* **Connect nodes**: Drag from the handle on the right edge of a source, pipeline, or routing rule to the handle on the left edge of a pipeline, router, or destination. While you drag, every handle that can receive the connection is highlighted. A source or a routing rule has one outgoing connection.
* **Move or remove a connection**: Drag the end of a connection to another node to move it, or drop it on the empty background to remove it.
* **Add processing or routing on a connection**: Hover over the connection, select the {icon}`plus_circle` plus icon that appears on it, then select **Add processing** or **Add routing**. The new node sits on that connection. Routing can only be added to a connection that ends at a destination. Refer to [Process data](process-data.md) and [Route data](route-data.md).
* **Open a node**: Select it. A source opens its details, a pipeline opens the **Processing** panel, and a router opens the **Edit routing** panel. A destination opens a panel with its configuration or, for a Local Elasticsearch destination, the indices that match its write patterns and a **Documents** chart. Select an index name there to open the index's read-only **Overview** and **Retention** tabs. Refer to [Open a destination from the Map](destinations.md#streams-destinations-open).
* **Delete a source or destination**: Select the node and press {kbd}`del` or {kbd}`backspace`. The node disappears, but the deletion is saved only when you select **Save changes**, and **Undo** brings it back until then. To delete right away instead, open the node and select **Delete source** or **Delete destination** at the bottom of its panel, then confirm. That deletion is saved immediately, like deleting from the **Sources** or **Destinations** tab.
* **Delete a pipeline or router**: A pipeline disappears when you delete all of its processors in the **Processing** panel and select **Save and apply**. A router disappears when you delete all of its rules in the **Edit routing** panel and select **Apply**, then **Save changes**.
* **Undo** and **Redo**: Step back and forward through your edits with the toolbar buttons or the [keyboard shortcuts](#streams-map-keyboard).

Connections, routers, and nodes you delete with the keyboard exist only in your browser until you select **Save changes** at the top of the Map. Before saving, the Map checks the configuration. For example, a pipeline that doesn't lead to a destination blocks the save until you connect it or delete its processors. On success, a message confirms the save and the Elastic-managed collectors pick up the new configuration. Everyone with the **All** privilege edits the same configuration, and the last save overwrites earlier ones, so coordinate edits with your team.

Two kinds of change save on their own and don't need **Save changes**. A source is saved when you select **Continue** in its dialog and a destination when you select **Create destination**, and processors are saved when you select **Save and apply** in the **Processing** panel.

## Move around the Map [streams-map-move]

The Map has the usual controls for finding your way around a large graph:

* **Pan and zoom**: Scroll or drag the background to pan. Pinch to zoom, or use **Zoom in**, **Zoom out**, and **Fit to screen** in the bottom-left corner.
* **Minimap**: The overview in the bottom-right corner shows where you are. Select a spot on it to go there, or select **Hide minimap** to collapse it.
* **Search**: Type in the search field above the Map to show only the nodes whose name, type, index, bucket, or endpoint matches, together with everything connected to them. The Map zooms to fit the result. If nothing matches, it says **No streams match your search**. Clear the field to see the whole Map again. This is the quickest way to look at one stream on its own.
* **Select several nodes**: Hold Shift and select each node, or hold Shift and drag a box around them.
* **Tidy up**: Right-click the background and select **Tidy up** to lay out the whole Map, or select several nodes first, right-click them, and select **Tidy up selection**. Positions you drag nodes to aren't kept when you reload the page.

### Keyboard shortcuts [streams-map-keyboard]

You can work on the Map without a mouse. Select the Map background first, so the keys act on the Map rather than on a text field.

| Mac | Windows and Linux | Action |
| --- | --- | --- |
| {kbd}`tab` | {kbd}`tab` | Move the focus from one node to the next. The focused node is selected. |
| {kbd}`up` {kbd}`down` {kbd}`left` {kbd}`right` | {kbd}`up` {kbd}`down` {kbd}`left` {kbd}`right` | Move the focused node on the Map. |
| {kbd}`enter` | {kbd}`enter` | Open the focused node. |
| {kbd}`del` or {kbd}`backspace` | {kbd}`del` or {kbd}`backspace` | Delete the selected source or destination. |
| {kbd}`cmd+z` | {kbd}`ctrl+z` | Undo the last edit. |
| {kbd}`cmd+shift+z` | {kbd}`ctrl+shift+z` or {kbd}`ctrl+y` | Redo the edit you undid. |
| {kbd}`esc` | {kbd}`esc` | Close an open menu and clear the selection. |

## Related pages [streams-map-related]

* [How Streams works](get-started/how-streams-work.md): Understand what sources, pipelines, routers, and destinations do and where each one runs.
* [Monitor streams](monitor-streams.md): Learn what the states and statistics on nodes and in the tables mean.
* [Troubleshooting](troubleshooting.md#streams-troubleshoot-no-data): Find out what to check when a destination shows **Data not flowing in**.
* [Streams glossary](glossary.md): Look up node, connection, stream, and the other terms used on this page.
