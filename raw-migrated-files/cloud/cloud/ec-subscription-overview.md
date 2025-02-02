# Check your subscription overview [ec-subscription-overview]

You can find more details about your subscription in the **Billing overview** page. To navigate there:

1. Log in to the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Select the user icon on the header bar and select **Billing** from the menu.
3. Go to the **Overview** page.

In the first section, you can find your subscription level, as well as your contract type: monthly or annual. Here you can [change your subscription level](../../../deploy-manage/cloud-organization/billing/manage-subscription.md).

In the second section, you can check the date when your next invoice or usage statement will be issued.

::::{note} 
Customers on the prepaid consumption model can see their subscription overview in the **Billing subscription** page, and high level details about their usage in the **Billing overview** page.
::::



## View account details [ec-account-details] 

If you have an annual subscription billed using the prepaid consumption model, you can check details of your available credits in the **Account details** section.

When you buy ECU to pay for your Elasticsearch Service usage, they are contracted through a purchase order consisting of one or more order lines. Each order line has a number of attributes:

Credits
:   The quantity of Elastic Consumption Units purchased through an order line and used to cover your consumption.

Usage
:   Your Elasticsearch Service resource consumption quantified in ECU. Resources consumed include capacity (RAM-hours), data transfer (data inter-node and data out), and snapshot storage (storage size or snapshot API calls). These three consumption types are generally known as [billing dimensions](../../../deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md).

Remaining balance
:   The quantity of ECU remaining on an order line. This is calculated as the original amount of credits purchased minus the credits used so far.

Start date
:   The date when the credits belonging to an order line can begin to be used to offset your consumption.

Expiration date
:   The date until which the purchased credits are valid and can be used to offset consumption. After this date, any unused credits are forfeited.

Status
:   An order line can have one of the following statuses:

    * Active: this means that the start date is in the past and the expiration date is in the future.
    * Expired: The expiration date for the line item is before the current date.
    * Future: The start date for the line item is after the current date.


List unit price
:   The list price paid for one ECU, in the transacted currency. This price does not include any discounts.

Discount rate
:   The discount percentage applied to the list unit price of one ECU.

Paid amount
:   The currency cost of the purchased credits. This is calculated as **Credits x List unit price x (100 - Discount rate)/100**.

