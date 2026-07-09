HTTP TLS is automatically enabled for {{es}} and {{kib}} using self-signed certificates, with [several options available for customization](/deploy-manage/security/k8s-https-settings.md), including custom certificates and domain names.

{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.

```{applies_to}
eck: ga 3.4
```

You can require {{es}} HTTP clients to present TLS client certificates (mutual TLS). For configuration details, see [Elasticsearch client certificate authentication on ECK](/deploy-manage/security/k8s-es-client-certificate-auth.md).
