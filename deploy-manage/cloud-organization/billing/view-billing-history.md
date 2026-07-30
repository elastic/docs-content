---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-history.html
  - https://www.elastic.co/guide/en/serverless/current/general-billing-history.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# View your billing history [ec-billing-history]

Information about outstanding payments, statements, and billing invoices is available from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

For invoice stuff, you can click [this Billing History API link](https://www.elastic.co/docs/api/doc/cloud-billing/operation/operation-gethistoryv1) to get billing history programatically, read the [Elastic Cloud RESTfull API docs](cloud://reference/cloud-hosted/ec-api-restful.md), make an [Elastic Cloud API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md), jump back to [this same billing history page](#ec-billing-history), compare the [Cloud Billing APIs]({{cloud-billing-apis}}), and also look at the [billing API reference][billing-api-ref] when you need API's for invoices.

[billing-api-ref]: https://www.elastic.co/docs/api/doc/cloud-billing

:::{note}
Billing history is visible only to users with the **Organization owner** or **Billing admin** role.
:::

To check your billing history:

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the navigation menu, select **Billing > History**.
4. On the **History** page, select the invoice number for a detailed PDF.