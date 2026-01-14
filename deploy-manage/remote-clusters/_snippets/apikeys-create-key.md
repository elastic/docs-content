<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- remote-clusters-api-key.md
- eck-remote-clusters-to-other-eck.md
- eck-remote-clusters-to-external.md
- ece-remote-cluster-self-managed.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ece-ess.md
- ece-enable-ccs-for-eck.md
- ec-remote-cluster-self-managed.md
- ec-remote-cluster-same-ess.md
- ec-remote-cluster-other-ess.md
- ec-remote-cluster-ece.md
- ec-enable-ccs-for-eck.md
-->
1. On the remote cluster, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](/deploy-manage/api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it to include access to the indices you want to use for {{ccs}} or {{ccr}}.
2. Copy the encoded key (`encoded` in the response) to a safe location. It is required for the local cluster configuration.
