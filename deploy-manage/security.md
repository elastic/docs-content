---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-files.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-securing-stack.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-ece.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-security.html
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-limitations.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-security-principles.html
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-technical.html
---

# Security

% SR: include this info somewhere in this section
% {{ech}} doesn't support custom SSL certificates, which means that a custom CNAME for an {{ech}} endpoint such as *mycluster.mycompanyname.com* also is not supported.
%
% In {{ech}}, IP sniffing is not supported by design and will not return the expected results. We prevent IP sniffing from returning the expected results to improve the security of our underlying {{ech}} infrastructure.
%
% encryption at rest (EAR) is enabled in {{ech}} by default. We support EAR for both the data stored in your clusters and the snapshots we take for backup, on all cloud platforms and across all regions.
% You can also bring your own key (BYOK) to encrypt your Elastic Cloud deployment data and snapshots. For more information, check [Encrypt your deployment with a customer-managed encryption key](../../../deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).

Note that the encryption happens at the file system level.

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/346

% Scope notes: this is just communication security - link to users + roles, spaces, monitoring, ++

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md
%      Notes: redirect only
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md
% - [ ] ./raw-migrated-files/kibana/kibana/xpack-security.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-security.md
% - [ ] ./raw-migrated-files/kibana/kibana/using-kibana-with-security.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-faq-technical.md

$$$field-document-limitations$$$

$$$alias-limitations$$$

$$$preventing-unauthorized-access$$$

$$$preserving-data-integrity$$$

$$$maintaining-audit-trail$$$

**This page is a work in progress.** The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md)
* [/raw-migrated-files/kibana/kibana/xpack-security.md](/raw-migrated-files/kibana/kibana/xpack-security.md)
* [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md](/raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md)
* [/raw-migrated-files/cloud/cloud-heroku/ech-security.md](/raw-migrated-files/cloud/cloud-heroku/ech-security.md)
* [/raw-migrated-files/kibana/kibana/using-kibana-with-security.md](/raw-migrated-files/kibana/kibana/using-kibana-with-security.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md)
* [/raw-migrated-files/cloud/cloud/ec-faq-technical.md](/raw-migrated-files/cloud/cloud/ec-faq-technical.md)