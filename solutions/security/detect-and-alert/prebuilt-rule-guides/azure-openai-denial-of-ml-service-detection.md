---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Denial of Azure OpenAI ML Service" prebuilt detection rule.'
---

# Potential Denial of Azure OpenAI ML Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Denial of Azure OpenAI ML Service

Azure OpenAI ML services enable scalable deployment of machine learning models, crucial for AI-driven applications. Adversaries may exploit these services by overwhelming them with excessive or malformed requests, leading to service degradation or outages. The detection rule identifies such threats by monitoring for high-frequency, large-size requests, which are indicative of potential denial-of-service attacks.

### Possible investigation steps

- Review the logs for the specific time window identified by the target_time_window field to understand the context and volume of requests.
- Identify the specific Azure resource involved using the azure.resource.name field to determine if the service is critical or sensitive.
- Examine the cloud.account.id field to ascertain if the requests are originating from a known or trusted account, or if they are potentially malicious.
- Analyze the request patterns, focusing on the avg_request_size and count fields, to determine if the requests are consistent with normal usage or indicative of a potential attack.
- Check for any recent changes or updates to the Azure OpenAI ML service configuration or deployment that might have affected its performance or security posture.
- Correlate the findings with other security logs or alerts to identify any related suspicious activities or broader attack patterns.

### False positive analysis

- High-volume legitimate usage patterns can trigger false positives, such as during scheduled batch processing or data analysis tasks. Users can mitigate this by setting exceptions for known time windows or specific resource names associated with these activities.
- Large input sizes from legitimate applications, like those processing extensive datasets or complex queries, may be misidentified as threats. Users should identify and whitelist these applications by their resource names or account IDs.
- Testing and development environments often generate high-frequency requests as part of load testing or performance tuning. Users can exclude these environments by filtering out specific resource names or account IDs associated with non-production activities.
- Automated scripts or integrations that interact with the Azure OpenAI ML service at high frequencies for valid business processes might be flagged. Users should document and exclude these scripts by identifying their unique request patterns or resource identifiers.

### Response and remediation

- Immediately throttle or block the IP addresses or accounts responsible for the high-frequency, large-size requests to prevent further service degradation.
- Notify the Azure OpenAI service administrators and relevant stakeholders about the detected potential denial-of-service attack for awareness and further action.
- Review and adjust rate limiting and request size policies on the Azure OpenAI ML service to mitigate the impact of similar attacks in the future.
- Conduct a post-incident analysis to identify any vulnerabilities or misconfigurations that allowed the attack to occur and address them promptly.
- Escalate the incident to the security operations team for further investigation and to determine if the attack is part of a larger threat campaign.
- Implement additional monitoring and alerting for unusual patterns of requests, focusing on high volume and frequency, to enhance early detection of similar threats.
- Coordinate with the cloud provider's support team to ensure any necessary infrastructure adjustments or protections are in place to prevent recurrence.
