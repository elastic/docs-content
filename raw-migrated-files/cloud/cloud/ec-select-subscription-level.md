# Choose a subscription level [ec-select-subscription-level]

When you decide to add your credit card and become a paying customer, you can choose a subscription level that includes the features you are going to use. On our [pricing page](https://www.elastic.co/cloud/elasticsearch-service/pricing), you can get a complete list of features by subscription level.

If, at any time during your monthly subscription with Elastic Cloud, you decide you need features on a higher subscription level, you can easily make changes. You can both upgrade to a higher subscription level, or downgrade to a lower one.

To change your subscription level:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Select the user icon on the header bar and select **Billing** from the menu.
3. On the **Overview** page, select **Update subscription**.
4. Choose a new subscription level.
5. Save your changes.

::::{important}
Changing to a higher subscription level takes place immediately. Moving to a lower subscription level takes effect 30 days after you most recently changed to a higher subscription level; in the interim, you pay the current rate. If you haven’t performed a self-service change in the past 30 days, then the change to the lower subscription level is immediate.
::::


::::{important}
Customers on the prepaid consumption billing model can change their subscription level in the **Billing subscription** page. Cloud Standard is not available for customers on the prepaid consumption billing model.
::::



## Feature usage notifications [ec_feature_usage_notifications]

If you try to change your subscription to a lower level, but you are using features that belong either to your current level or to a higher one, you need to make some changes before you can proceed, as described in **review required feature changes** link.

This overview shows you:

* Any features in use that belong to a higher subscription level, grouped by deployment
* Which subscription level you should change to in order to keep those features

You can [change your subscription level](../../../deploy-manage/cloud-organization/billing/manage-subscription.md) to the recommended level, or stop using the features that belong to a higher level. In the following list, you can find the features we are tracking and the relevant instructions to remove them from your deployments:

`Machine learning`
:   Edit your deployment to disable [machine learning](/explore-analyze/machine-learning/anomaly-detection.md).

`Searchable snapshots`
:   Edit your deployment index management policies to disable the frozen tier that is using [searchable snapshots](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), or set up your cold tier to not mount indices from a searchable snapshot.

`JDBC/ODBC clients`
:   Make sure that there are no applications that use the SQL [JDBC](/explore-analyze/query-filter/languages/sql-jdbc.md) or [ODBC](/explore-analyze/query-filter/languages/sql-odbc.md) clients.

`Field-level or document-level security`
:   Remove any user role configurations based on field or document access [through the API](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) or the Kibana Roles page.

::::{note}
After you have made your changes to the deployment, it can take up to one hour to clear the notification banner.
::::


