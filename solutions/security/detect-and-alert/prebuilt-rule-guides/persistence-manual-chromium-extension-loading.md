---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Manual Loading of a Suspicious Chromium Extension" prebuilt detection rule.
---

# Manual Loading of a Suspicious Chromium Extension

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Manual Loading of a Suspicious Chromium Extension

Chromium-based browsers support loading extensions from local directories using the --load-extension command line flag, bypassing the normal extension store installation process. Threat actors abuse this capability to load malicious extensions that can steal cookies, capture session tokens, intercept form submissions, or inject content into web pages. Unlike store-installed extensions, manually loaded extensions don't undergo security review and can request arbitrary permissions. This detection rule identifies browsers launched with the --load-extension flag from suspicious parent processes.

### Possible investigation steps

- Examine the process.args containing --load-extension to identify the full path of the extension being loaded.
- Navigate to the extension directory and review the manifest.json to understand the permissions requested, including access to cookies, tabs, or web requests.
- Analyze the extension's JavaScript files for malicious functionality such as cookie exfiltration, form interception, or communication with external servers.
- Review the process.parent.executable to understand how the browser was launched with the malicious extension and trace back to the initial execution vector.
- Check for network connections made by the browser process to identify potential data exfiltration endpoints.
- Review browser profile data for evidence of credential theft or session hijacking.
- Search for the same extension path across other systems to identify potential lateral movement or widespread deployment.

### False positive analysis

- Cypress and other automated testing frameworks load extensions for browser automation. These are already excluded in the query.
- ChromeDriver used for Selenium testing loads extensions programmatically. These paths are excluded in the query.
- Developer debugging may require manual extension loading during active development. Verify with development teams if such activities are expected.
- Enterprise browser customization may deploy internal extensions via command line. Review with IT operations to document approved extensions.

### Response and remediation

- Immediately terminate the browser process to stop any ongoing malicious activity such as cookie theft or session hijacking.
- Remove the malicious extension directory from the filesystem to prevent future loading.
- Clear browser session data including cookies, cached credentials, and saved passwords for the affected browser profile.
- Review and revoke any sessions for sensitive web applications that were accessed while the extension was loaded.
- Investigate how the malicious extension was deployed and remediate the initial access vector.
- Block the malicious extension path or hash in endpoint security policies to prevent reloading.
- Reset passwords for web accounts that may have been compromised through the malicious extension.
- Check browser sync settings to ensure the malicious extension doesn't propagate to other devices.

