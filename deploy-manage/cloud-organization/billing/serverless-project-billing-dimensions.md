---
navigation_title: Serverless billing dimensions
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/general-serverless-billing.html
applies_to:
  serverless: all
products:
  - id: cloud-serverless
---

# Serverless project billing dimensions [general-serverless-billing]

{{serverless-full}} billing is based on your usage across these dimensions:

* [Offerings](#offerings)
* [Add-ons](#add-ons)

Specific prices can be found in the [Cloud Pricing Table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless).

## Offerings [offerings] 

To learn about billing dimensions for specific offerings, refer to:

* [](elasticsearch-billing-dimensions.md)
* [](elastic-observability-billing-dimensions.md)
* [](security-billing-dimensions.md)


## Add-ons [add-ons] 


### Data out [general-serverless-billing-data-out] 

*Data out* accounts for all of the traffic coming out of a serverless project. This includes search results, as well as monitoring data sent from the project. The same rate applies regardless of the destination of the data, whether to the internet, another region, or a cloud provider account in the same region. Data coming out of the project through AWS PrivateLink, GCP Private Service Connect, or Azure Private Link is also considered data out.


### Support [general-serverless-billing-support] 

If your subscription level is Standard, there is no separate charge for Support reflected on your bill. If your subscription level is Gold, Platinum, or Enterprise, a charge is made for Support as a percentage (%) of the ECUs. To find out more about our support levels, go to [https://www.elastic.co/support](https://www.elastic.co/support).

