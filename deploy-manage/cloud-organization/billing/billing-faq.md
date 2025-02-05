---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-billing.html
---

# Billing FAQ [ec-faq-billing]

This frequently-asked-questions list answers some of your more common questions about Elasticsearch Service billing.

**General billing questions**

* [Is there a way for me to estimate how much Elasticsearch Service will cost?](#faq-cost)
* [Where can I find a detailed view of my consumption?](#faq-consumption)
* [How do I view previous receipts and billing history?](#faq-history)
* [How can I change who receives receipts and billing notifications?](#faq-notify)
* [What are the available payment methods on Elasticsearch Service?](#faq-payment)
* [Who can I contact for more information?](#faq-contact)
* [Why is my credit card charged?](#faq-charge)
* [When is my credit card charged?](#faq-when)
* [Why is my credit card charged if I canceled my trial?](#faq-whystillcharged)
* [What is the cancellation policy for monthly subscriptions?](#faq-cancelpolicy)
* [Why am I being charged if I don’t use any of my deployments?](#faq-chargednotusing)
* [How can I delete my Elastic Cloud account?](#faq-deleteaccount)
* [Can I get a refund?](#faq-refund)
* [What is included in my paid Elasticsearch Service deployment?](#faq-included)
* [What are the data transfer and storage charges and how can I control them?](#faq-dts)
* [What taxes will be applied on my invoice?](#faq-taxes)

**Prepaid consumption questions**

* [What purchasing channels can be used for prepaid consumption credits?](#faq-channels)
* [Can I migrate my monthly account to the prepaid consumption model?](#faq-migration)
* [What happens if my credits are depleted mid-year?](#faq-depletion)
* [If I have a multi-year contract and I run out of balance, can I draw against the next year’s credits?](#faq-draw-credits)
* [If my user login is invited to a different organization, what happens to the prepaid credits for the current organization?](#faq-organizations)
* [What kind of subscription level can a customer have on the prepaid consumption model?](#faq-level)
* [Where can I follow the remaining balance and usage?](#faq-usage)
* [How will I know that I am running out of credits?](#faq-notification)
* [How can I pay for on-demand usage?](#faq-on-demand)
* [What happens when a prepaid consumption contract expires and is not renewed?](#faq-lapse)
* [If credits are purchased through multiple orders, which ones get used first?](#faq-credits)
* [What do the prepaid credits cover?](#faq-prepaidcover)


## General billing FAQ [ec-faq-billing-general]

$$$faq-cost$$$Is there a way for me to estimate how much Elasticsearch Service will cost?
:   Yes, there is: Try our [Elasticsearch Service Pricing Calculator](https://www.elastic.co/cloud/elasticsearch-service/pricing?page=docs&placement=docs-body). You can also use the  [Elasticsearch Service price list](https://ela.st/esspricelist).

$$$faq-consumption$$$Where can I find a detailed view of my consumption?
:   To make it easy to track the ongoing cost of Elasticsearch Service, we’ve added line items to the downloadable [invoices](https://cloud.elastic.co/billing/overview?page=docs&placement=docs-body).

    Example invoice
    :   :::{image} ../../../images/cloud-ec-bill-example-new.png
    :alt: Example invoice
    :::

    Additionally, on the Elasticsearch Service [Usage analysis](https://cloud.elastic.co/billing/usage?page=docs&placement=docs-body) page, the **month-to-date usage** tile shows accrued costs and can help you to better estimate the next charge amount.


$$$faq-history$$$How do I view previous receipts and billing history?
:   Check the [billing history](https://cloud.elastic.co/billing/history?page=docs&placement=docs-body), where you can view and download receipts for all previous charges.

$$$faq-notify$$$How can I change who receives receipts and billing notifications?
:   The account owner can change who receives receipts and billing notifications by changing the [email details](https://cloud.elastic.co/account/contacts?page=docs&placement=docs-body).

$$$faq-payment$$$What are the available payment methods on Elasticsearch Service?
:   For month-to-month payments only credit cards are accepted. We also allow payments by bank transfer for annual subscriptions.

$$$faq-contact$$$Who can I contact for more information?
:   If you have any further questions about your credit card statement, billing, or receipts, please send an email to `ar@elastic.co` or open a [Support case](../../../troubleshoot/troubleshoot/index.md) using the *Billing issue* category.

$$$faq-charge$$$Why is my credit card charged?
:   If you are on a monthly plan, the charge is a recurring fee for using our hosted Elasticsearch Service. The fee is normally charged at the start of each month, but it can also be charged at other times during the month. If a charge is unsuccessful, we will try to charge your card again at a later date.

$$$faq-when$$$When is my credit card charged?
:   You are billed on the first day of each month for usage in the prior month.

$$$faq-whystillcharged$$$Why is my credit card charged if I canceled my trial?
:   If you add a credit card to your Elastic Cloud account at any time during the trial period, the trial is converted to a paid subscription. You then have to pay for any expense incurred by your deployment beginning when the credit card was added. If you delete your deployment at a later date, you will still be invoiced for any usage that occurs between the conversion date and the deployment deletion date.

$$$faq-cancelpolicy$$$What is the cancellation policy for monthly subscriptions?
:   There are no cancellation or termination fees for monthly subscriptions. If the service is no longer needed, you can spin down all of your deployments. Usage for that month will be billed at the end of the month in your final bill.

$$$faq-chargednotusing$$$Why am I being charged if I don’t use any of my deployments?
:   Even if you have no activity on your account and you haven’t logged into the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body), your active deployments still incur costs that we need to charge you for. To avoid being charged for active but unused deployments, you can simply delete them. Your account will stay active with no charges, and you can always spin up more capacity when you need it.

$$$faq-deleteaccount$$$How can I delete my Elastic Cloud account?
:   To have your account removed, you can contact support through the Elasticsearch Service [Support form](https://cloud.elastic.co/support?page=docs&placement=docs-body) or use one of these [alternative contact methods](../../../troubleshoot/troubleshoot/index.md). For details about our data erasure policy, check [Privacy Rights and Choices](https://www.elastic.co/legal/privacy-statement#privacy-rights-and-choices?page=docs&placement=docs-body) in our General Privacy Statement.

$$$faq-refund$$$Can I get a refund?
:   Charges are non-refundable, but once you delete a deployment we’ll stop charging you for that deployment immediately. You only pay for what you use and you can stop using the service at any time. For any special considerations warranting a potential refund, please use the Elasticsearch Service Console [Support form](https://cloud.elastic.co/support?page=docs&placement=docs-body) to open a support case and select *Billing issue* as the category. To ensure quick processing, be sure to provide detail about the reasons for the refund request as well as other matters pertaining to the issue. For other ways to open a Support case, check [Contact us](../../../troubleshoot/troubleshoot/index.md).

$$$faq-included$$$What is included in my paid Elasticsearch Service deployment?
:   All subscription tiers for the Elasticsearch Service include the following free allowance:

    * Free 1GB RAM Kibana instance
    * Free 1GB RAM Machine Learning node
    * Free 2GB RAM Enterprise Search instance
    * Free 1GB RAM APM server
    * A free allowance for [data transfer and snapshot storage costs](#faq-dts)

    Note that if you go above the free tier of Kibana/ML/APM (for example, a 2GB Kibana instance), you will be charged in full for the size of that instance.


$$$faq-dts$$$What are the data transfer and storage charges and how can I control them?
:   Read about our [usage-based billing dimensions](cloud-hosted-deployment-billing-dimensions.md).

$$$faq-taxes$$$What taxes will be applied on my invoice?
:   Customers within the United States, and US territories, will be billed from Elasticsearch Inc., based out of the United States. The US Sales Tax rate will be based on the SaaS tax rates in the local jurisdiction (state/county/city) of the billing address of your subscription.

    Customers outside the United States, will be billed from Elasticsearch BV, based out of the Netherlands. Customers with a billing address in countries with applicable EU VAT will have VAT applied based on their country and status as a business or private customer. Elastic collects VAT Numbers associated with EU VAT to determine your status as a business (B2B) or private / non-business customer (B2C), as this is a key factor to determine Elastic’s liability to charge VAT on your subscription. To update your VAT Number follow the instructions provided in [Add your billing details](https://www.elastic.co/guide/en/cloud/current/ec-billing-details.html). Customers located in countries without EU VAT will not be applied VAT on their invoices.



## Prepaid consumption FAQ [ec-faq-consumption]

The following section applies to annual contracts that are billed on the prepaid consumption billing model.

$$$faq-channels$$$What purchasing channels can be used for prepaid consumption credits?
:   The prepaid consumption billing model is currently only available for Elastic Direct customers - customers who are purchasing directly from Elastic. This offering may expand to marketplace customers in the future.

$$$faq-migration$$$Can I migrate my monthly account to the prepaid consumption model?
:   Yes, if you have a monthly Elasticsearch Service account, you can [contact us](https://www.elastic.co/cloud/contact) to migrate to prepaid consumption.

$$$faq-depletion$$$What happens if I run out of credits?
:   If your credit balance is entirely consumed while you have an active contract, you can continue to use Elastic Cloud and will receive invoices for the additional on-demand usage.

    * By default, the on-demand usage is billed at the list price in ECU, and invoiced at the currency equivalent.
    * If you have future credit line items that are not active yet, the on-demand usage is billed at the rate of the last active credit line item, using the same payment method. Any discounts that applied to that last active credit line item also apply to the on-demand usage until the next line item becomes active.


$$$faq-draw-credits$$$If I have a multi-year contract and I run out of balance, can I draw against the next year’s credits?
:   No, this option is currently not available.

$$$faq-organizations$$$If my user login is invited to a different organization, what happens to the prepaid credits for the current organization?
:   Prepaid credits are always assigned to a given organization and NOT to a specific user account. If a user is invited to a different organization, they will not carry the prepaid credits to the new organization.

$$$faq-level$$$What kind of subscription level can a customer have on the prepaid consumption model?
:   When the credits are first provisioned, your Cloud account will be set to Enterprise. You can [change your subscription level](manage-subscription.md) at any time. We are offering only Gold, Platinum, and Enterprise support levels for prepaid consumption customers. Standard is not offered for prepaid consumption.

$$$faq-usage$$$Where can I follow the remaining balance and usage?
:   The current usage and remaining balance can be found in the [Usage](monitor-analyze-usage.md) page. You will also receive monthly usage statements that are published in the [Billing history](view-billing-history.md) page.

$$$faq-notification$$$How will I know that I am running out of credits?
:   Your account billing contacts and the members of your organization will receive email notifications when your credit balance falls below 33%, 25%, and 16% of credits remaining.

$$$faq-on-demand$$$How can I pay for on-demand usage?
:   We only support PO (invoicing) for on-demand usage, for prepaid consumption customers. The issued invoices include tax.

$$$faq-lapse$$$What happens when a prepaid consumption contract expires and is not renewed?
:   Your Elastic Cloud account will automatically change into a monthly account, paid through PO (invoicing). You will continue to incur costs, as we will not delete any of your deployments. You will not benefit from any discount because monthly customers are billed at list prices.  To switch your account to credit card payment, you must first send an email to `CloudBillingOps@elastic.co` to indicate that this is your new preferred payment method. Once your email processed, Elastic will inform you that you can update your credit card information accordingly.

$$$faq-credits$$$If credits are purchased through multiple orders, which ones get used first?
:   Credits get consumed in the order of expiration (first expired - first used). If two or more order lines have the same expiration date, the one with the highest discount is consumed first. If there are two or more order lines with the same discount, then the one with the lower balance is consumed first.

$$$faq-prepaidcover$$$What do the prepaid credits cover?
:   If you have an annual contract, your prepaid credits are used to cover all usage, including capacity, data transfer, and snapshot storage.
