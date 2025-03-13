---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-security-principles.html
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/elastic-stack/current/install-stack-demo-secure.html
---

# Secure your cluster or deployment

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/346

% Scope notes: consider keeping the mapped tutorial as a quickstart at some level

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md
% - [ ] ./raw-migrated-files/kibana/kibana/using-kibana-with-security.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/install-stack-demo-secure.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$install-stack-demo-secure-agent$$$

$$$install-stack-demo-secure-ca$$$

$$$install-stack-demo-secure-fleet$$$

$$$install-stack-demo-secure-http$$$

$$$install-stack-demo-secure-kib-es$$$

$$$install-stack-demo-secure-prereqs$$$

$$$install-stack-demo-secure-second-node$$$

$$$install-stack-demo-secure-transport$$$

$$$install-stack-demo-secure-view-data$$$

$$$security-configure-settings$$$

**This page is a work in progress.** The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md)
* [/raw-migrated-files/kibana/kibana/using-kibana-with-security.md](/raw-migrated-files/kibana/kibana/using-kibana-with-security.md)
* [/raw-migrated-files/stack-docs/elastic-stack/install-stack-demo-secure.md](/deploy-manage/security/install-stack-demo-secure.md)

Protecting your {{es}} cluster and the data it contains is of utmost importance. Implementing a defense in depth strategy provides multiple layers of security to help safeguard your system.

:::{important}
Never run an {{es}} cluster without security enabled. This principle cannot be overstated. Running {{es}} without security leaves your cluster exposed to anyone who can send network traffic to {{es}}, permitting these individuals to download, modify, or delete any data in your cluster.
::: 

To secure your clusters and deployments, consider the following:

## Network access

Control which systems can access your Elastic deployments and clusters through traffic filtering and network controls:

- **IP traffic filtering**: Restrict access based on IP addresses or CIDR ranges.
- **Private link filters**: Secure connectivity through AWS PrivateLink, Azure Private Link, or GCP Private Service Connect.
- **Static IPs**: Use static IP addresses for predictable firewall rules.
- **Remote cluster access**: Secure cross-cluster operations.

Refer to [](traffic-filtering.md).

## Cluster communication

- **HTTP and HTTPs**
- **TLS certificates and keys**


## Data, objects and settings security

- **Bring your own encryption key**: Use your own encryption key instead of the default encryption at rest provided by Elastic.
- **{{es}} and {{kib}} keystores**: Secure sensitive settings using keystores
- **{{kib}} saved objects**: Customize the encryption for {{kib}} objects such as dashboards.
- **{{kib}} session management**: Customize {{kib}} session expiration settings.

Refer to [](data-security.md).

## User roles

[Define roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for your users and [assign appropriate privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to ensure that users have access only to the resources that they need. This process determines whether the user behind an incoming request is allowed to run that request.

:::{important}
Never try to run {{es}} as the `root` user, which would invalidate any defense strategy and permit a malicious user to do **anything** on your server. You must create a dedicated, unprivileged user to run {{es}}. By default, the `rpm`, `deb`, `docker`, and Windows packages of {{es}} contain an `elasticsearch` user with this scope.
:::
