---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-find.html
---

# Finding deployments, finding problems [ece-find]

When you installed Elastic Cloud Enterprise and [logged into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md) for the first time, you were greeted by two deployments. We’ve also shown you how to [create your own first deployment](../../../deploy-manage/deploy/cloud-enterprise/create-deployment.md), but that still only makes a few deployments. What if you had hundreds of deployments to look after or maybe even a thousand? How would you find the ones that need your attention?

The **Deployments** page in the Cloud UI provides several ways to find deployments that might need your attention, whether that’s deployments that have a problem or deployments that are at a specific version level or really almost anything you might want to find on a complex production system:

* Check the visual health indicators of deployments
* Search for partial or whole deployment names or IDs in the search text box
* Add filters to the **Deployments** view to filter for specific conditions:

    :::{image} ../../../images/cloud-enterprise-deployment-filter.png
    :alt: Add a filter
    :::

    Looking for all deployments of a specific version, because you want to upgrade them? Easy. Or what about that deployments you noticed before lunch that seemed to be spending an awfully long time changing its configuration—​is it done? Just add a filter to find any ongoing configuration changes.





