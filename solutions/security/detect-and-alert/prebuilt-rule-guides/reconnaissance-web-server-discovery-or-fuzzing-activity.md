---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Web Server Discovery or Fuzzing Activity" prebuilt detection rule.
---

# Web Server Discovery or Fuzzing Activity

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Discovery or Fuzzing Activity

This rule flags a single origin generating a rapid burst of GET requests that produce many 404/403 responses, a hallmark of automated web discovery or fuzzing. Attackers commonly run wordlist-driven enumeration to probe paths such as /admin/, /login, /backup.zip, /.env, /.git/, and undocumented API routes, gauging which resources exist and where access controls fail. Detecting this reconnaissance early helps prevent subsequent targeted exploitation of newly found endpoints and weak authentication flows.

### Possible investigation steps

- Correlate user-agent, TLS JA3/JA4, Host/SNI, and X-Forwarded-For to fingerprint the client, identify common fuzzing tools or disguised automation, and recover the true origin if traffic traversed a CDN or proxy.
- Summarize the top requested paths and response codes for this source to spot any 2xx or 401 outcomes amid the denials, flagging hits on sensitive locations such as /.env, /.git, /admin interfaces, backups, installer scripts, and undocumented API routes.
- Pivot to the same timeframe for adjacent web and authentication activity from this origin to see whether POSTs, credential attempts, or parameterized requests followed the enumeration, indicating progression toward exploitation or spraying.
- Review WAF/CDN and reverse-proxy logs for blocks, challenges, or rate limiting and whether multiple virtual hosts were targeted via the Host header, confirming if and how far requests reached the application tier.
- Validate whether the source aligns with approved internal scanners or scheduled testing via inventories and change records, and if not, enrich with ASN/geolocation, reverse DNS, and threat intel to assess reputation and recurrence across your estate.

### False positive analysis

- An internal QA link checker or monitoring crawler run from a single host can request hundreds of unique paths and generate many 404/403 GETs when routes, assets, or permissions are misconfigured.
- A shared egress IP (NAT or corporate proxy) aggregating many users during a faulty deployment can trigger high volumes of 404/403 GETs as browsers collectively hit moved or newly restricted resources.

### Response and remediation

- Immediately rate-limit or block the offending source IP at the WAF/CDN and reverse proxy, applying a challenge or temporary ban to the observed User-Agent and JA3/JA4 fingerprint driving the 500+ unique-path 404/403 GET burst.
- If traffic came through a proxy or CDN, use X-Forwarded-For to identify and block the true origin, and add a temporary ASN or geolocation block if the source aligns with known scanner networks.
- Verify whether the source is an approved internal scanner; if not, disable the job or container, remove any scheduled tasks and API keys used, and notify the owner to stop testing against production immediately.
- Review the requested path list to identify any 2xx or 401 hits and remediate exposures such as accessible /.env, /.git, /admin interfaces, backup archives, or installer scripts by removing files, disabling endpoints, and rotating secrets.
- Escalate to incident response if enumeration persists after blocking, pivots to POSTs or credential attempts, originates from rotating IPs (Tor/VPN/residential), or produces 2xx on sensitive endpoints despite WAF rules.
- Harden the web tier by enabling per-IP rate limiting and bot challenges, turning off directory listing and default app endpoints, blocking patterns like /.git/, /.env, and /backup.zip at the WAF, and restricting origin access to CDN egress only.

