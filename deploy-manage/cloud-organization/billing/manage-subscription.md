---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/general-check-subscription.html
  - https://www.elastic.co/guide/en/cloud/current/ec-subscription-overview.html
  - https://www.elastic.co/guide/en/cloud/current/ec-select-subscription-level.html
  - https://www.elastic.co/guide/en/cloud/current/ec-licensing.html
applies_to:
  deployment:
    ess: all
  serverless: all
---

# Manage your subscription

When you decide to add your credit card and become a paying customer, you can choose a subscription level. 

Depending on whether you're using {{ech}} deployment or {{serverless-full}} projects, your subscription level might dictate what features you can access or what level of support you receive. On the following pricing pages, you can review additional details about what you get at each subscription level:

* [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service/pricing)
* [{{serverless-full}}](https://www.elastic.co/pricing/serverless-search)

You can find more details about your subscription in the [Billing overview page](https://cloud.elastic.co/billing/overview), in the **Subscription level** section. 


## Change your subscription level [ec-select-subscription-level]

If, at any time during your monthly subscription with {{ecloud}}, you decide you need to upgrade to a higher subscription level, you can easily make changes. You can both upgrade to a higher subscription level, or downgrade to a lower one.

To change your subscription level:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Select the user icon on the header bar and select **Billing** from the menu.
3. On the **Overview** page, select **Update subscription**.
4. Choose a new subscription level.
5. Save your changes.

::::{important}
* Changing to a higher subscription level takes place immediately. Moving to a lower subscription level takes effect 30 days after you most recently changed to a higher subscription level. In the interim, you pay the current rate. If you haven’t performed a self-service change in the past 30 days, then the change to the lower subscription level is immediate.
* **Cloud Standard** is not available for customers on the prepaid consumption billing model.
::::

### Feature usage notifications [ec_feature_usage_notifications]

:::{applies_to}
:hosted: all
:::

If you try to change your subscription to a lower level, but you are using features that belong either to your current level or to a higher one, you need to make some changes before you can proceed, as described in **Review required feature changes**.

This overview shows you the following details:

* Any features in use that belong to a higher subscription level, grouped by deployment
* Which subscription level you should change to in order to keep those features

You can [change your subscription level](/deploy-manage/cloud-organization/billing/manage-subscription.md) to the recommended level, or stop using the features that belong to a higher level. In the following list, you can find the features we are tracking and the instructions to remove them from your deployments:

`Machine learning`
:   Edit your deployment to disable [machine learning](/explore-analyze/machine-learning.md).

`Searchable snapshots`
:   Edit your deployment index management policies to disable the frozen tier that is using [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), or set up your cold tier to not mount indices from a searchable snapshot.

`JDBC/ODBC clients`
:   Make sure that there are no applications that use the SQL [JDBC](/explore-analyze/query-filter/languages/sql-jdbc.md) or [ODBC](/explore-analyze/query-filter/languages/sql-odbc.md) clients.

`Field-level or document-level security`
:   Remove any user role configurations based on field or document access [through the API](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) or the Kibana [Roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) page.

::::{note}
After you have made your changes to the deployment, it can take up to one hour to clear the notification banner.
::::
