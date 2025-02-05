---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-models.html
applies:
  hosted: all
  serverless: all
---

# Billing models [ec-billing-models]

You can be billed for {{ecloud}} using one of the following billing models:

* [Monthly, billed by Elastic](#ec-monthly-direct)
* [Monthly, billed through a marketplace](#ec-monthly-marketplace)
* [Prepaid](#ec-prepaid-consumption)

Regardless of your billing model, all {{ecloud}} usage is metered and billed in [Elastic Consumption Units (ECU)](/deploy-manage/cloud-organization/billing/ecu.md).

## Monthly, billed by Elastic [ec-monthly-direct] 

When you sign up for {{ecloud}} by [adding your credit card details](/deploy-manage/cloud-organization/billing/add-billing-details.md) in the {{ecloud}} Console, you are billed on a monthly basis.

At each billing cycle, on the first of each month, all usage for the previous month is aggregated, invoiced, and charged in arrears on the credit card used to sign up for the service.

All usage is expressed and charged in US dollars only.

Refer to our [Billing FAQ](/deploy-manage/cloud-organization/billing/billing-faq.md) for more details about monthly invoicing.

## Monthly, billed through a marketplace [ec-monthly-marketplace] 

You can sign up for {{ecloud}} [from a marketplace](/deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md). In this case, all usage is reported hourly to the marketplace.

At the marketplace’s billing cycle, all usage is aggregated and charged as part of your cloud provider bill.

{{ecloud}} usage appears as a single invoice line with the total amount charged. For a detailed breakdown of your usage, visit the [Usage page](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md) in the {{ecloud}} Console.

::::{note} 
Marketplaces typically invoice you in arrears on the first of each month. There are exceptions, however, such as in the case of the [GCP billing cycle](https://cloud.google.com/billing/docs/how-to/billing-cycle).
::::

## Prepaid consumption [ec-prepaid-consumption] 

All new and renewing {{ecloud}} annual customers are automatically enrolled into the prepaid consumption billing model.

Prepaid consumption is built on four key concepts:

Consumption-based billing
:   You pay for the actual product used, regardless of the application or use case. This is different from subscription-based billing models where customers pay a flat fee restricted by usage quotas, or one-time upfront payment billing models such as those used for on-prem software licenses.

    You can purchase credits for a single or multi-year contract. Consumption is on demand, and every month we deduct from your balance based on your usage and contract terms. This allows you to seamlessly expand your usage to the full extent of your requirements and available budget, without any quotas or restrictions.

Resource-based pricing
:   You are charged for the actual computing resources you use: capacity (consisting of RAM and CPU plus disk allowance), data transfer, and snapshot storage. This normalizes billing dimensions across different use cases (for example, the number of agents for APM, the number of hosts for Security, the volume of data ingest for Observability, and so on) making it easy to compare and aggregate costs.

Elastic Consumption Unit (ECU)
:   An ECU is a unit of aggregate consumption across multiple resources over time.

    Each type of computing resource (capacity, data transfer, and snapshot) that you consume has its own unit of measure. For example, capacity is measured in GB-hour, data transfer in GB, snapshot storage in GB-month and snapshot API requests in thousands of requests.

    In order to aggregate consumption across different resource types, all resources are priced in ECU. ECU has a fixed exchange rate to fiat currency of 1 ECU = $1.00.

    Check [Elastic Consumption Units](/deploy-manage/cloud-organization/billing/ecu.md) for more details.


Credits
:   Credits are used to pay for the metered consumption. They are expressed in ECU, and can be purchased at a discount, and in different currencies. The list price of 1 ECU is $1.00, but it can be discounted or converted to a different currency for invoicing purposes. Credits have both a start date and an expiration date after which they will be forfeited.

Based on these four key concepts, the prepaid consumption lifecycle is as follows:

1. You purchase credits expressed in ECU, typically at a discount.
2. You begin using {{ecloud}} resources.
3. At every billing cycle (which takes place on the first of each month), the previous month's usage, expressed in ECU, is deducted from your ECU balance.
4. If your ECU balance is depleted before the credit expiration date, you are invoiced for on-demand usage in arrears at list price. On-demand usage is expressed in ECU, and is converted to currency amounts for invoicing purposes.¹
5. At the end of the contract period, any credits remaining in your balance are forfeited.
6. During the contract period, you can purchase additional credits at any time (as an add-on). This can be done with the same discount as the original purchase. Credits purchased through an add-on have the same expiration as the original purchase.²

¹ When you renew your contract or commit to a multi-year contract, any on-demand usage incurred in the years other than the last are billed with the same discount as the original purchase.

² Purchasing credits through early renewals, or through add-ons with different expiration dates will be available in the near future.

::::{note} 
Existing annual+overages customers will be able to switch to prepaid consumption when they renew or sign a new contract. Existing manual burndown customers will be migrated gradually to prepaid consumption in the near future. Exceptions apply.
::::