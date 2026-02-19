When a local cluster makes a request to a remote cluster using a cross-cluster API key:

1. The local cluster signs the request headers with its configured private key and sends the signature and certificate chain as header
   in the request to the remote cluster.
2. The remote cluster verifies that the API key is valid.
3. If the API key has a certificate identity pattern configured, the remote cluster extracts the Distinguished Name (DN) from the
   certificate chain's leaf certificate and matches it against the certificate identity pattern.
4. The remote cluster validates that the provided certificate chain is trusted.
5. The remote cluster validates the signature and checks that the certificate is not expired.

If any of these validation steps fail, the request is rejected.
