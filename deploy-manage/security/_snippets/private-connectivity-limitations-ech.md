* **Transport client:** The {{es}} transport client is not supported over private connections.
* **Managed OTLP endpoint:** The [managed OTLP endpoint](opentelemetry://reference/motlp.md) is not accessible over private connections. The public endpoint is still available.
* **SSO to {{kib}} from the {{ecloud}} console:** You can't use SSO to log in to {{kib}} endpoints that are protected by private connections. Then the connection to {{kib}} public URL is still available.

  As a workaround, you can [add an IP filter](/deploy-manage/security/ip-filtering-cloud.md) for the hosts that will use SSO through the {{ecloud}} console.
  
  In {{ech}}, you can still SSO into private {{kib}} endpoints individually using the [SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md) or [OIDC](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md) protocol from your own identity provider, just not through the {{ecloud}} console. Stack-level authentication using the {{es}} username and password also works with `{{kibana-id}}.vpce.{region}.aws.elastic-cloud.com` URLs.