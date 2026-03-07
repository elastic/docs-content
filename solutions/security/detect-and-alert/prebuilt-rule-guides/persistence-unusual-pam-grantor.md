---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Authentication via Unusual PAM Grantor" prebuilt detection rule.
---

# Authentication via Unusual PAM Grantor

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Authentication via Unusual PAM Grantor

Pluggable Authentication Modules (PAM) are integral to Linux systems, managing authentication tasks. Adversaries may exploit uncommon PAM grantors to escalate privileges or maintain persistence by altering default configurations. The detection rule identifies successful authentications using atypical PAM grantors, signaling potential unauthorized access or configuration tampering.

### Possible investigation steps

- Review the specific PAM grantor involved in the authentication event to determine if it is known or expected in your environment.
- Check the user account associated with the authentication event for any signs of compromise or unusual activity, such as recent changes in permissions or unexpected login times.
- Investigate the source IP address and hostname of the authentication event to verify if it is a recognized and authorized system within your network.
- Examine recent changes to the PAM configuration files on the affected host to identify any unauthorized modifications or additions.
- Correlate this event with other security alerts or logs from the same host or user to identify potential patterns of malicious activity.
- Consult with system administrators or relevant personnel to confirm if the use of the unusual PAM grantor was part of a legitimate change or update.

### False positive analysis

- Custom PAM modules: Organizations may use custom PAM modules for specific applications or security policies. Review these modules to ensure they are legitimate and add them to an exception list if they are frequently triggering alerts.
- Administrative scripts: Some administrative scripts might use non-standard PAM grantors for automation purposes. Verify the scripts' legitimacy and consider excluding them from the rule if they are part of routine operations.
- Third-party software: Certain third-party software may install or use uncommon PAM grantors as part of their authentication process. Validate the software's authenticity and add its grantors to an exception list if they are known to be safe.
- Development environments: In development or testing environments, developers might experiment with different PAM configurations. Ensure these environments are properly isolated and consider excluding them from the rule to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Review the PAM configuration files on the affected system to identify and revert any unauthorized changes to the grantors. Ensure only legitimate PAM modules are in use.
- Terminate any suspicious or unauthorized processes that may have been initiated by the attacker to maintain persistence or escalate privileges.
- Conduct a thorough review of user accounts and privileges on the affected system to identify any unauthorized changes or newly created accounts. Revoke any unauthorized access.
- Restore the affected system from a known good backup if unauthorized changes cannot be easily reverted or if the system's integrity is in question.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for PAM-related activities across the network to detect similar threats in the future, ensuring that alerts are promptly reviewed and acted upon.
