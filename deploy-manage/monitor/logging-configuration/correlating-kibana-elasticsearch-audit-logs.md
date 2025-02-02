---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
---

# Correlating Kibana and Elasticsearch audit logs [xpack-security-audit-logging]

Audit logging is a [subscription feature](https://www.elastic.co/subscriptions) that you can enable to keep track of security-related events, such as authorization success and failures. Logging these events enables you to monitor {{kib}} for suspicious activity and provides evidence in the event of an attack.

Use the {{kib}} audit logs in conjunction with [{{es}} audit logging](enabling-elasticsearch-audit-logs.md) to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges. For more information on enabling audit logging in {{es}}, refer to [Auditing security events](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing.html).

::::{note}
Audit logs are **disabled** by default. To enable this functionality, you must set `xpack.security.audit.enabled` to `true` in `kibana.yml`.

You can optionally configure audit logs location, file/rolling file appenders and ignore filters using [Audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings).

::::


## Audit events [xpack-security-ecs-audit-logging]

Refer to the table of events that can be logged for auditing purposes.

Each event is broken down into [category](enabling-kibana-audit-logs.md#field-event-category), [type](enabling-kibana-audit-logs.md#field-event-type), [action](enabling-kibana-audit-logs.md#field-event-action) and [outcome](enabling-kibana-audit-logs.md#field-event-outcome) fields to make it easy to filter, query and aggregate the resulting logs. The [trace.id](enabling-kibana-audit-logs.md#field-trace-id) field can be used to correlate multiple events that originate from the same request.

Refer to [Audit schema](enabling-kibana-audit-logs.md#xpack-security-ecs-audit-schema) for a table of fields that get logged with audit event.

::::{note}
To ensure that a record of every operation is persisted even in case of an unexpected error, asynchronous write operations are logged immediately after all authorization checks have passed, but before the response from {{es}} is received. Refer to the corresponding {{es}} logs for potential write errors.

::::


|     |
| --- |
| #### Category: authentication [_category_authentication]<br><br><br> |
| **Action** | **Outcome** | **Description** |
| `user_login` | `success` | User has logged in successfully. |
| `failure` | Failed login attempt (e.g. due to invalid credentials). |
| `user_logout` | `unknown` | User is logging out. |
| `session_cleanup` | `unknown` | Removing invalid or expired session. |
| `access_agreement_acknowledged` | n/a | User has acknowledged the access agreement. |
| #### Category: database [_category_database]<br><br>##### Type: creation [_type_creation]<br><br><br><br> |
| **Action** | **Outcome** | **Description** |
| `saved_object_create` | `unknown` | User is creating a saved object. |
| `failure` | User is not authorized to create a saved object. |
| `saved_object_open_point_in_time` | `unknown` | User is creating a Point In Time to use when querying saved objects. |
| `failure` | User is not authorized to create a Point In Time for the provided saved object types. |
| `connector_create` | `unknown` | User is creating a connector. |
| `failure` | User is not authorized to create a connector. |
| `rule_create` | `unknown` | User is creating a rule. |
| `failure` | User is not authorized to create a rule. |
| `ad_hoc_run_create` | `unknown` | User is creating an ad hoc run. |
| `failure` | User is not authorized to create an ad hoc run. |
| `space_create` | `unknown` | User is creating a space. |
| `failure` | User is not authorized to create a space. |
| `case_create` | `unknown` | User is creating a case. |
| `failure` | User is not authorized to create a case. |
| `case_configuration_create` | `unknown` | User is creating a case configuration. |
| `failure` | User is not authorized to create a case configuration. |
| `case_comment_create` | `unknown` | User is creating a case comment. |
| `failure` | User is not authorized to create a case comment. |
| `case_comment_bulk_create` | `unknown` | User is creating multiple case comments. |
| `failure` | User is not authorized to create multiple case comments. |
| `case_user_action_create_comment` | `success` | User has created a case comment. |
| `case_user_action_create_case` | `success` | User has created a case. |
| `ml_put_ad_job` | `success` | Creating anomaly detection job. |
| `failure` | Failed to create anomaly detection job. |
| `ml_put_ad_datafeed` | `success` | Creating anomaly detection datafeed. |
| `failure` | Failed to create anomaly detection datafeed. |
| `ml_put_calendar` | `success` | Creating calendar. |
| `failure` | Failed to create calendar. |
| `ml_post_calendar_events` | `success` | Adding events to calendar. |
| `failure` | Failed to add events to calendar. |
| `ml_forecast` | `success` | Creating anomaly detection forecast. |
| `failure` | Failed to create anomaly detection forecast. |
| `ml_put_filter` | `success` | Creating filter. |
| `failure` | Failed to create filter. |
| `ml_put_dfa_job` | `success` | Creating data frame analytics job. |
| `failure` | Failed to create data frame analytics job. |
| `ml_put_trained_model` | `success` | Creating trained model. |
| `failure` | Failed to create trained model. |
| `product_documentation_create` | `unknown` | User requested to install the product documentation for use in AI Assistants. |
| `knowledge_base_entry_create` | `success` | User has created knowledge base entry [id=x] |
| `failure` | Failed attempt to create a knowledge base entry |
| `knowledge_base_entry_update` | `success` | User has updated knowledge base entry [id=x] |
| `failure` | Failed attempt to update a knowledge base entry |
| `knowledge_base_entry_delete` | `success` | User has deleted knowledge base entry [id=x] |
| `failure` | Failed attempt to delete a knowledge base entry |
| ##### Type: change [_type_change]<br><br><br> |
| **Action** | **Outcome** | **Description** |
| `saved_object_update` | `unknown` | User is updating a saved object. |
| `failure` | User is not authorized to update a saved object. |
| `saved_object_update_objects_spaces` | `unknown` | User is adding and/or removing a saved object to/from other spaces. |
| `failure` | User is not authorized to add or remove a saved object to or from other spaces. |
| `saved_object_remove_references` | `unknown` | User is removing references to a saved object. |
| `failure` | User is not authorized to remove references to a saved object. |
| `saved_object_collect_multinamespace_references` | `success` | User has accessed references to a multi-space saved object. |
| `failure` | User is not authorized to access references to a multi-space saved object. |
| `connector_update` | `unknown` | User is updating a connector. |
| `failure` | User is not authorized to update a connector. |
| `rule_update` | `unknown` | User is updating a rule. |
| `failure` | User is not authorized to update a rule. |
| `rule_update_api_key` | `unknown` | User is updating the API key of a rule. |
| `failure` | User is not authorized to update the API key of a rule. |
| `rule_enable` | `unknown` | User is enabling a rule. |
| `failure` | User is not authorized to enable a rule. |
| `rule_disable` | `unknown` | User is disabling a rule. |
| `failure` | User is not authorized to disable a rule. |
| `rule_mute` | `unknown` | User is muting a rule. |
| `failure` | User is not authorized to mute a rule. |
| `rule_unmute` | `unknown` | User is unmuting a rule. |
| `failure` | User is not authorized to unmute a rule. |
| `rule_alert_mute` | `unknown` | User is muting an alert. |
| `failure` | User is not authorized to mute an alert. |
| `rule_alert_unmute` | `unknown` | User is unmuting an alert. |
| `failure` | User is not authorized to unmute an alert. |
| `space_update` | `unknown` | User is updating a space. |
| `failure` | User is not authorized to update a space. |
| `alert_update` | `unknown` | User is updating an alert. |
| `failure` | User is not authorized to update an alert. |
| `rule_snooze` | `unknown` | User is snoozing a rule. |
| `failure` | User is not authorized to snooze a rule. |
| `rule_unsnooze` | `unknown` | User is unsnoozing a rule. |
| `failure` | User is not authorized to unsnooze a rule. |
| `case_update` | `unknown` | User is updating a case. |
| `failure` | User is not authorized to update a case. |
| `case_push` | `unknown` | User is pushing a case to an external service. |
| `failure` | User is not authorized to push a case to an external service. |
| `case_configuration_update` | `unknown` | User is updating a case configuration. |
| `failure` | User is not authorized to update a case configuration. |
| `case_comment_update` | `unknown` | User is updating a case comment. |
| `failure` | User is not authorized to update a case comment. |
| `case_user_action_add_case_assignees` | `success` | User has added a case assignee. |
| `case_user_action_update_case_connector` | `success` | User has updated a case connector. |
| `case_user_action_update_case_description` | `success` | User has updated a case description. |
| `case_user_action_update_case_settings` | `success` | User has updated the case settings. |
| `case_user_action_update_case_severity` | `success` | User has updated the case severity. |
| `case_user_action_update_case_status` | `success` | User has updated the case status. |
| `case_user_action_pushed_case` | `success` | User has pushed a case to an external service. |
| `case_user_action_add_case_tags` | `success` | User has added tags to a case. |
| `case_user_action_update_case_title` | `success` | User has updated the case title. |
| `ml_open_ad_job` | `success` | Opening anomaly detection job. |
| `failure` | Failed to open anomaly detection job. |
| `ml_close_ad_job` | `success` | Closing anomaly detection job. |
| `failure` | Failed to close anomaly detection job. |
| `ml_start_ad_datafeed` | `success` | Starting anomaly detection datafeed. |
| `failure` | Failed to start anomaly detection datafeed. |
| `ml_stop_ad_datafeed` | `success` | Stopping anomaly detection datafeed. |
| `failure` | Failed to stop anomaly detection datafeed. |
| `ml_update_ad_job` | `success` | Updating anomaly detection job. |
| `failure` | Failed to update anomaly detection job. |
| `ml_reset_ad_job` | `success` | Resetting anomaly detection job. |
| `failure` | Failed to reset anomaly detection job. |
| `ml_revert_ad_snapshot` | `success` | Reverting anomaly detection snapshot. |
| `failure` | Failed to revert anomaly detection snapshot. |
| `ml_update_ad_datafeed` | `success` | Updating anomaly detection datafeed. |
| `failure` | Failed to update anomaly detection datafeed. |
| `ml_put_calendar_job` | `success` | Adding job to calendar. |
| `failure` | Failed to add job to calendar. |
| `ml_delete_calendar_job` | `success` | Removing job from calendar. |
| `failure` | Failed to remove job from calendar. |
| `ml_update_filter` | `success` | Updating filter. |
| `failure` | Failed to update filter. |
| `ml_start_dfa_job` | `success` | Starting data frame analytics job. |
| `failure` | Failed to start data frame analytics job. |
| `ml_stop_dfa_job` | `success` | Stopping data frame analytics job. |
| `failure` | Failed to stop data frame analytics job. |
| `ml_update_dfa_job` | `success` | Updating data frame analytics job. |
| `failure` | Failed to update data frame analytics job. |
| `ml_start_trained_model_deployment` | `success` | Starting trained model deployment. |
| `failure` | Failed to start trained model deployment. |
| `ml_stop_trained_model_deployment` | `success` | Stopping trained model deployment. |
| `failure` | Failed to stop trained model deployment. |
| `ml_update_trained_model_deployment` | `success` | Updating trained model deployment. |
| `failure` | Failed to update trained model deployment. |
| `product_documentation_update` | `unknown` | User requested to update the product documentation for use in AI Assistants. |
| ##### Type: deletion [_type_deletion]<br><br><br> |
| **Action** | **Outcome** | **Description** |
| `saved_object_delete` | `unknown` | User is deleting a saved object. |
| `failure` | User is not authorized to delete a saved object. |
| `saved_object_close_point_in_time` | `unknown` | User is deleting a Point In Time that was used to query saved objects. |
| `failure` | User is not authorized to delete a Point In Time. |
| `connector_delete` | `unknown` | User is deleting a connector. |
| `failure` | User is not authorized to delete a connector. |
| `rule_delete` | `unknown` | User is deleting a rule. |
| `failure` | User is not authorized to delete a rule. |
| `ad_hoc_run_delete` | `unknown` | User is deleting an ad hoc run. |
| `failure` | User is not authorized to delete an ad hoc run. |
| `space_delete` | `unknown` | User is deleting a space. |
| `failure` | User is not authorized to delete a space. |
| `case_delete` | `unknown` | User is deleting a case. |
| `failure` | User is not authorized to delete a case. |
| `case_comment_delete_all` | `unknown` | User is deleting all comments associated with a case. |
| `failure` | User is not authorized to delete all comments associated with a case. |
| `case_comment_delete` | `unknown` | User is deleting a case comment. |
| `failure` | User is not authorized to delete a case comment. |
| `case_user_action_delete_case_assignees` | `success` | User has removed a case assignee. |
| `case_user_action_delete_comment` | `success` | User has deleted a case comment. |
| `case_user_action_delete_case` | `success` | User has deleted a case. |
| `case_user_action_delete_case_tags` | `success` | User has removed tags from a case. |
| `ml_delete_ad_job` | `success` | Deleting anomaly detection job. |
| `failure` | Failed to delete anomaly detection job. |
| `ml_delete_model_snapshot` | `success` | Deleting model snapshot. |
| `failure` | Failed to delete model snapshot. |
| `ml_delete_ad_datafeed` | `success` | Deleting anomaly detection datafeed. |
| `failure` | Failed to delete anomaly detection datafeed. |
| `ml_delete_calendar` | `success` | Deleting calendar. |
| `failure` | Failed to delete calendar. |
| `ml_delete_calendar_event` | `success` | Deleting calendar event. |
| `failure` | Failed to delete calendar event. |
| `ml_delete_filter` | `success` | Deleting filter. |
| `failure` | Failed to delete filter. |
| `ml_delete_forecast` | `success` | Deleting forecast. |
| `failure` | Failed to delete forecast. |
| `ml_delete_dfa_job` | `success` | Deleting data frame analytics job. |
| `failure` | Failed to delete data frame analytics job. |
| `ml_delete_trained_model` | `success` | Deleting trained model. |
| `failure` | Failed to delete trained model. |
| `product_documentation_delete` | `unknown` | User requested to delete the product documentation for use in AI Assistants. |
| ##### Type: access [_type_access]<br><br><br> |
| **Action** | **Outcome** | **Description** |
| `saved_object_get` | `success` | User has accessed a saved object. |
| `failure` | User is not authorized to access a saved object. |
| `saved_object_resolve` | `success` | User has accessed a saved object. |
| `failure` | User is not authorized to access a saved object. |
| `saved_object_find` | `success` | User has accessed a saved object as part of a search operation. |
| `failure` | User is not authorized to search for saved objects. |
| `connector_get` | `success` | User has accessed a connector. |
| `failure` | User is not authorized to access a connector. |
| `connector_find` | `success` | User has accessed a connector as part of a search operation. |
| `failure` | User is not authorized to search for connectors. |
| `rule_get` | `success` | User has accessed a rule. |
| `failure` | User is not authorized to access a rule. |
| `rule_get_execution_log` | `success` | User has accessed execution log for a rule. |
| `failure` | User is not authorized to access execution log for a rule. |
| `rule_find` | `success` | User has accessed a rule as part of a search operation. |
| `failure` | User is not authorized to search for rules. |
| `rule_schedule_backfill` | `success` | User has accessed a rule as part of a backfill schedule operation. |
| `failure` | User is not authorized to access rule for backfill scheduling. |
| `ad_hoc_run_get` | `success` | User has accessed an ad hoc run. |
| `failure` | User is not authorized to access ad hoc run. |
| `ad_hoc_run_find` | `success` | User has accessed an ad hoc run as part of a search operation. |
| `failure` | User is not authorized to search for ad hoc runs. |
| `space_get` | `success` | User has accessed a space. |
| `failure` | User is not authorized to access a space. |
| `space_find` | `success` | User has accessed a space as part of a search operation. |
| `failure` | User is not authorized to search for spaces. |
| `alert_get` | `success` | User has accessed an alert. |
| `failure` | User is not authorized to access an alert. |
| `alert_find` | `success` | User has accessed an alert as part of a search operation. |
| `failure` | User is not authorized to access alerts. |
| `case_get` | `success` | User has accessed a case. |
| `failure` | User is not authorized to access a case. |
| `case_bulk_get` | `success` | User has accessed multiple cases. |
| `failure` | User is not authorized to access multiple cases. |
| `case_resolve` | `success` | User has accessed a case. |
| `failure` | User is not authorized to access a case. |
| `case_find` | `success` | User has accessed a case as part of a search operation. |
| `failure` | User is not authorized to search for cases. |
| `case_ids_by_alert_id_get` | `success` | User has accessed cases. |
| `failure` | User is not authorized to access cases. |
| `case_get_metrics` | `success` | User has accessed metrics for a case. |
| `failure` | User is not authorized to access metrics for a case. |
| `cases_get_metrics` | `success` | User has accessed metrics for cases. |
| `failure` | User is not authorized to access metrics for cases. |
| `case_configuration_find` | `success` | User has accessed a case configuration as part of a search operation. |
| `failure` | User is not authorized to search for case configurations. |
| `case_comment_get_metrics` | `success` | User has accessed metrics for case comments. |
| `failure` | User is not authorized to access metrics for case comments. |
| `case_comment_alerts_attach_to_case` | `success` | User has accessed case alerts. |
| `failure` | User is not authorized to access case alerts. |
| `case_comment_get` | `success` | User has accessed a case comment. |
| `failure` | User is not authorized to access a case comment. |
| `case_comment_bulk_get` | `success` | User has accessed multiple case comments. |
| `failure` | User is not authorized to access multiple case comments. |
| `case_comment_get_all` | `success` | User has accessed case comments. |
| `failure` | User is not authorized to access case comments. |
| `case_comment_find` | `success` | User has accessed a case comment as part of a search operation. |
| `failure` | User is not authorized to search for case comments. |
| `case_categories_get` | `success` | User has accessed a case. |
| `failure` | User is not authorized to access a case. |
| `case_tags_get` | `success` | User has accessed a case. |
| `failure` | User is not authorized to access a case. |
| `case_reporters_get` | `success` | User has accessed a case. |
| `failure` | User is not authorized to access a case. |
| `case_find_statuses` | `success` | User has accessed a case as part of a search operation. |
| `failure` | User is not authorized to search for cases. |
| `case_user_actions_get` | `success` | User has accessed the user activity of a case. |
| `failure` | User is not authorized to access the user activity of a case. |
| `case_user_actions_find` | `success` | User has accessed the user activity of a case as part of a search operation. |
| `failure` | User is not authorized to access the user activity of a case. |
| `case_user_action_get_metrics` | `success` | User has accessed metrics for the user activity of a case. |
| `failure` | User is not authorized to access metrics for the user activity of a case. |
| `case_user_action_get_users` | `success` | User has accessed the users associated with a case. |
| `failure` | User is not authorized to access the users associated with a case. |
| `case_connectors_get` | `success` | User has accessed the connectors of a case. |
| `failure` | User is not authorized to access the connectors of a case. |
| `ml_infer_trained_model` | `success` | Inferring using trained model. |
| `failure` | Failed to infer using trained model. |
| #### Category: web [_category_web]<br><br><br> |
| **Action** | **Outcome** | **Description** |
| `http_request` | `unknown` | User is making an HTTP request. |


## Audit schema [xpack-security-ecs-audit-schema]

Audit logs are written in JSON using [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/1.6/index.html) specification.

|     |
| --- |
| #### Base Fields [_base_fields]<br><br><br> |
| **Field** | **Description** |
| `@timestamp` | Time when the event was generated.<br>Example: `2016-05-23T08:05:34.853Z` |
| `message` | Human readable description of the event. |
| #### Event Fields [_event_fields]<br><br><br> |
| **Field** | **Description** |
| $$$field-event-action$$$ `event.action` | The action captured by the event.<br>Refer to [Audit events](enabling-kibana-audit-logs.md#xpack-security-ecs-audit-logging) for a table of possible actions. |
| $$$field-event-category$$$ `event.category` | High level category associated with the event.<br>This field is closely related to `event.type`, which is used as a subcategory.<br>Possible values:`database`,`web`,`authentication` |
| $$$field-event-type$$$ `event.type` | Subcategory associated with the event.<br>This field can be used along with the `event.category` field to enable filtering events down to a level appropriate for single visualization.<br>Possible values:`creation`,`access`,`change`,`deletion` |
| $$$field-event-outcome$$$ `event.outcome` | Denotes whether the event represents a success or failure:<br><br>* Any actions that the user is not authorized to perform are logged with outcome:  `failure`<br>* Authorized read operations are only logged after successfully fetching the data from {{es}} with outcome: `success`<br>* Authorized create, update, or delete operations are logged before attempting the operation in {{es}} with outcome: `unknown`<br><br>Possible values: `success`, `failure`, `unknown`<br> |
| #### User Fields [_user_fields]<br><br><br> |
| **Field** | **Description** |
| `user.id` | Unique identifier of the user across sessions (See [user profiles](../../users-roles/cluster-or-deployment-auth/user-profiles.md)). |
| `user.name` | Login name of the user.<br>Example: `jdoe` |
| `user.roles[]` | Set of user roles at the time of the event.<br>Example: `[kibana_admin, reporting_user]` |
| #### Kibana Fields [_kibana_fields]<br><br><br> |
| **Field** | **Description** |
| `kibana.space_id` | ID of the space associated with the event.<br>Example: `default` |
| `kibana.session_id` | ID of the user session associated with the event.<br>Each login attempt results in a unique session id. |
| `kibana.saved_object.type` | Type of saved object associated with the event.<br>Example: `dashboard` |
| `kibana.saved_object.id` | ID of the saved object associated with the event. |
| `kibana.authentication_provider` | Name of the authentication provider associated with the event.<br>Example: `my-saml-provider` |
| `kibana.authentication_type` | Type of the authentication provider associated with the event.<br>Example: `saml` |
| `kibana.authentication_realm` | Name of the Elasticsearch realm that has authenticated the user.<br>Example: `native` |
| `kibana.lookup_realm` | Name of the Elasticsearch realm where the user details were retrieved from.<br>Example: `native` |
| `kibana.add_to_spaces[]` | Set of space IDs that a saved object is being shared to as part of the event.<br>Example: `[default, marketing]` |
| `kibana.delete_from_spaces[]` | Set of space IDs that a saved object is being removed from as part of the event.<br>Example: `[marketing]` |
| #### Error Fields [_error_fields]<br><br><br> |
| **Field** | **Description** |
| `error.code` | Error code describing the error. |
| `error.message` | Error message. |
| #### HTTP and URL Fields [_http_and_url_fields]<br><br><br> |
| **Field** | **Description** |
| `client.ip` | Client IP address. |
| `http.request.method` | HTTP request method.<br>Example: `get`, `post`, `put`, `delete` |
| `http.request.headers.x-forwarded-for` | `X-Forwarded-For` request header used to identify the originating client IP address when connecting through proxy servers.<br>Example: `161.66.20.177, 236.198.214.101` |
| `url.domain` | Domain of the URL.<br>Example: `www.elastic.co` |
| `url.path` | Path of the request.<br>Example: `/search` |
| `url.port` | Port of the request.<br>Example: `443` |
| `url.query` | The query field describes the query string of the request.<br>Example: `q=elasticsearch` |
| `url.scheme` | Scheme of the request.<br>Example: `https` |
| #### Tracing Fields [_tracing_fields]<br><br><br> |
| **Field** | **Description** |
| $$$field-trace-id$$$ `trace.id` | Unique identifier allowing events of the same transaction from {{kib}} and {{es}} to be correlated. |


## Correlating audit events [xpack-security-ecs-audit-correlation]

Audit events can be correlated in two ways:

1. Multiple {{kib}} audit events that resulted from the same request can be correlated together.
2. If [{{es}} audit logging](enabling-elasticsearch-audit-logs.md) is enabled, {{kib}} audit events from one request can be correlated with backend calls that create {{es}} audit events.

::::{note}
The examples below are simplified, many fields have been omitted and values have been shortened for clarity.
::::


### Example 1: correlating multiple {{kib}} audit events [_example_1_correlating_multiple_kib_audit_events]

When "thom" creates a new alerting rule, five audit events are written:

```json
{"event":{"action":"http_request","category":["web"],"outcome":"unknown"},"http":{"request":{"method":"post"}},"url":{"domain":"localhost","path":"/api/alerting/rule","port":5601,"scheme":"https"},"user":{"name":"thom","roles":["superuser"]},"kibana":{"space_id":"default","session_id":"3dHCZRB..."},"@timestamp":"2022-01-25T13:05:34.449-05:00","message":"User is requesting [/api/alerting/rule] endpoint","trace":{"id":"e300e06..."}}
{"event":{"action":"space_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"space","id":"default"}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.454-05:00","message":"User has accessed space [id=default]","trace":{"id":"e300e06..."}}
{"event":{"action":"connector_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"action","id":"5e3b1ae..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.948-05:00","message":"User has accessed connector [id=5e3b1ae...]","trace":{"id":"e300e06..."}}
{"event":{"action":"connector_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"action","id":"5e3b1ae..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.956-05:00","message":"User has accessed connector [id=5e3b1ae...]","trace":{"id":"e300e06..."}}
{"event":{"action":"rule_create","category":["database"],"type":["creation"],"outcome":"unknown"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"alert","id":"64517c3..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.956-05:00","message":"User is creating rule [id=64517c3...]","trace":{"id":"e300e06..."}}
```

All of these audit events can be correlated together by the same `trace.id` value `"e300e06..."`. The first event is the HTTP API call, the next audit events are checks to validate the space and the connectors, and the last audit event is the actual rule creation.


### Example 2: correlating a {{kib}} audit event with {{es}} audit events [_example_2_correlating_a_kib_audit_event_with_es_audit_events]

When "thom" logs in, a "user_login" {{kib}} audit event is written:

```json
{"event":{"action":"user_login","category":["authentication"],"outcome":"success"},"kibana":{"session_id":"ab93zdA..."},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T09:40:39.267-05:00","message":"User [thom] has logged in using basic provider [name=basic]","trace":{"id":"818cbf3..."}}
```

The `trace.id` value `"818cbf3..."` in the {{kib}} audit event can be correlated with the `opaque_id` value in these six {{es}} audit events:

```json
{"type":"audit", "timestamp":"2022-01-25T09:40:38,604-0500", "event.action":"access_granted", "user.name":"thom", "user.roles":["superuser"], "request.id":"YCx8wxs...", "action":"cluster:admin/xpack/security/user/authenticate", "request.name":"AuthenticateRequest", "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/index", "request.name":"IndexRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk", "request.name":"BulkRequest", "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk[s]", "request.name":"BulkShardRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/index:op_type/create", "request.name":"BulkItemRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk[s][p]", "request.name":"BulkShardRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
```

The {{es}} audit events show that "thom" authenticated, then subsequently "kibana_system" created a session for that user.
