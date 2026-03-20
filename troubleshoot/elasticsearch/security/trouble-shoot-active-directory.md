---
navigation_title: Active Directory account lockout
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trouble-shoot-active-directory.html
applies_to:
  deployment:
    eck:
    ece:
    self:
products:
  - id: elasticsearch
---

# Troubleshoot Active Directory account lockout [trouble-shoot-active-directory]

**Symptoms:**

* Certain users are being frequently locked out of Active Directory.

**Resolution:**

Check your realm configuration; realms are checked serially, one after another. If your Active Directory realm is being checked before other realms and there are usernames that appear in both Active Directory and another realm, a valid login for one realm might be causing failed login attempts in another realm.

For example, if `UserA` exists in both Active Directory and a file realm, and the Active Directory realm is checked first and file is checked second, an attempt to authenticate as `UserA` in the file realm would first attempt to authenticate against Active Directory and fail, before successfully authenticating against the `file` realm. Because authentication is verified on each request, the Active Directory realm would be checked - and fail - on each request for `UserA` in the `file` realm. In this case, while the authentication request completed successfully, the account on Active Directory would have received several failed login attempts, and that account might become temporarily locked out. Plan the order of your realms accordingly.

Also note that it is not typically necessary to define multiple Active Directory realms to handle domain controller failures. When using Microsoft DNS, the DNS entry for the domain should always point to an available domain controller.

