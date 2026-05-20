---
navigation_title: Certificate verification with curl on Mac
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-maccurl.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot failed certificate verification with curl on Mac [trb-security-maccurl]

**Symptoms:**

* `curl` on the Mac returns a certificate verification error even when the `--cacert` option is used.

**Resolution:**

Apple’s integration of `curl` with their keychain technology disables the `--cacert` option. See [http://curl.haxx.se/mail/archive-2013-10/0036.html](http://curl.haxx.se/mail/archive-2013-10/0036.html) for more information.

You can use another tool, such as `wget`, to test certificates. Alternately, you can add the certificate for the signing certificate authority MacOS system keychain, using a procedure similar to the one detailed at the [Apple knowledge base](http://support.apple.com/kb/PH14003). Be sure to add the signing CA’s certificate and not the server’s certificate.

