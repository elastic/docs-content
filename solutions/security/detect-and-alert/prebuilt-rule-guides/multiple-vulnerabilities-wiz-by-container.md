---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Multiple Vulnerabilities by Asset via Wiz" prebuilt detection rule.
---

# Multiple Vulnerabilities by Asset via Wiz

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Multiple Vulnerabilities by Asset via Wiz

This alert identifies assets with an elevated number of vulnerabilities reported by Wiz, potentially indicating weak security posture, missed patching, or active exposure. The rule highlights assets with a high volume of distinct vulnerabilities, the presence of exploitable vulnerabilities, or a combination of multiple severities, helping prioritize assets that pose increased risk.

### Possible investigation steps

- Review the affected asset details using `wiz.vulnerability.vulnerable_asset.name` and `wiz.vulnerability.vulnerable_asset.id` to confirm asset ownership, criticality, and exposure (e.g., internet-facing, production).
- Examine the list of detected vulnerabilities using `Esql.vuln_id_values` to identify known high-risk or widely exploited CVEs.
- Assess vulnerability severity distribution via `Esql.vuln_severity_values`, focusing on assets with multiple severity levels or repeated high/critical findings.
- Determine whether any vulnerabilities have known exploits by validating `wiz.vulnerability.has_exploit`, prioritizing those assets for immediate remediation.
- Cross-check recent patching, configuration changes, or deployment activity on the asset to identify potential gaps or misconfigurations.

### False positive analysis

- Assets undergoing initial onboarding, scanning expansion, or configuration changes may temporarily report a high volume of findings.
- Vulnerability aggregation may include informational or low-impact findings that inflate counts without representing immediate risk.
- Duplicate or closely related vulnerabilities affecting shared packages or libraries may appear as multiple findings for the same root cause.
- Test, lab, or non-production assets may legitimately tolerate higher vulnerability counts depending on risk acceptance.

### Response and remediation

- Prioritize remediation for assets with exploitable vulnerabilities or multiple high/critical severity findings.
- Apply missing patches, updates, or configuration fixes according to asset criticality and exposure.
- Implement compensating controls (e.g., network segmentation, access restrictions) if immediate patching is not feasible.
- Validate remediation by re-scanning the asset in Wiz to confirm vulnerability reduction.
- Review vulnerability management processes to prevent recurrence, including patch SLAs, asset ownership, and exposure monitoring.
