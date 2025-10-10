---
navigation_title: Troubleshoot
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/get-support-help.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/troubleshooting-and-faqs.html
  - https://www.elastic.co/guide/en/cloud/current/ec-get-help.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-get-help.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-help.html
products:
  - id: elastic-stack
  - id: cloud-hosted
  - id: cloud-enterprise
description: Troubleshooting resources and guidance for Elastic products including
  Elasticsearch, Kibana, Observability, Security, and deployment platforms. Find
  solutions and get support.
---

# Troubleshooting

This section contains troubleshooting resources and guidance to help you resolve issues with Elastic products.

If you can't find your issue here, explore the [additional resources](#troubleshoot-additional-resources) or [contact us](#contact-us).

:::{note}
You might need to review troubleshooting content for more than one product or topic area. Most Elastic deployments use multiple components from the [Elastic Stack](/get-started/the-stack.md), plus a deployment orchestrator. Check all topics relevant to your infrastructure.
:::

* [{{es}}](/troubleshoot/elasticsearch.md)
* [{{kib}}](/troubleshoot/kibana.md)
* [Elastic {{observability}}](/troubleshoot/observability.md)
* [{{elastic-sec}}](/troubleshoot/security.md)
* [Ingest tools](/troubleshoot/ingest.md)
* [{{ecloud}}](/troubleshoot/deployments/elastic-cloud.md)
* [{{ece}}](/troubleshoot/deployments/cloud-enterprise/cloud-enterprise.md)
* [{{eck}}](/troubleshoot/deployments/cloud-on-k8s/kubernetes.md)

## Additional resources [troubleshoot-additional-resources]

* Find additional troubleshooting articles in the [Elastic Support Portal](https://support.elastic.co/).

  You can access the Support Portal using your {{ecloud}} account. {{ecloud}} accounts are free and do not require an active subscription.

* Visit the [Elastic community forums](https://discuss.elastic.co) to get answers from experts in the community, including Elastic team members.

* Use the top bar to search all docs for your issue. Some troubleshooting content appears in other sections of the Elastic documentation.


## Contact us [contact-us]

If you have an [Elastic subscription](https://www.elastic.co/pricing), you can contact Elastic support for assistance. You can reach us in the following ways:

* **Through the [Elastic Support Portal](https://support.elastic.co/):** The Elastic Support Portal is the central place where you can access all of your cases, subscriptions, and licenses. Within a few hours after subscribing, you'll receive an email with instructions on how to log in to the Support Portal, where you can track both current and archived cases.

  You can access the portal [directly](https://support.elastic.co/) or by clicking the life preserver icon on any Elastic Cloud page.


* **By email:** [support@elastic.co](mailto:support@elastic.co)

  :::{tip}
  If you contact us by email, use the email address you registered with so we can help you more quickly. If your registered email is a distribution list, you can register a second email address with us. Just open a case to let us know the name and email address you want to add.
  :::

  :::{warning}
  All cases opened by email default to a normal severity level. For incidents, open a case through the [Elastic Support Portal](https://support.elastic.co/) and select the [appropriate severity](https://www.elastic.co/support/welcome#what-to-say-in-a-case).
  :::

## Working with support [troubleshoot-work-with-support]

When you open a support case:

* Describe the problem with context about the situation and its business severity, as described in [What should I say in my case?](https://www.elastic.co/support/welcome#what-to-say-in-a-case).

  * If an error message was encountered, include the full error message and the timezone-designated timestamp of when the problem occurred.

  * If the problem is UI-related and can't be replicated using API calls, pull a [browser network log](https://www.elastic.co/blog/generating-browser-har-file-kibana-troubleshooting). 

* Upload the related product's diagnostics and debug logs:

  * If hosting on {{serverless-full}} or {{ech}}, Support can pull diagnostics on your behalf as long as you include resource IDs:
    
    * {{serverless-full}} Project ID or {{kib}} URL
    * {{ech}} Deployment ID or {{kib}} URL

  * If hosting on {{ece}} or {{eck}}:

    * {{ece}} [diagnostic](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md) flagging `--deployments` as applicable
    * {{eck}} [diagnostic](/troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md)

  * If self-hosting:

    * {{es}} [diagnostic](/troubleshoot/elasticsearch/diagnostic.md) and [debug logs](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md)
    * {{kib}} and {{fleet}} [diagnostic](/troubleshoot/kibana/capturing-diagnostics.md) and [debug logs](/deploy-manage/monitor/logging-configuration/kibana-log-levels.md)
    
    * Ingest tools:

      * {{ls}} [diagnostic](/troubleshoot/ingest/logstash/diagnostic.md) and [debug logs](logstash://reference/logging.md)
      * {{agent}} [diagnostic](https://www.elastic.co/docs/troubleshoot/ingest/fleet/common-problems#trb-collect-agent-diagnostics) and [debug logs](https://www.elastic.co/docs/reference/fleet/monitor-elastic-agent#change-logging-level)
  

  :::{tip}
  The {{es}} cluster maintains an advanced task management system, while other products use a simpler polling mechanism. Because of this, some issues appear only in their start-up debug logs. Later logs may note only that the subprocess has stopped or that it has not changed state from an earlier error.
  :::

  :::{warning}
  Diagnostics and logs mainly emit product metadata and settings, but they may expose sensitive data which needs to be redacted before being shared outside of your organization. Refer to each product's diagnostics page for information on sanitizing output.
  :::

