### Certificate management

Follow these best practices for managing certificates:

* Never use self-signed certificates in production. Generate certificates using a trusted CA or your organization's CA.
* When generating certificates, include all hostnames and IP addresses that will be used in the certificate's Subject Alternative Name (SAN) list.
* Store private keys securely and use appropriate file permissions. Consider using encrypted keys with passphrases.
* Plan for certificate rotation. For more information, refer to [Certificate rotation](/reference/fleet/certificates-rotation.md).