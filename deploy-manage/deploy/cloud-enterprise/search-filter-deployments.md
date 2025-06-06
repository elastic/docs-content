---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-find.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Search and filter deployments [ece-find]

When you installed {{ece}} and [logged into the Cloud UI](log-into-cloud-ui.md) for the first time, you were greeted by two deployments. We’ve also shown you how to [create your own first deployment](create-deployment.md), but that still only makes a few deployments. What if you had hundreds of deployments to look after or maybe even a thousand? How would you find the ones that need your attention?

The **Deployments** page in the Cloud UI provides several ways to find deployments that might need your attention, whether that’s deployments that have a problem or deployments that are at a specific version level or really almost anything you might want to find on a complex production system:

* Check the visual health indicators of deployments
* Search for partial or whole deployment names or IDs in the search text box
* Add filters to the **Deployments** view to filter for specific conditions:

    :::{image} /deploy-manage/images/cloud-enterprise-deployment-filter.png
    :alt: Add a filter
    :::

    Need to find all deployments running a specific version for an upgrade? Simply apply a filter. Or perhaps you noticed a deployment that was taking an unusually long time to apply configuration changes? Check its status by filtering for ongoing configuration updates.




