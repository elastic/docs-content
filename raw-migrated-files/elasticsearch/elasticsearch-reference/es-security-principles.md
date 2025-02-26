# {{es}} security principles [es-security-principles]

Protecting your {{es}} cluster and the data it contains is of utmost importance. Implementing a defense in depth strategy provides multiple layers of security to help safeguard your system. The following principles provide a foundation for running {{es}} in a secure manner that helps to mitigate attacks on your system at multiple levels.


## Run {{es}} with security enabled [security-run-with-security] 

Never run an {{es}} cluster without security enabled. This principle cannot be overstated. Running {{es}} without security leaves your cluster exposed to anyone who can send network traffic to {{es}}, permitting these individuals to download, modify, or delete any data in your cluster. [Start the {{stack}} with security enabled](../../../deploy-manage/security/security-certificates-keys.md) or [manually configure security](../../../deploy-manage/security/manually-configure-security-in-self-managed-cluster.md) to prevent unauthorized access to your clusters and ensure that internode communication is secure.


## Run {{es}} with a dedicated non-root user [security-not-root-user] 

Never try to run {{es}} as the `root` user, which would invalidate any defense strategy and permit a malicious user to do **anything** on your server. You must create a dedicated, unprivileged user to run {{es}}. By default, the `rpm`, `deb`, `docker`, and Windows packages of {{es}} contain an `elasticsearch` user with this scope.


## Protect {{es}} from public internet traffic [security-protect-cluster-traffic] 

Even with security enabled, never expose {{es}} to public internet traffic. Using an application to sanitize requests to {{es}} still poses risks, such as a malicious user writing [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search) requests that could overwhelm an {{es}} cluster and bring it down. Keep {{es}} as isolated as possible, preferably behind a firewall and a VPN. Any internet-facing applications should run pre-canned aggregations, or not run aggregations at all.

While you absolutely shouldn’t expose {{es}} directly to the internet, you also shouldn’t expose {{es}} directly to users. Instead, use an intermediary application to make requests on behalf of users. This implementation allows you to track user behaviors, such as can submit requests, and to which specific nodes in the cluster. For example, you can implement an application that accepts a search term from a user and funnels it through a [`simple_query_string`](asciidocalypse://docs/elasticsearch/docs/reference/query-languages/query-dsl-simple-query-string-query.md) query.


## Implement role based access control [security-create-appropriate-users] 

[Define roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for your users and [assign appropriate privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to ensure that users have access only to the resources that they need. This process determines whether the user behind an incoming request is allowed to run that request.

