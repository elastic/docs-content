# Supported versions [k8s-supported]

ECK is compatible with:

* Kubernetes 1.28-1.32
* OpenShift 4.12-4.17
* Google Kubernetes Engine (GKE), Azure Kubernetes Service (AKS), and Amazon Elastic Kubernetes Service (EKS)
* Helm: 3.2.0+
* Elasticsearch, Kibana, APM Server: 6.8+, 7.1+, 8+
* Enterprise Search: 7.7+, 8.x (Enterprise Search is not available in {{stack}} 9.0+)

* Beats: 7.0+, 8+
* Elastic Agent: 7.10+ (standalone), 7.14+ (Fleet), 8+
* Elastic Maps Server: 7.11+, 8+
* Logstash: 8.7+

ECK should work with all conformant installers as listed in these [FAQs](https://github.com/cncf/k8s-conformance/blob/master/faq.md#what-is-a-distribution-hosted-platform-and-an-installer). Distributions include source patches and so may not work as-is with ECK.

Alpha, beta, and stable API versions follow the same [conventions used by Kubernetes](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning).

Elastic Stack application images for the OpenShift-certified Elasticsearch (ECK) Operator are only available from version 7.10 and later.

Check the full [Elastic support matrix](https://www.elastic.co/support/matrix#matrix_kubernetes) for more information.

