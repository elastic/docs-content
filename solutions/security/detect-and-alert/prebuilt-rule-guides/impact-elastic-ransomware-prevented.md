---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Ransomware - Prevented - Elastic Defend" prebuilt detection rule.
---

# Ransomware - Prevented - Elastic Defend

## Triage and analysis

### Investigating Ransomware - Prevented - Elastic Defend

Ransomware protection adds a dedicated layer of detection and prevention against ransomware attacks. Our Ransomware protection consists of 3 subtypes: `behavioral`, `canary files`, and `MBR`. Our behavioral ransomware protection monitors the low level file system activity of all processes on the system to identify generic file encryption techniques. We include signals such as file header information, entropy calculations, known and suspicious extensions, and more to make verdicts. Canary files serve as a high confidence short-cut to other behavior techniques. Our endpoint places hidden files in select directories on the system and will trigger on any process attempting to tamper with the files. Finally, we protect the Master Boot Record (MBR) with our kernel minifilter driver to prevent this type of ransomware attack.

Generally, our ransomware protection is tuned to have extremely low false positives rates. We understand how alarming and disruptive ransomware false positives can be which has factored into its design goals. More likely than not, if this protection fires, it is a true positive. However, certain categories of software do behave similarly to ransomware from the perspective of this protection. That includes installers and backup software, which can make a large number of modifications to documents (especially during a restore operation). Further, encryption or system utilities which modify the system’s MBR may also trigger our MBR protection.

### Possible investigation steps

- The `Ransomware.files` field provides details about files modification (paths, entropy, extension and file headers).
- Investigate the metadata and the activity of the process or processes that triggered the alert.
- Assess whether this activity is prevalent in your environment by looking for similar occurrences across hosts.
- Some Ransomware attacks tend to execute the operation on multiple hosts at the same time for maximum impact.
- Verify the activity of the `user.name` associated with the alert (local or remote actity, privileged or standard user).
- Quickly identifying the compromised credentials is critical to remediate Ransomware attacks.
- Verify if there are any other alert types (Behavior or Memory Threat) associated with the same host or user or process within the same time.

### False positive analysis

- Installers and backup software, which can make a large number of modifications to documents (especially during a restore operation).
- Encryption or system utilities which modify the system’s MBR may also trigger our MBR protection.

### Response and Remediation

- Immediate Isolation and Containment: Quickly disconnect affected systems from the network, including both wired and wireless connections, to prevent the ransomware from spreading. This includes disabling network cards and removing network cables if necessary, while keeping the systems powered on for forensic purposes.
- Activate Incident Response Team and Plan: Assemble your incident response team and implement your incident response plan. Contact necessary stakeholders including IT security, legal counsel, and executive management. Document all actions taken from the moment of detection.
Initial Assessment and Evidence Preservation: Identify the scope of the infection and the type of ransomware.
- Take screenshots of ransom messages and create disk images of affected systems. Record all observable indicators of compromise (IOCs) before any remediation begins.
- Business Impact Analysis: Evaluate which critical business operations are affected and establish priority systems for recovery. Determine regulatory reporting requirements based on the type of data potentially compromised.
- Secure Backup Verification: Identify and verify the integrity of your latest clean backups. Check backup systems for potential compromise and ensure they were disconnected during the attack to prevent encryption of backup data.
- System Recovery Preparation: Build a clean environment for recovery operations, including secured networks and validated clean systems. Prepare tools and resources needed for system restoration.
- Malware Eradication: Remove the ransomware from infected systems using appropriate security tools. This may involve complete system rebuilds from known clean sources rather than attempting to clean infected systems.
- Data Restoration: Begin restoring systems from verified clean backups, starting with the most critical business operations. Implement additional security controls and monitoring during the restoration process.
- Security Posture Strengthening: Update all security systems including firewalls, antivirus, and endpoint protection. Reset all credentials across the organization and implement additional access controls like multi-factor authentication where needed.
- Post-Incident Activities: Conduct a detailed post-incident analysis to identify how the ransomware entered the environment. Update security policies and incident response plans based on lessons learned, and provide additional security awareness training to staff.

