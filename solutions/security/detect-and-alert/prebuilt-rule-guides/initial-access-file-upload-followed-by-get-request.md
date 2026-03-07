---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Initial Access via File Upload Followed by GET Request" prebuilt detection rule.
---

# Initial Access via File Upload Followed by GET Request

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Initial Access via File Upload Followed by GET Request

This rule flags a common initial-access pattern: a multipart/form-data upload that drops a dynamic web script on a server, followed shortly by a request to execute that file and establish a foothold. Attackers exploit a permissive upload form to plant shell.php or shell.jsp in an uploads or temp directory, then immediately request it to spawn a web shell, enumerate files, and run commands—often leveraging redirects or 2xx/3xx responses that indicate successful placement and access.

### Possible investigation steps

- Correlate the upload transaction with the server-side file creation and the subsequent access to the same resource, matching timestamps, source IP, and path, and follow any redirects to the final executed file.
- Retrieve the uploaded artifact from disk, verify it sits in a web-accessible location, inspect content for web shell traits (eval/system/exec, obfuscation, password gates), and record hashes.
- Examine server process telemetry immediately after the access for interpreter or shell spawns and unexpected outbound connections originating from web server workers.
- Review application logs and access context to determine whether the upload was authenticated, which account or session performed it, and whether user-agent, referer, or headers deviate from normal clients.
- Broaden the timeline to identify related uploads, file renames, or repeated requests from the same actor, including parameterized calls that suggest command execution or directory enumeration.

### False positive analysis

- An authenticated administrator installs a legitimate plugin or module via the application’s upload form, which unpacks or renames .php or .jsp files and then auto-loads a setup page, producing the multipart upload, file creation/rename, and immediate GET pattern.
- Automated deployment or QA routines upload and deploy a .war or server-side script through a web-based admin interface and then perform health-check or warm-up requests, resulting in the same multipart upload, server-side file creation, and follow-up GET sequence.

### Response and remediation

- Immediately block access to the uploaded script that was invoked via GET/POST (e.g., /uploads/shell.php) and the source IPs that executed it, restrict the site to allowlisted IPs or maintenance mode, and temporarily disable the upload endpoint.
- Quarantine and remove the uploaded web shell and any additional executable scripts or WARs in web-accessible directories (uploads, webroot, temp), terminate interpreter or shell processes spawned by the web server account (www-data/nginx/w3wp/tomcat), and revert malicious .htaccess/web.config rewrites.
- Hunt for persistence and lateral-movement artifacts created after the upload, including recent .php/.jsp/.cgi file creations or renames in static asset folders, cron/systemd tasks, startup scripts, unauthorized admin users or plugins, and remove them.
- Restore altered application files from known-good backups or redeploy a clean container/VM, rotate database and API credentials stored in config files or environment variables, invalidate active sessions, and only re-enable uploads after confirming execution is blocked in upload directories.
- Escalate to incident command and privacy/legal if you observe command execution parameters on the uploaded page (?cmd=, ?exec=), shells spawning (/bin/sh, powershell.exe), database dumps, or outbound callbacks from web server processes to external hosts.
- Harden by storing uploads outside the webroot, denying execution in upload paths (disable PHP/CGI handlers and set noexec permissions), enforcing strict extension/MIME allowlists and AV/sandbox scanning for multipart/form-data, enabling file-integrity alerts on new .php/.jsp in served paths, and deploying WAF rules to block direct requests to uploaded executables.

