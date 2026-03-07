---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Attempt to Establish VScode Remote Tunnel" prebuilt detection rule.
---

# Attempt to Establish VScode Remote Tunnel

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Attempt to Establish VScode Remote Tunnel

Visual Studio Code (VScode) offers a remote tunnel feature enabling developers to connect to remote environments seamlessly. While beneficial for legitimate remote development, adversaries can exploit this to establish unauthorized access or control over systems. The detection rule identifies suspicious use of VScode's tunnel command, focusing on specific command-line arguments and process behaviors, to flag potential misuse indicative of command and control activities.

### Possible investigation steps

- Review the process details to confirm the presence of the "tunnel" argument in the command line, which indicates an attempt to establish a remote tunnel session.
- Check the parent process name to ensure it is not "Code.exe" when the process name is "code-tunnel.exe" with the "status" argument, as this is an exception in the rule.
- Investigate the origin of the process by examining the user account and machine from which the process was initiated to determine if it aligns with expected usage patterns.
- Analyze network logs to identify any unusual or unauthorized connections to GitHub or remote VScode instances that may suggest malicious activity.
- Correlate the event with other security alerts or logs from data sources like Elastic Endgame, Sysmon, or Microsoft Defender for Endpoint to gather additional context on the activity.
- Assess the risk and impact by determining if the system or user account has been involved in previous suspicious activities or if there are any indicators of compromise.

### False positive analysis

- Legitimate remote development activities using VScode's tunnel feature may trigger the rule. Users can create exceptions for known developer machines or specific user accounts frequently using this feature for authorized purposes.
- Automated scripts or deployment tools that utilize VScode's remote tunnel for legitimate operations might be flagged. Consider excluding these processes by identifying their unique command-line arguments or parent processes.
- Scheduled tasks or system maintenance activities that involve VScode's remote capabilities could be misidentified as threats. Review and whitelist these tasks by their specific execution times or associated service accounts.
- Development environments that frequently update or test VScode extensions might inadvertently match the rule's criteria. Exclude these environments by setting up exceptions based on their network segments or IP addresses.
- Training or demonstration sessions using VScode's remote features for educational purposes can be mistaken for suspicious activity. Implement exclusions for these sessions by tagging them with specific event identifiers or user roles.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious VScode processes identified by the detection rule to halt potential command and control activities.
- Conduct a thorough review of system logs and process histories to identify any additional indicators of compromise or lateral movement attempts.
- Reset credentials and access tokens associated with the affected system and any connected services to mitigate unauthorized access.
- Restore the system from a known good backup if any unauthorized changes or malware are detected.
- Implement network segmentation to limit the ability of similar threats to spread across the environment.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
