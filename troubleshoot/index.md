---
navigation_title: "Troubleshoot"
mapped_urls:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/get-support-help.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/troubleshooting-and-faqs.html
  - https://www.elastic.co/guide/en/cloud/current/ec-get-help.html
---

# Troubleshooting


% Scope notes: - Match new content type; TOC entry TBD - consider splitting out subsections?

% see https://docs.elastic.dev/content-architecture/content-type/troubleshooting/entrypoint

% TODO pull in product-specific tips etc. from other TS sections


:::{admonition} WIP
⚠️ **This section is a work in progress.** ⚠️

The documentation team is actively working on the pages in this section.
:::

This section contains information about resolving common issues you might encounter with Elastic products, as well as troubleshooting resources and guidance.

If you can't find your issue here, explore the [additional resources](#troubleshoot-additional-resources) or [contact us](#contact-us).

:::{note} 
You might need to review the troubleshooting content for more than one product or topic area. In most Elastic deployments, you use multiple components from the [Elastic Stack](/get-started/the-stack.md), plus software to orchestrate your deployment. Because these components communicate with each other, you might see errors in one product that originate from another part of the stack, or from your deployment infrastructure. 
:::

* [{{es}}](/troubleshoot/elasticsearch/elasticsearch.md)
* [{{kib}}](/troubleshoot/kibana.md)
* [Elastic {{observability}}](/troubleshoot/observability.md)
* [{{elastic-sec}}](/troubleshoot/security.md)
* [Ingest tools](/troubleshoot/ingest.md)
* [{{ecloud}}](/troubleshoot/deployments/elastic-cloud.md)
* [{{ece}}](/troubleshoot/deployments/cloud-enterprise/cloud-enterprise.md)
* [{{eck}}](/troubleshoot/deployments/cloud-on-k8s/kubernetes.md)

## Error reference 
:::{admonition} WIP
Work in progress
:::

## Additional resources [troubleshoot-additional-resources]

* Find additional troubleshooting articles in the [Elastic Support Portal](https://support.elastic.co/).

  You can access the Support Portal using your {{ecloud}} account. {{ecloud}} accounts are free and do not require an active subscription.

* Visit the [Elastic community forums](https://discuss.elastic.co) to get answers from experts in the community, including Elastic team members.

* Use the top search bar to search all our docs for your issue. Some troubleshooting content is contained in other sections of the Elastic documentation.


## Contact us [contact-us]

If you have an [Elastic subscription](https://www.elastic.co/pricing), you can contact Elastic support for assistance. You can reach us in the following ways: 

* **Through the [Elastic Support Portal](https://support.elastic.co/):** The Elastic Support Portal is the central place where you can access all of your cases, subscriptions, and licenses. Within a few hours after subscribing, you receive an email with instructions on how to log in to the Support Portal, where you can track both current and archived cases.

  You can access the portal [directly](https://support.elastic.co/) or by clicking the life preserver icon on any Elastic Cloud page.


* **By email:** [support@elastic.co](mailto:support@elastic.co)

  :::{tip}
  If you contact us by email, use the email address you registered with so we can help you more quickly. If you are using a distribution list as your registered email, you can also register a second email address with us. Just open a case to let us know the name and email address you want to add.
  :::

## Working with support [troubleshoot-work-with-support]

Try these tips when opening a support case:

* Include the deployment ID that you want help with, especially if you have several deployments. 

  You can find the deployment ID on the overview page for your cluster in the {{ecloud}} Console.

* Describe the problem. Include any relevant details, including error messages you encountered, dates and times when the problem occurred, or anything else you think might be helpful.

* Upload any pertinent files.
