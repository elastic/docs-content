---
navigation_title: Kerberos
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-kerberos.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Common Kerberos exceptions [trb-security-kerberos]

**Symptoms:**

* User authentication fails due to either GSS negotiation failure or a service login failure (either on the server or in the {{es}} http client). Some of the common exceptions are listed below with some tips to help resolve them.

**Resolution:**

`Failure unspecified at GSS-API level (Mechanism level: Checksum failed)`
:   When you see this error message on the HTTP client side, then it may be related to an incorrect password.

When you see this error message in the {{es}} server logs, then it may be related to the {{es}} service keytab. The keytab file is present but it failed to log in as the user. Check the keytab expiry. Also check whether the keytab contain up-to-date credentials; if not, replace them.

You can use tools like `klist` or `ktab` to list principals inside the keytab and validate them. You can use `kinit` to see if you can acquire initial tickets using the keytab. Check the tools and their documentation in your Kerberos environment.

Kerberos depends on proper hostname resolution, so check your DNS infrastructure. Incorrect DNS setup, DNS SRV records or configuration for KDC servers in `krb5.conf` can cause problems with hostname resolution.


`Failure unspecified at GSS-API level (Mechanism level: Request is a replay (34))`
`Failure unspecified at GSS-API level (Mechanism level: Clock skew too great (37))`
:   To prevent replay attacks, Kerberos V5 sets a maximum tolerance for computer clock synchronization and it is typically 5 minutes. Check whether the time on the machines within the domain is in sync.


`gss_init_sec_context() failed: An unsupported mechanism was requested`
`No credential found for: 1.2.840.113554.1.2.2 usage: Accept`
:   You would usually see this error message on the client side when using `curl` to test {{es}} Kerberos setup. For example, these messages occur when you are using an old version of curl on the client and therefore Kerberos Spnego support is missing. The Kerberos realm in {{es}} only supports Spengo mechanism (Oid 1.3.6.1.5.5.2); it does not yet support Kerberos mechanism (Oid 1.2.840.113554.1.2.2).

Make sure that:

* You have installed curl version 7.49 or above as older versions of curl have known Kerberos bugs.
* The curl installed on your machine has `GSS-API`, `Kerberos` and `SPNEGO` features listed when you invoke command `curl -V`. If not, you will need to compile `curl` version with this support.

To download latest curl version visit [https://curl.haxx.se/download.html](https://curl.haxx.se/download.html)


As Kerberos logs are often cryptic in nature and many things can go wrong as it depends on external services like DNS and NTP. You might have to enable additional debug logs to determine the root cause of the issue.

{{es}} uses a JAAS (Java Authentication and Authorization Service) Kerberos login module to provide Kerberos support. To enable debug logs on {{es}} for the login module use following Kerberos realm setting:

```yaml
xpack.security.authc.realms.kerberos.<realm-name>.krb.debug: true
```

For detailed information, see [Kerberos realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-kerberos-settings).

Sometimes you may need to go deeper to understand the problem during SPNEGO GSS context negotiation or look at the Kerberos message exchange. To enable Kerberos/SPNEGO debug logging on JVM, add following JVM system properties:

`-Dsun.security.krb5.debug=true`

`-Dsun.security.spnego.debug=true`

For more information about JVM system properties, see [Set JVM options](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options).

