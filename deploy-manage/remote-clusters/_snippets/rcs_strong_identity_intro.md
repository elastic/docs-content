Cross-cluster API keys can be configured with strong identity verification to provide an additional layer of security. To enable this feature, a
cross-cluster API key is created on the remote cluster with a certificate identity pattern that specifies which certificates are allowed
to use it. The local cluster must then sign each request with its private key and include a certificate whose subject Distinguished Name
(DN) matches the pattern. The remote cluster validates both that the certificate is trusted by its configured certificate authorities
and that the certificate's subject matches the API key's identity pattern.

:::{note}
Each remote cluster alias on the local cluster can have different remote signing configurations.
:::
