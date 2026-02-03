Follow these steps to configure trust in your self-managed cluster:

1. Trust the [deployment CA you downloaded previously](#download-ca) by either configuring the [setting](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md) `xpack.security.transport.ssl.certificate_authorities` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) or by [adding it to the trust store](/deploy-manage/security/different-ca.md).

2. Configure trust restrictions in the self-managed cluster:

    All the clusters in an {{ech}} region or an {{ece}} environment are signed by the same certificate authority. As a result, if you only add this CA to your self-managed cluster, it would trust every cluster in that region or environment, including clusters that belong to other organizations.

    To avoid this, use the setting `xpack.security.transport.ssl.trust_restrictions.path`, which points to a file that limits the certificates that are trusted based on their `otherName` attribute.

	  The following is an example of a trust restrictions file, with an explanation of what each entry allows:

    ```yaml
      trust.subject_name:
      - *.node.aaaabbbbaaaabbbb.cluster.1053523734.account <1>
      - *.node.xxxxyyyyxxxxyyyy.cluster.1053523734.account <1>
      - *.node.*.cluster.83988631.account <2>
      - node*.<CLUSTER_FQDN> <3>
    ```
    1. Two specific clusters with cluster ids `aaaabbbbaaaabbbb` and `xxxxyyyyxxxxyyyy` from an ECE environment or ECH organization with ID `1053523734`
    2. Any cluster from an ECE environment or ECH organization with ID `83988631`
    3. The nodes from its own cluster (whose certificates follow a different convention: `CN = node1.<CLUSTER_FQDN>`, `CN = node2.<CLUSTER_FQDN>` and `CN = node3.<CLUSTER_FQDN>`)
