---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-secure-comms-stack.html
---

# Secure communication with the Elastic Stack [apm-secure-comms-stack]

::::{note} 
This documentation only applies to the APM Server binary.
::::


Use role-based access control or API keys to grant APM Server users access to secured resources.


## Role-based access [apm-secure-comms-stack-role-based] 

Manage access on a feature-by-feature basis by creating several custom feature-related roles and assigning one or more of these roles to each APM Server user based on which features they need to access.

[**Read more in Use feature roles →**](create-assign-feature-roles-to-apm-server-users.md)


## API keys [apm-secure-comms-stack-api-keys] 

Instead of using usernames and passwords, you can use API keys to grant access to Elasticsearch resources. You can set API keys to expire at a certain time, and you can explicitly invalidate them.

[**Read more in Grant access using API keys →**](grant-access-using-api-keys.md)


## More resources [_more_resources] 

After privileged users have been created, use authentication to connect to a secured Elastic cluster.

* [Secure communication with {{es}}](configure-elasticsearch-output.md#apm-securing-communication-elasticsearch)
* [Secure communication with {{ls}}](configure-logstash-output.md#apm-configuring-ssl-logstash)

For secure communication between APM Server and APM Agents, see [Secure communication with APM agents](secure-communication-with-apm-agents.md).

A reference of all available [SSL configuration settings](ssltls-settings.md) is also available.

::::{important} 
:name: apm-security-overview

APM Server exposes an HTTP endpoint, and as with anything that opens ports on your servers, you should be careful about who can connect to it. Firewall rules are recommended to ensure only authorized systems can connect.

::::




