# Stack Management [management]

**Stack Management** is home to UIs for managing all things Elastic Stack— indices, clusters, licenses, UI settings, data views, spaces, and more.

Access to individual features is governed by {{es}} and {{kib}} privileges. Consult your administrator if you do not have the appropriate access.


## Ingest [manage-ingest]

|     |     |
| --- | --- |
| [Ingest Pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) | Create and manage ingest pipelines that let you perform common transformationsand enrichments on your data. |
| [Logstash Pipelines](https://www.elastic.co/guide/en/logstash/current/logstash-centralized-pipeline-management.html) | Create, edit, and delete your Logstash pipeline configurations. |


## Data [manage-data]

|     |     |
| --- | --- |
| [Index Management](../../../manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md) | View index settings, mappings, and statistics and perform operations, such as refreshing,flushing, and clearing the cache. Practicing good index management ensuresthat your data is stored cost effectively. |
| [Index Lifecycle Policies](../../../manage-data/lifecycle/index-lifecycle-management.md) | Create a policy for defining the lifecycle of an index as it agesthrough the hot, warm, cold, and delete phases.Such policies help you control operation costsbecause you can put data in different resource tiers. |
| [Snapshot and Restore](../../../deploy-manage/tools/snapshot-and-restore.md) | Define a policy that creates, schedules, and automatically deletes snapshots to ensure that youhave backups of your cluster in case something goes wrong. |
| [Rollup Jobs](../../../manage-data/lifecycle/rollup.md) | [8.11.0] Create a job that periodically aggregates data from one or more indices, and thenrolls it into a new, compact index. Rollup indices are a good way to store months oryears of historical data in combination with your raw data. |
| [Transforms](../../../explore-analyze/transforms.md) | Use transforms to pivot existing {{es}} indices into summarized or entity-centric indices. |
| [Cross-Cluster Replication](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-tutorial.html) | Replicate indices on a remote cluster and copy them to a follower index on a local cluster.This is important fordisaster recovery. It also keeps data local for faster queries. |
| [Remote Clusters](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-tutorial.html#ccr-getting-started-remote-cluster) | Manage your remote clusters for use with cross-cluster search and cross-cluster replication.You can add and remove remote clusters, and check their connectivity. |


## Alerts and Insights [manage-alerts-insights]

|     |     |
| --- | --- |
| [{{rules-ui}}](../../../explore-analyze/alerts-cases.md) | Centrally [manage your rules](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md) across {{kib}}. |
| [Cases](../../../explore-analyze/alerts-cases/cases.md) | Create and manage cases to investigate issues. |
| [{{connectors-ui}}](../../../deploy-manage/manage-connectors.md) | Create and [manage reusable connectors](../../../deploy-manage/manage-connectors.md) for triggering actions. |
| [Reporting](../../../explore-analyze/report-and-share.md) | Monitor the generation of reports—PDF, PNG, and CSV—and download reports that you previously generated.A report can contain a dashboard, visualization, table with Discover search results, or Canvas workpad. |
| Machine Learning Jobs | View, export, and import your [{{anomaly-detect}}](../../../explore-analyze/machine-learning/anomaly-detection.md) and[{{dfanalytics}}](../../../explore-analyze/machine-learning/data-frame-analytics.md) jobs. Open the Single MetricViewer or Anomaly Explorer to see your {{anomaly-detect}} results. |
| [Watcher](../../../explore-analyze/alerts-cases/watcher.md) | Detect changes in your data by creating, managing, and monitoring alerts.For example, you might create an alert when the maximum total CPU usage on a machine goesabove a certain percentage. |
| [Maintenance windows](../../../explore-analyze/alerts-cases/alerts/maintenance-windows.md) | Suppress rule notifications for scheduled periods of time. |


## Security [manage-security]

|     |     |
| --- | --- |
| [Users](../../../deploy-manage/security.md) | View the users that have been defined on your cluster.Add or delete users and assign roles that give usersspecific privileges. |
| [Roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) | View the roles that exist on your cluster. Customizethe actions that a user with the role can perform, on a cluster, index, and space level. |
| [API Keys](../../../deploy-manage/api-keys/elasticsearch-api-keys.md) | Create secondary credentials so that you can send requests on behalf of the user.Secondary credentials have the same or lower access rights. |
| [Role Mappings](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) | Assign roles to your users using a set of rules. Role mappings are requiredwhen authenticating via an external identity provider, such as Active Directory,Kerberos, PKI, OIDC, and SAML. |


## {{kib}} [manage-kibana]

|     |     |
| --- | --- |
| [Data Views](../../../explore-analyze/find-and-organize/data-views.md) | Manage the fields in the data views that retrieve your data from {{es}}. |
| [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md) | Copy, edit, delete, import, and export your saved objects.These include dashboards, visualizations, maps, data views, Canvas workpads, and more. |
| [Tags](../../../explore-analyze/find-and-organize/tags.md) | Create, manage, and assign tags to your saved objects. |
| [Search Sessions](../../../explore-analyze/discover/search-sessions.md) | Manage your saved search sessions, groups of queries that run in the background.Search sessions are useful when your queries take longer than usual to process,for example, when you have a large volume of data or when the performance of your storage location is slow. |
| [Spaces](../../../deploy-manage/manage-spaces.md) | Create spaces to organize your dashboards and other saved objects into categories.A space is isolated from all other spaces,so you can tailor it to your needs without impacting others. |
| [Advanced Settings](https://www.elastic.co/guide/en/kibana/current/advanced-options.html) | Customize {{kib}} to suit your needs. Change the format for displaying dates, turn on dark mode,set the timespan for notification messages, and much more. |


## Stack [manage-stack]

|     |     |
| --- | --- |
| [License Management](../../../deploy-manage/license/manage-your-license-in-self-managed-cluster.md) | View the status of your license, start a trial, or install a new license. Forthe full list of features that are included in your license,see the [subscription page](https://www.elastic.co/subscriptions). |

