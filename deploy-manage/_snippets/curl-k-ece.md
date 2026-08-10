::::{important}
The `curl` examples on this page use HTTPS. If the remote endpoint uses a certificate that is not publicly trusted (for example, one signed by a private or corporate CA), provide the corresponding CA certificate using `--cacert /path/to/ca.pem` so that `curl` can verify it. For more details, refer to [manage security certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md).

For testing only, you can use [`--insecure`](https://curl.se/docs/manpage.html#-k) (or `-k`) to skip certificate verification. This flag turns off TLS trust checks and should not be used in production.
::::
