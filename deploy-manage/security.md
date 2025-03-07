---
applies_to:
  deployment: all
  serverless: all
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
---

# Security

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

An Elastic implementation comprises many moving parts. There are the Elasticsearch nodes that form the cluster, Kibana instances, additional stack components such as Logstash and Beats, and clients and integrations all communicating with your cluster.

To keep your data secured, Elastic offers security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster. Regardless of your deployment type, Elastic sets up certain security features for you automatically.

In this section, you’ll learn about how to manage basic Elastic security features. You’ll also learn how to implement advanced security measures.

As part of your overall security strategy, you can also do the following:

- Prevent unauthorized access with [password protection and role-based access control].
- Maintain an [audit trail] for security-related events.
- Control access to dashboards and other saved objects in your UI using [Spaces].
- Connect a local cluster to a [remote cluster] to enable cross-cluster replication and search.
- Manage [API keys] used for programmatic access to Elastic.



Keeping your Elastic installation and data safe generally means:

- Securing the hosting environment where your Elastic products are deployed.
  - self-managed
    - TLS certificates
    - HTTPS 
  - ECE
    - TLS certificates
    - Cloud RBAC
  - ECH and Serverless
    - SSO
    - Role-based access control
- Securing the deployments and clusters within that environment.
  - Authentication and access
    - `elastic` power user, built-in and system user passwords
    - Deployment-level authentication protocols (SAML, OpenID Connect, Kerberos, JWT)
    - Trust for cross-cluster communication
    - Traffic and IP filtering
  - Using the Elasticsearch keystore for sensitive settings
  - [ECH only] Encryption using a customer-managed encryption key
  - Keeping deployments up to date
  - Audit logging
  - Index and document-level permissions
  - Kibana security
    - Kibana sessions management
    - Spaces
    - Saved object security
- Securing your own account and access to the environment and deployments.
  - [ECH only] Multifactor authentication
  - User API keys
- Securing clients and integrations connected to your environment's clusters.


