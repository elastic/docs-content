---
navigation_title: Access {{kib}}
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/access.html
applies_to:
  deployment:
    self:
products:
  - id: kibana
---

# Access {{kib}} in a self-managed cluster [access]

Access {{kib}} through the web application on port 5601.

1. Point your web browser to the machine where you are running {{kib}} and specify the port number. For example, `localhost:5601` or `https://YOURDOMAIN.com:5601`.

    To remotely connect to {{kib}}, set [`server.host`](kibana://reference/configuration-reference/general-settings.md#server-host) to a non-loopback address.

    :::{note}
    For production deployments, you should always [secure {{kib}} with a certificate](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http) and access it over HTTPS.
    :::

2. Log on to your account.
3. Go to the home page, then click **{{kib}}**.
4. To make the {{kib}} page your landing page, click **Make this my landing page**.

## Grant other users access to {{kib}}

{{kib}} leverages {{es}} authentication and authorization technologies to secure access.

To learn about authentication options, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md). 

To learn how to enable authentication providers for {{kib}}, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md).

## Resources

* [Troubleshoot: Check {{kib}} server status](/troubleshoot/kibana/access.md)
* [Troubleshoot: Error: {{kib}} server is not ready yet](/troubleshoot/kibana/error-server-not-ready.md) 