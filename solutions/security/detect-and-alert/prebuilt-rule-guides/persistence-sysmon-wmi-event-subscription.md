---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious WMI Event Subscription Created" prebuilt detection rule.
---

# Suspicious WMI Event Subscription Created

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious WMI Event Subscription Created

Windows Management Instrumentation (WMI) is a powerful framework for managing data and operations on Windows systems. It allows for event subscriptions that can trigger actions based on system events. Adversaries exploit this for persistence by creating event subscriptions that execute malicious scripts or commands. The detection rule identifies such abuse by monitoring specific event codes and API calls related to the creation of suspicious WMI event consumers, flagging potential threats.

### Possible investigation steps

- Review the event logs for event code 21 in the windows.sysmon_operational dataset to identify the specific WMI event subscription created, focusing on the winlog.event_data.Operation and winlog.event_data.Consumer fields.
- Examine the process details associated with the IWbemServices::PutInstance API call in the endpoint.events.api dataset, particularly the process.Ext.api.parameters.consumer_type, to determine the nature of the consumer created.
- Investigate the source and context of the command or script associated with the CommandLineEventConsumer or ActiveScriptEventConsumer to assess its legitimacy and potential malicious intent.
- Check for any related processes or activities around the time of the event to identify potential lateral movement or further persistence mechanisms.
- Correlate the findings with other security alerts or logs to determine if this event is part of a broader attack pattern or campaign.

### False positive analysis

- Legitimate administrative scripts or tools may create WMI event subscriptions for system monitoring or automation. Review the source and context of the event to determine if it aligns with known administrative activities.
- Software installations or updates might use WMI event subscriptions as part of their setup or configuration processes. Verify if the event coincides with recent software changes and consider excluding these specific events if they are routine.
- Security software or management tools often use WMI for legitimate purposes. Identify and document these tools in your environment, and create exceptions for their known behaviors to reduce noise.
- Scheduled tasks or system maintenance scripts may trigger similar events. Cross-reference with scheduled task logs or maintenance windows to confirm if these are expected activities.
- Custom scripts developed in-house for system management might inadvertently match the detection criteria. Ensure these scripts are documented and consider excluding their specific signatures from the rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes associated with the WMI event subscription, specifically those linked to CommandLineEventConsumer or ActiveScriptEventConsumer.
- Remove the malicious WMI event subscription by using WMI management tools or scripts to delete the identified event consumer.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional threats.
- Review and reset any compromised credentials, especially if SYSTEM privileges were potentially accessed or escalated.
- Monitor the network for any signs of similar activity or attempts to recreate the WMI event subscription, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
