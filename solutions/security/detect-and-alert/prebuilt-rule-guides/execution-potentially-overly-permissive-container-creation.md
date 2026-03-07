---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Privileged Docker Container Creation" prebuilt detection rule.
---

# Privileged Docker Container Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privileged Docker Container Creation

Docker containers are lightweight, portable units that package applications and their dependencies. The `--privileged` flag grants containers extensive host access, posing security risks. Adversaries exploit this to escalate privileges or escape containers. The detection rule identifies unusual privileged container creation by monitoring specific process actions and arguments, helping to flag potential threats early.

### Possible investigation steps

- Review the alert details to confirm the presence of the `--privileged` flag in the process arguments, as indicated by the query field `process.args:(run and --privileged)`.
- Identify the parent process of the Docker command by examining the `event.category:process` and `event.type:start` fields to determine if it originates from an unusual or unauthorized source.
- Check the user account associated with the Docker process to verify if it has legitimate access and permissions to create privileged containers.
- Investigate the timeline of events leading up to the container creation by reviewing related logs and events around the `event.action:exec` to identify any suspicious activities or patterns.
- Assess the container's configuration and running processes to determine if any unauthorized or potentially harmful applications are being executed within the container.
- Correlate the alert with other security events or alerts in the environment to identify potential indicators of compromise or broader attack patterns.

### False positive analysis

- Routine administrative tasks may trigger the rule if system administrators use the --privileged flag for legitimate container management. To handle this, identify and document these tasks, then create exceptions for known administrative processes.
- Automated deployment scripts that require elevated privileges might also cause false positives. Review these scripts and whitelist them by specifying the parent process or script name in the exclusion criteria.
- Development environments often use privileged containers for testing purposes. To reduce noise, exclude processes originating from known development machines or user accounts.
- Some monitoring or security tools may use privileged containers for legitimate purposes. Verify these tools and add them to the exception list to prevent unnecessary alerts.
- Regularly review and update the exclusion list to ensure it reflects current operational practices and does not inadvertently allow malicious activity.

### Response and remediation

- Immediately isolate the affected container to prevent further interaction with the host system. This can be done by stopping the container using `docker stop <container_id>`.

- Review and revoke any unnecessary permissions or access rights granted to the container. Ensure that the `--privileged` flag is not used unless absolutely necessary.

- Conduct a thorough investigation of the container's filesystem and running processes to identify any malicious activity or unauthorized changes. Use tools like `docker exec` to inspect the container's environment.

- Check for any signs of container escape or host compromise by reviewing system logs and monitoring for unusual activity on the host machine.

- If a compromise is confirmed, initiate a full incident response procedure, including forensic analysis and system restoration from clean backups.

- Update and patch the Docker daemon and any related software to the latest versions to mitigate known vulnerabilities that could be exploited.

- Enhance monitoring and alerting for privileged container creation by integrating additional security tools or services that provide real-time threat intelligence and anomaly detection.
