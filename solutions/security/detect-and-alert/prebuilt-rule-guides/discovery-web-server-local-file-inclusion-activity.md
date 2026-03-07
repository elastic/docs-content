---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Web Server Local File Inclusion Activity" prebuilt detection rule.'
---

# Web Server Local File Inclusion Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Local File Inclusion Activity

This rule surfaces successful GET requests containing directory traversal or direct access to sensitive paths, signaling Local File Inclusion exploitation that can expose credentials, configuration, and process context and enable further compromise. A common attacker pattern is abusing a vulnerable parameter to fetch ../../../../etc/passwd, then pivoting to /proc/self/environ to harvest secrets and identify execution context for subsequent steps.

### Possible investigation steps

- Retrieve contiguous access logs around the alert to rebuild each request/response pair (URI, parameters, user agent, referer, cookies, X-Forwarded-For) and identify which parameter reflected traversal or wrapper usage and whether the response likely contained file contents.
- Compare response sizes and content-types for the suspicious requests to normal pages and look for signatures such as "root:x:" lines, INI/XML keys, or base64 blobs that indicate disclosure of /etc/passwd, web.config/applicationhost.config, or other sensitive files.
- Review web server and application error logs at the same timestamps for include/open stream warnings, open_basedir or allow_url_fopen messages, and stack traces to confirm the code path handling the input and any mitigations in place.
- Pivot on the same source and timeframe to find adjacent probes (php://filter, data://, expect://, zip://, phar://, /proc/self/environ, traversal into webroots/configs) and any follow-on POSTs to upload endpoints or new script paths, signaling progression toward RCE or webshell placement.
- Determine whether the traffic was authenticated and whether it traversed a WAF or reverse proxy by correlating cookies or session IDs and client IPs with proxy/WAF logs, noting any blocks, rule matches, or bypasses to bound scope and urgency.

### False positive analysis

- A site search or documentation endpoint echoing user-supplied text can include strings like ../../../../etc/passwd, windows/win.ini, or php://filter in the query string and return a normal 200 OK results page rather than performing a file include.
- An authenticated admin feature (such as a log viewer or file browser) may legitimately accept path= or file= parameters referencing local paths like /var/log/nginx or /inetpub/logs/logfiles and return 200 when serving allowed files, producing URLs that match the rule without exploitation.

### Response and remediation

- Immediately block the source IP at the reverse proxy/WAF and deploy deny rules for GET requests using ../../ or ..\..\ traversal or wrappers (php://, expect://, data://) that fetch /etc/passwd, /proc/self/environ, wp-config.php, web.config, or applicationhost.config.
- Configure the web server to return 403 for paths resolving to /proc, /etc, /var/log, /inetpub, applicationhost.config, and web.config and to reject wrapper schemes like php:// and expect://, then reload Nginx/Apache/IIS to apply.
- Fix the vulnerable include logic by canonicalizing input with realpath, rejecting any .. segments or absolute paths, enforcing a whitelist of allowed files, and in PHP disabling allow_url_include/allow_url_fopen and setting open_basedir to a safe directory.
- Rotate exposed secrets by changing database and API credentials from wp-config.php, connection strings and machine keys from web.config/applicationhost.config, and any tokens in /proc/self/environ, then invalidate active sessions and cache.
- Escalate to incident leadership and quarantine the host if response bodies contain credential patterns (e.g., "root:x:" from /etc/passwd or XML keys from web.config), if /etc/shadow or windows/system32/config/SAM was requested, or if follow-on POSTs or new .php/.aspx files appear in the webroot.
- Recover by verifying integrity of /var/www and /inetpub/wwwroot, scanning for webshells and unexpected includes, redeploying a known-good build or container image if tampering is found, and adding WAF normalization to double-decode URLs and 403 traversal attempts.
