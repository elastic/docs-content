---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-ecu.html
applies_to:
  deployment:
    ess: all
  serverless: all
---

# Elastic Consumption Units [ec-billing-ecu]

All {{ecloud}} usage is metered and billed in Elastic Consumption Units (ECU). An Elastic Consumption Unit is a unit of measure for {{ecloud}} resources (capacity, data transfer, or snapshot storage).

The nominal value of one Elastic Consumption Unit is $1.00. You can use our [{{ech}} pricing calculator](https://cloud.elastic.co/pricing) or our [public pricing table](https://ela.st/esspricelist) to estimate your costs in USD, and then apply the conversion rate of 1 ECU = $1.00 to calculate the ECU equivalent.

Your monthly usage statement is issued in ECU, though it also includes the currency equivalent of your consumption. The **Usage** page in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) also shows usage information in ECU.

## Contractual information and quoting [ec_contractual_information_and_quoting]

When you sign a prepaid consumption contract, you are purchasing Elastic Consumption Units which can be used to cover your {{ecloud}} usage throughout your contract period.

Elastic Consumption Units measure the value of your usage, as opposed to measuring the cost of the purchase, which may vary based on currency rate and discount.

Refer to our [Billing FAQ](/deploy-manage/cloud-organization/billing/billing-faq.md) for more details about prepaid consumption.

## View available credits

If you have an annual subscription billed using the prepaid consumption model, you can check details of your available credits on the [Billing overview page](https://cloud.elastic.co/billing/overview), in the **Available credits** section.

When you buy ECU to pay for your {{ecloud}} usage, they are contracted through a purchase order consisting of one or more order lines. Each order line has a number of attributes:

Credits
:   The quantity of Elastic Consumption Units purchased through an order line and used to cover your consumption.

Usage
:   Your {{ecloud}} resource consumption quantified in ECU. Resources consumed include capacity (RAM-hours), data transfer (data inter-node and data out), and snapshot storage (storage size or snapshot API calls). These three consumption types are generally known as [billing dimensions](../../../deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md).

Remaining balance
:   The quantity of ECU remaining on an order line. This is calculated as the original amount of credits purchased minus the credits used so far.

Start date
:   The date when the credits belonging to an order line can begin to be used to offset your consumption.

Expiration date
:   The date until which the purchased credits are valid and can be used to offset consumption. After this date, any unused credits are forfeited.

Status
:   An order line can have one of the following statuses:

    * **Active**: this means that the start date is in the past and the expiration date is in the future.
    * **Expired**: The expiration date for the line item is before the current date.
    * **Future**: The start date for the line item is after the current date.


List unit price
:   The list price paid for one ECU, in the transacted currency. This price does not include any discounts.

Discount rate
:   The discount percentage applied to the list unit price of one ECU.

Paid amount
:   The currency cost of the purchased credits. This is calculated as **Credits x List unit price x (100 - Discount rate)/100**.