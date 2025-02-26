---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/timeline-object-schema.html
  - https://www.elastic.co/guide/en/serverless/current/security-timeline-object-schema.html
---

# Timeline schema [timeline-object-schema]

The Timeline schema lists all the JSON fields and objects required to create a Timeline or a Timeline template using the Create Timeline API.

::::{important}
All column, dropzone, and filter fields must be [ECS fields](ecs://docs/reference/index.md).
::::


This screenshot maps the Timeline UI components to their JSON objects:

:::{image} ../../../images/security-timeline-object-ui.png
:alt: timeline object ui
:class: screenshot
:::

1. [Title](#timeline-object-title) (`title`)
2. [Global notes](#timeline-object-global-notes) (`globalNotes`)
3. [Data view](#timeline-object-dataViewId) (`dataViewId`)
4. [KQL bar query](#timeline-object-kqlquery) (`kqlQuery`)
5. [Time filter](#timeline-object-daterange) (`dateRange`)
6. [Additional filters](#timeline-object-filters) (`filters`)
7. [KQL bar mode](#timeline-object-kqlmode) (`kqlMode`)
8. [Dropzone](#timeline-object-dropzone) (each clause is contained in its own `dataProviders` object)
9. [Column headers](#timeline-object-columns) (`columns`)
10. [Event-specific notes](#timeline-object-event-notes) (`eventNotes`)

| Name | Type | Description |
| --- | --- | --- |
| $$$timeline-object-columns$$$`columns` | [columns[]](#col-obj) | The Timeline’scolumns. |
| `created` | Float | The time the Timeline was created, using a 13-digit Epochtimestamp. |
| `createdBy` | String | The user who created the Timeline. |
| $$$timeline-object-dropzone$$$`dataProviders` | [dataProviders[]](#dataProvider-obj) | Object containing dropzone queryclauses. |
| $$$timeline-object-dataViewId$$$`dataViewId` | String | ID of the Timeline’s Data View, for example: `"dataViewId":"security-solution-default"`. |
| $$$timeline-object-daterange$$$`dateRange` | dateRange | The Timeline’s search period:<br><br>* `end`: The time up to which events are searched, using a 13-digit Epoch timestamp.<br>* `start`: The time from which events are searched, using a 13-digit Epoch timestamp.<br> |
| `description` | String | The Timeline’s description. |
| $$$timeline-object-event-notes$$$`eventNotes` | [eventNotes[]](#eventNotes-obj) | Notes added to specific events in the Timeline. |
| `eventType` | String | Event types displayed in the Timeline, which can be:<br><br>* `All data sources`<br>* `Events`: Event sources only<br>* `Detection Alerts`: Detection alerts only<br> |
| `favorite` | [favorite[]](#favorite-obj) | Indicates when and who marked aTimeline as a favorite. |
| $$$timeline-object-filters$$$`filters` | [filters[]](#filters-obj) | Filters usedin addition to the dropzone query. |
| $$$timeline-object-global-notes$$$`globalNotes` | [globalNotes[]](#globalNotes-obj) | Global notes added to the Timeline. |
| $$$timeline-object-kqlmode$$$`kqlMode` | String | Indicates whether the KQL bar filters the dropzone query results or searches for additional results, where:<br><br>* `filter`: filters dropzone query results<br>* `search`: displays additional search results<br> |
| $$$timeline-object-kqlquery$$$`kqlQuery` | [kqlQuery](#kqlQuery-obj) | KQL barquery. |
| `pinnedEventIds` | pinnedEventIds[] | IDs of events pinned to the Timeline’ssearch results. |
| `savedObjectId` | String | The Timeline’s saved object ID. |
| `savedQueryId` | String | If used, the saved query ID used to filter or searchdropzone query results. |
| `sort` | sort | Object indicating how rows are sorted in the Timeline’s grid:<br><br>* `columnId` (string): The ID of the column used to sort results.<br>* `sortDirection` (string): The sort direction, which can be either `desc` or `asc`.<br> |
| `templateTimelineId` | String | A unique ID (UUID) for Timeline templates. For Timelines, the value is `null`.<br> |
| `templateTimelineVersion` | Integer | Timeline template version number. ForTimelines, the value is `null`. |
| $$$timeline-object-typeField$$$`timelineType` | String | Indicates whether the Timeline is a template or not, where:<br><br>* `default`: Indicates a Timeline used to actively investigate events.<br>* `template`: Indicates a Timeline template used when detection rule alerts are investigated in Timeline.<br> |
| $$$timeline-object-title$$$`title` | String | The Timeline’s title. |
| `updated` | Float | The last time the Timeline was updated, using a13-digit Epoch timestamp. |
| `updatedBy` | String | The user who last updated the Timeline. |
| `version` | String | The Timeline’s version. |


## columns object [col-obj]

| Name | Type | Description |
| --- | --- | --- |
| `aggregatable` | Boolean | Indicates whether the field can be aggregated acrossall indices (used to sort columns in the UI). |
| `category` | String | The ECS field set to which the field belongs. |
| `description` | String | UI column field description tooltip. |
| `example` | String | UI column field example tooltip. |
| `indexes` | String | Security indices in which the field exists and has the same{{es}} type. `null` when all the security indices have the field with the sametype. |
| `id` | String | ECS field name, displayed as the column header in the UI. |
| `type` | String | The field’s type. |


## dataProviders object [dataProvider-obj]

| Name | Type | Description |
| --- | --- | --- |
| `and` | dataProviders[] | Array containing dropzone query clauses using `AND`logic. |
| `enabled` | Boolean | Indicates if the dropzone query clause is enabled. |
| `excluded` | Boolean | Indicates if the dropzone query clause uses `NOT` logic. |
| `id` | String | The dropzone query clause’s unique ID. |
| `name` | String | The dropzone query clause’s name (the clause’s valuewhen Timelines are exported from the UI). |
| `queryMatch` | queryMatch | The dropzone query clause:<br><br>* `field` (string): The field used to search Security indices.<br>* `operator` (string): The clause’s operator, which can be:<br><br>    * `:` - The `field` has the specified `value`.<br>    * `:*` - The field exists.<br><br>* `value` (string): The field’s value used to match results.<br> |


## eventNotes object [eventNotes-obj]

| Name | Type | Description |
| --- | --- | --- |
| `created` | Float | The time the note was created, using a 13-digit Epochtimestamp. |
| `createdBy` | String | The user who added the note. |
| `eventId` | String | The ID of the event to which the note was added. |
| `note` | String | The note’s text. |
| `noteId` | String | The note’s ID |
| `timelineId` | String | The ID of the Timeline to which the note was added. |
| `updated` | Float | The last time the note was updated, using a13-digit Epoch timestamp. |
| `updatedBy` | String | The user who last updated the note. |
| `version` | String | The note’s version. |


## favorite object [favorite-obj]

| Name | Type | Description |
| --- | --- | --- |
| `favoriteDate` | Float | The time the Timeline was marked as a favorite, using a13-digit Epoch timestamp. |
| `fullName` | String | The full name of the user who marked the Timeline asa favorite. |
| `keySearch` | String | `userName` encoded in Base64. |
| `userName` | String | The {{kib}} username of the user who marked theTimeline as a favorite. |


## filters object [filters-obj]

| Name | Type | Description |
| --- | --- | --- |
| `exists` | String | [Exists term query](elasticsearch://docs/reference/query-languages/query-dsl-exists-query.md) for thespecified field (`null` when undefined). For example, `{"field":"user.name"}`. |
| `meta` | meta | Filter details:<br><br>* `alias` (string): UI filter name.<br>* `disabled` (boolean): Indicates if the filter is disabled.<br>* `key`(string): Field name or unique string ID.<br>* `negate` (boolean): Indicates if the filter query clause uses `NOT` logic.<br>* `params` (string): Value of `phrase` filter types.<br>* `type` (string): Type of filter. For example, `exists` and `range`. For more information about filtering, see [Query DSL](elasticsearch://docs/reference/query-languages/querydsl.md).<br> |
| `match_all` | String | [Match all term query](elasticsearch://docs/reference/query-languages/query-dsl-match-all-query.md)for the specified field (`null` when undefined). |
| `query` | String | [DSL query](elasticsearch://docs/reference/query-languages/querydsl.md) (`null` when undefined). Forexample, `{"match_phrase":{"ecs.version":"1.4.0"}}`. |
| `range` | String | [Range query](elasticsearch://docs/reference/query-languages/query-dsl-range-query.md) (`null` whenundefined). For example, `{"@timestamp":{"gte":"now-1d","lt":"now"}}"`. |


## globalNotes object [globalNotes-obj]

| Name | Type | Description |
| --- | --- | --- |
| `created` | Float | The time the note was created, using a 13-digit Epochtimestamp. |
| `createdBy` | String | The user who added the note. |
| `note` | String | The note’s text. |
| `noteId` | String | The note’s ID |
| `timelineId` | String | The ID of the Timeline to which the note was added. |
| `updated` | Float | The last time the note was updated, using a13-digit Epoch timestamp. |
| `updatedBy` | String | The user who last updated the note. |
| `version` | String | The note’s version. |


## kqlQuery object [kqlQuery-obj]

| Name | Type | Description |
| --- | --- | --- |
| `filterQuery` | filterQuery | Object containing query details:<br><br>* `kuery`: Object containing the query’s clauses and type:<br><br>    * `expression`(string): The query’s clauses.<br>    * `kind` (string): The type of query, which can be `kuery` or `lucene`.<br><br>* `serializedQuery` (string): The query represented in JSON format.<br> |

