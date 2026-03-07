---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Python Site or User Customize File Creation" prebuilt detection rule.'
---

# Python Site or User Customize File Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Python Site or User Customize File Creation

Python's `sitecustomize.py` and `usercustomize.py` are scripts that execute automatically when Python starts, allowing for environment-specific customizations. Adversaries can exploit these files to maintain persistence by injecting malicious code. The detection rule monitors file creation and modification in key directories, excluding benign processes, to identify unauthorized changes indicative of potential backdooring or persistence attempts.

### Possible investigation steps

- Review the file path where the creation or modification was detected to determine if it is a system-wide, user-specific, or virtual environment location, as specified in the query.
- Identify the process executable responsible for the file creation or modification and verify if it is listed in the exclusion list of benign processes. If not, investigate the process for potential malicious activity.
- Check the timestamp of the file creation or modification event to correlate with any other suspicious activities or alerts on the system around the same time.
- Examine the contents of the sitecustomize.py or usercustomize.py file for any unauthorized or suspicious code that could indicate persistence mechanisms or backdooring attempts.
- Investigate the user account associated with the file creation or modification event to determine if the activity aligns with expected behavior or if it suggests potential compromise.
- Review system logs and other security alerts for additional context or indicators of compromise related to the detected event.

### False positive analysis

- Package managers like pip and poetry can trigger false positives when they create or modify sitecustomize.py or usercustomize.py during package installations or updates. To handle this, ensure these processes are included in the exclusion list within the detection rule.
- System updates or software installations that involve Python libraries might also lead to false positives. Regularly review and update the exclusion list to include known benign processes such as pacman or restic that are part of routine system maintenance.
- Custom scripts or automation tools that use Python to manage environments could inadvertently modify these files. Identify and exclude these specific scripts or tools if they are verified as non-malicious.
- Virtual environments often involve the creation of sitecustomize.py for environment-specific configurations. Consider excluding the virtual environment's Python executables if they are part of a controlled and secure development process.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or spread of malicious code.
- Review the contents of the `sitecustomize.py` and `usercustomize.py` files for any unauthorized or suspicious code. Remove any malicious code identified.
- Restore the affected files from a known good backup if available, ensuring that the restored files are free from unauthorized modifications.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or persistence mechanisms.
- Monitor the system and network for any signs of continued unauthorized access or attempts to modify the `sitecustomize.py` and `usercustomize.py` files.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for changes to critical Python directories and files to enhance detection of similar threats in the future.
