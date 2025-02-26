# Technical FAQ [ec-faq-technical]

This frequently-asked-questions list answers some of your more common questions about configuring {{ech}}.

* [Can I implement a Hot-Warm architecture?](../../../deploy-manage/index.md#faq-hw-architecture)
* [What about dedicated master nodes?](../../../deploy-manage/index.md#faq-master-nodes)
* [Can I use a Custom SSL certificate?](../../../deploy-manage/index.md#faq-ssl)
* [Can {{ech}} autoscale?](../../../deploy-manage/index.md#faq-autoscale)
* [Do you support IP sniffing?](../../../deploy-manage/index.md#faq-ip-sniffing)
* [Does {{ech}} support encryption at rest?](../../../deploy-manage/index.md#faq-encryption-at-rest)
* [Can I find the static IP addresses for my endpoints on {{ech}}?](../../../deploy-manage/index.md#faq-static-ip-elastic-cloud)

    $$$faq-hw-architecture$$$Can I implement a hot-warm architecture?
    :   [*hot-warm architecture*](https://www.elastic.co/blog/hot-warm-architecture) refers to an Elasticsearch setup for larger time-data analytics use cases with two different types of nodes, hot and warm. {{ech}} supports hot-warm architectures in all of the solutions provided by allowing you to add warm nodes to any of your deployments.

    $$$faq-master-nodes$$$What about dedicated master nodes?
    :   [Master nodes](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/modules-node.html#master-node) are responsible for cluster-wide actions, such as creating or deleting an index, tracking which nodes are part of the cluster, and deciding which shards to allocate to which nodes. For clusters that have six or more Elasticsearch nodes, dedicated master-eligible nodes are introduced. When your cluster grows, consider separating dedicated master-eligible nodes from dedicated data nodes. We recommend using at least 4GB RAM for dedicated master nodes.

    $$$faq-ssl$$$Can I use a Custom SSL certificate?
    :   We don’t support custom SSL certificates, which means that a custom CNAME for an {{ech}} endpoint such as *mycluster.mycompanyname.com* also is not supported.

    $$$faq-autoscale$$$Can {{ech}} autoscale?
    :   {{ech}} now supports autoscaling. To learn how to enable it through the console or the API, check [Deployment autoscaling](../../../deploy-manage/autoscaling.md).

    $$$faq-ip-sniffing$$$Do you support IP sniffing?
    :   IP sniffing is not supported by design and will not return the expected results. We prevent IP sniffing from returning the expected results to improve the security of our underlying {{ech}} infrastructure.

    $$$faq-encryption-at-rest$$$Does {{ech}} support encryption at rest?
    :   Yes, encryption at rest (EAR) is enabled in {{ech}} by default. We support EAR for both the data stored in your clusters and the snapshots we take for backup, on all cloud platforms and across all regions.


You can also bring your own key (BYOK) to encrypt your Elastic Cloud deployment data and snapshots. For more information, check [Encrypt your deployment with a customer-managed encryption key](../../../deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).

Note that the encryption happens at the file system level.

$$$faq-static-ip-elastic-cloud$$$We have requirements around restricting access by adding firewall rules to only allow access to certain IP addresses from our Infosec team. Do you provide static IP addresses for the endpoints on {{ech}}?
:   We do provide [static IP ranges](../../../deploy-manage/security/elastic-cloud-static-ips.md), but they should be used with caution as noted in the documentation. IP addresses assigned to cloud resources can change without notice. This could be initiated by cloud providers with no knowledge to us. For this reason, we generally do not recommend that you use firewall rules to allow or restrict certain IP ranges. If you do wish to secure communication for deployment endpoints on {{ech}}, please use [Private Link](../../../deploy-manage/security/traffic-filtering.md). However, in situations where using Private Link services do not meet requirements (for example, secure traffic **from** Elastic Cloud), static IP ranges can be used.

