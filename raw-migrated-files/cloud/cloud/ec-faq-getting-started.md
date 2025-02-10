# Elasticsearch Service FAQ [ec-faq-getting-started]

This frequently-asked-questions list helps you with common questions while you get Elasticsearch Service up and running for the first time. For questions about Elasticsearch Service configuration options or billing, check the [Technical FAQ](../../../deploy-manage/index.md) and the [Billing FAQ](../../../deploy-manage/cloud-organization/billing/billing-faq.md).

* [What is Elasticsearch Service?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-what)
* [Is Elasticsearch Service the same as Amazon’s {{es}} Service?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-aws-difference)
* [Can I run the full Elastic Stack in Elasticsearch Service?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-full-stack)
* [Can I try Elasticsearch Service for free?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-trial)
* [What if I need to change the size of my {{es}} cluster at a later time?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-config)
* [Do you offer support subscriptions?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-subscriptions)
* [Where is Elasticsearch Service hosted?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-where)
* [What is the difference between Elasticsearch Service and the Amazon {{es}} Service?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-vs-aws)
* [Can I use Elasticsearch Service on platforms other than AWS?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-aws)
* [Do you offer Elastic’s commercial products?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-elastic)
* [Is my {{es}} cluster protected by X-Pack?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-x-pack)
* [Is there a limit on the number of documents or indexes I can have in my cluster?](../../../deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-limit)

    $$$faq-what$$$What is Elasticsearch Service?
    :   Elasticsearch Service is hosted and managed {{es}} and {{kib}} brought to you by the creators of {{es}}. Elasticsearch Service is part of Elastic Cloud and ships with features that you can only get from the company behind {{es}}, {{kib}}, {{beats}}, and {{ls}}. {{es}} is a full text search engine that suits a range of uses, from search on websites to big data analytics and more.

    $$$faq-aws-difference$$$Is Elasticsearch Service the same as Amazon’s {{es}} Service?
    :   Elasticsearch Service is not the same as the Amazon {{es}} service. To learn more about the differences, check our [AWS {{es}} Service](https://www.elastic.co/aws-elasticsearch-service) comparison.

    $$$faq-full-stack$$$Can I run the full Elastic Stack in Elasticsearch Service?
    :   Many of the products that are part of the Elastic Stack are readily available in Elasticsearch Service, including {{es}}, {{kib}}, plugins, and features such as monitoring and security. Use other Elastic Stack products directly with Elasticsearch Service. For example, both Logstash and Beats can send their data to Elasticsearch Service. What is run is determined by the [subscription level](https://www.elastic.co/cloud/as-a-service/subscriptions).

    $$$faq-trial$$$Can I try Elasticsearch Service for free?
    :   Yes, sign up for a 14-day free trial. The trial starts the moment a cluster is created.

        During the free trial period get access to a deployment to explore Elastic solutions for Enterprise Search, Observability, Security, or the latest version of the Elastic Stack.


    $$$faq-config$$$What if I need to change the size of my {{es}} cluster at a later time?
    :   Scale your clusters both up and down from the user console, whenever you like. The resizing of the cluster is transparently done in the background, and highly available clusters are resized without any downtime. If you scale your cluster down, make sure that the downsized cluster can handle your {{es}} memory requirements. Read more about sizing and memory in [Sizing {{es}}](https://www.elastic.co/blog/found-sizing-elasticsearch).

    $$$faq-subscriptions$$$Do you offer support?
    :   Yes, all subscription levels for Elasticsearch Service include support, handled by email or through the Elastic Support Portal. Different subscription levels include different levels of support. For the Standard subscription level, there is no service-level agreement (SLA) on support response times. Gold and Platinum subscription levels include an SLA on response times to tickets and dedicated resources. To learn more, check [Getting Help](../../../troubleshoot/troubleshoot/index.md).

    $$$faq-where$$$Where is Elasticsearch Service hosted?
    :   We host our {{es}} clusters on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. Check out which [regions we support](https://www.elastic.co/guide/en/cloud/current/ec-reference-regions.html) and what [hardware we use](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html). New data centers are added all the time.

    $$$faq-vs-aws$$$What is the difference between Elasticsearch Service and the Amazon {{es}} Service?
    :   Elasticsearch Service is the only hosted and managed {{es}} service built, managed, and supported by the company behind {{es}}, {{kib}}, {{beats}}, and {{ls}}. With Elasticsearch Service, you always get the latest versions of the software. Our service is built on best practices and years of experience hosting and managing thousands of {{es}} clusters in the Cloud and on premise. For more information, check the following Amazon and Elastic {{es}} Service [comparison page](https://www.elastic.co/aws-elasticsearch-service).

        Please note that there is no formal partnership between Elastic and Amazon Web Services (AWS), and Elastic does not provide any support on the AWS {{es}} Service.


    $$$faq-aws$$$Can I use Elasticsearch Service on platforms other than AWS?
    :   Yes, create deployments on the Google Cloud Platform and Microsoft Azure.

    $$$faq-elastic$$$Do you offer Elastic’s commercial products?
    :   Yes, all Elasticsearch Service customers have access to basic authentication, role-based access control, and monitoring.

        Elasticsearch Service Gold, Platinum and Enterprise customers get complete access to all the capabilities in X-Pack:

        * Security
        * Alerting
        * Monitoring
        * Reporting
        * Graph Analysis & Visualization

        [Contact us](https://www.elastic.co/cloud/contact) to learn more.


    $$$faq-x-pack$$$Is my Elasticsearch cluster protected by X-Pack?
    :   Yes, X-Pack security features offer the full power to protect your Elasticsearch Service deployment with basic authentication and role-based access control.

    $$$faq-limit$$$Is there a limit on the number of documents or indexes I can have in my cluster?
    :   No. We do not enforce any artificial limit on the number of indexes or documents you can store in your cluster.

        That said, there is a limit to how many indexes Elasticsearch can cope with. Every shard of every index is a separate Lucene index, which in turn comprises several files. A process cannot have an unlimited number of open files. Also, every shard has its associated control structures in memory. So, while we will let you make as many indexes as you want, there are limiting factors. Our larger plans provide your processes with more dedicated memory and CPU-shares, so they are capable of handling more indexes. The number of indexes or documents you can fit in a given plan therefore depends on their structure and use.


