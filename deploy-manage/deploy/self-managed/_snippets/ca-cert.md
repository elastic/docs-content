If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each {{es}} node:

```sh subs=true
{{es-conf}}{{slash}}certs{{slash}}http_ca.crt
```

Copy the `http_ca.crt` file to your machine and configure your client to use this certificate to establish trust when it connects to {{es}}.