---
applies_to:
  deployment:
    self: ga
products:
  - id: kibana
---

# FIPS compliance for {{kib}} [fips-kibana]

To run {{kib}} in FIPS mode, you must have the appropriate [subscription](https://www.elastic.co/subscriptions).

::::{important}
The Node bundled with {{kib}} is not configured by default to be a FIPS environment. You must configure a FIPS 140-2 or FIPS 140-3 compliant OpenSSL3 provider. Consult the Node.js documentation to learn how to configure your environment.

::::


For {{kib}}, adherence to FIPS 140-2 and FIPS 140-3 is ensured by:

* Using FIPS-approved and NIST-recommended cryptographic algorithms.
* Delegating the implementation of these cryptographic algorithms to a NIST-certified cryptographic module (available via Node.js configured with the proper OpenSSL3 provider).
* Allowing the configuration of {{kib}} in a FIPS 140-2 or FIPS 140-3 compliant manner, as documented below.

The specific FIPS standard applied (140-2 or 140-3) depends on the OpenSSL3 provider used to configure your Node.js environment.

## Configuring {{kib}} for FIPS [_configuring_kib_for_fips]

The following settings need to be reviewed and configured to run {{kib}} successfully in a FIPS-compliant Node.js environment.

### Enable FIPS mode [_enable_fips_mode]

Set `xpack.security.fipsMode.enabled` to `true` in your {{kib}} configuration:

```yaml
xpack.security.fipsMode.enabled: true
```

### {{kib}} keystore [_kibana_keystore]

NIST Special Publication 800-132 (Recommendation for Password-Based Key Derivation: Part 1: Storage Applications) specifies a minimum security strength of 112 bits for password-protected key material, a requirement that applies in both FIPS 140-2 and FIPS 140-3 compliant environments. As such, the {{kib}} keystore password must be at least 14 bytes (112 bits) long. For single-byte ASCII characters, this means a minimum of 14 characters; for 2-byte UTF-8 characters (code points U+0080–U+07FF), a minimum of 7 characters.

For more information on how to set this password, refer to the [keystore documentation](/deploy-manage/security/secure-settings.md#change-password).


### TLS keystore and keys [_tls_keystore_and_keys]

Keystores can be used in a number of general TLS settings to store key and trust material. PKCS#12 keystores cannot be used in a FIPS 140-2 or FIPS 140-3 compliant Node.js environment. Avoid using these types of keystores. Your FIPS provider may offer a compliant keystore implementation, or you can use PEM-encoded files. To use PEM-encoded key material, use the relevant `*.key` and `*.certificate` configuration options; for trust material, use `*.certificate_authorities`.

As an example, avoid PKCS#12-specific settings such as:

* `server.ssl.keystore.path`
* `server.ssl.truststore.path`
* `elasticsearch.ssl.keystore.path`
* `elasticsearch.ssl.truststore.path`