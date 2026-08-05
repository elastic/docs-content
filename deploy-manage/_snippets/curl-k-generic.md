::::{tip}
If the remote endpoint uses a certificate that is not publicly trusted (for example, one signed by a private or corporate CA), provide the corresponding CA certificate using `--cacert /path/to/ca.pem` so that `curl` can verify it.

For testing only, you can use [`--insecure`](https://curl.se/docs/manpage.html#-k) (or `-k`) to skip certificate verification. This flag turns off TLS trust checks and should not be used in production.
::::
