<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- eck-remote-clusters.md
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
% this will need improvement in a future PR, as the text below is only valid for API key based security model

If you're using the API key–based security model for {{ccr}} or {{ccs}}, you can define user roles with [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) on the local cluster to further restrict the permissions granted by the API key. For more details, refer to [Configure roles and users](/deploy-manage/remote-clusters/remote-clusters-api-key.md#remote-clusters-privileges-api-key).