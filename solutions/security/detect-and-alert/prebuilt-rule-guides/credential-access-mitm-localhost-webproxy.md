---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "WebProxy Settings Modification" prebuilt detection rule.
---

# WebProxy Settings Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating WebProxy Settings Modification

Web proxy settings in macOS manage how web traffic is routed, often used to enhance security or manage network traffic. Adversaries may exploit these settings to redirect or intercept web traffic, potentially capturing sensitive data like credentials. The detection rule identifies suspicious use of the `networksetup` command to alter proxy settings, excluding known legitimate applications, thus highlighting potential unauthorized modifications indicative of malicious activity.

### Possible investigation steps

- Review the process details to confirm the use of the networksetup command with arguments like -setwebproxy, -setsecurewebproxy, or -setautoproxyurl, which indicate an attempt to modify web proxy settings.
- Check the parent process information to ensure it is not one of the known legitimate applications such as /Library/PrivilegedHelperTools/com.80pct.FreedomHelper or /Applications/Fiddler Everywhere.app/Contents/Resources/app/out/WebServer/Fiddler.WebUi.
- Investigate the user account associated with the process to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Examine recent network traffic logs for unusual patterns or connections that could suggest traffic redirection or interception.
- Look for any additional alerts or logs related to the same host or user that might indicate a broader pattern of suspicious activity.
- Assess the system for any signs of compromise or unauthorized access, such as unexpected user accounts or changes to system configurations.

### False positive analysis

- Legitimate applications like FreedomHelper, Fiddler Everywhere, and xpcproxy may trigger the rule when they modify proxy settings. To prevent these from being flagged, ensure they are included in the exclusion list of known applications.
- Network management tools such as Proxyman and Incoggo might also be detected. Add these to the exclusion list to avoid unnecessary alerts.
- Regular system updates or configurations by IT administrators can sometimes involve proxy setting changes. Coordinate with IT to identify these activities and consider adding them to the exclusion criteria if they are routine and verified as safe.
- Automated scripts or maintenance tasks that adjust proxy settings for legitimate reasons should be reviewed and, if deemed non-threatening, excluded from detection to reduce false positives.
- Monitor for any new applications or processes that may need to be added to the exclusion list as part of ongoing security management to ensure the rule remains effective without generating excessive false alerts.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes related to the `networksetup` command that are not associated with known legitimate applications.
- Review and reset the web proxy settings on the affected device to their default or intended configuration to ensure no malicious redirection is in place.
- Conduct a thorough scan of the affected system using updated security tools to identify and remove any malware or unauthorized software that may have been installed.
- Analyze logs and network traffic to identify any data that may have been intercepted or exfiltrated, focusing on sensitive information such as credentials.
- Escalate the incident to the security operations team for further investigation and to determine if other systems may be affected.
- Implement enhanced monitoring and alerting for similar activities across the network to detect and respond to future attempts promptly.
