---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Zoom Meeting with no Passcode" prebuilt detection rule.
---

# Zoom Meeting with no Passcode

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Zoom Meeting with no Passcode

Zoom meetings without passcodes are vulnerable to unauthorized access, known as Zoombombing, where intruders disrupt sessions with inappropriate content. Adversaries exploit this by joining unsecured meetings to cause chaos or gather sensitive information. The detection rule identifies such meetings by monitoring Zoom event logs for sessions created without a passcode, helping to mitigate potential security breaches.

### Possible investigation steps

- Review the Zoom event logs to identify the specific meeting details, including the meeting ID and the organizer's information, using the fields event.type, event.module, event.dataset, and event.action.
- Contact the meeting organizer to verify if the meeting was intentionally created without a passcode and understand the context or purpose of the meeting.
- Check for any unusual or unauthorized participants who joined the meeting by examining the participant logs associated with the meeting ID.
- Assess if any sensitive information was discussed or shared during the meeting that could have been exposed to unauthorized participants.
- Evaluate the need to implement additional security measures, such as enabling passcodes for all future meetings or using waiting rooms to control participant access.

### False positive analysis

- Internal team meetings may be scheduled without a passcode for convenience, especially if all participants are within a secure network. To handle this, create exceptions for meetings initiated by trusted internal users or within specific IP ranges.
- Recurring meetings with a consistent group of participants might not use passcodes to simplify access. Consider excluding these meetings by identifying and whitelisting their unique meeting IDs.
- Training sessions or webinars intended for a broad audience might be set up without passcodes to ease access. Implement a policy to review and approve such meetings in advance, ensuring they are legitimate and necessary.
- Meetings created by automated systems or bots for integration purposes may not require passcodes. Identify these systems and exclude their meeting creation events from triggering alerts.
- In some cases, meetings may be intentionally left without passcodes for public access, such as community events. Establish a process to verify and document these events, allowing them to be excluded from the rule.

### Response and remediation

- Immediately terminate any ongoing Zoom meetings identified without a passcode to prevent further unauthorized access or disruption.
- Notify the meeting host and relevant stakeholders about the security incident, advising them to reschedule the meeting with appropriate security measures, such as enabling a passcode or waiting room.
- Review and update Zoom account settings to enforce mandatory passcodes for all future meetings, ensuring compliance with security policies.
- Conduct a security audit of recent Zoom meetings to identify any other sessions that may have been created without a passcode and take corrective actions as necessary.
- Escalate the incident to the IT security team for further investigation and to assess any potential data breaches or information leaks resulting from the unauthorized access.
- Implement enhanced monitoring and alerting for Zoom meeting creation events to quickly detect and respond to any future instances of meetings being set up without passcodes.
- Coordinate with the communications team to prepare a response plan for any potential public relations issues arising from the incident, ensuring clear and consistent messaging.
