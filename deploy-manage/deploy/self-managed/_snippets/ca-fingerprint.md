Copy the fingerprint value that’s output to your terminal when {{es}} starts, and configure your client to use this fingerprint to establish trust when it connects to {{es}}.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate by running the following command. The path is to the auto-generated CA certificate for the HTTP layer.

```sh
openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt
```

The command returns the security certificate, including the fingerprint. The `issuer` should be `Elasticsearch security auto-configuration HTTP CA`.

```sh
issuer= /CN=Elasticsearch security auto-configuration HTTP CA
SHA256 Fingerprint=<fingerprint>
```