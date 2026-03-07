---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubernetes Container Created with Excessive Linux Capabilities" prebuilt detection rule.'
---

# Kubernetes Container Created with Excessive Linux Capabilities

## Triage and analysis

### Investigating Kubernetes Container Created with Excessive Linux Capabilities

Linux capabilities were designed to divide root privileges into smaller units. Each capability grants a thread just enough power to perform specific privileged tasks. In Kubernetes, containers are given a set of default capabilities that can be dropped or added to at the time of creation. Added capabilities entitle containers in a pod with additional privileges that can be used to change
core processes, change network settings of a cluster, or directly access the underlying host. The following have been used in container escape techniques:

BPF - Allow creating BPF maps, loading BPF Type Format (BTF) data, retrieve JITed code of BPF programs, and more.
DAC_READ_SEARCH - Bypass file read permission checks and directory read and execute permission checks.
NET_ADMIN - Perform various network-related operations.
SYS_ADMIN - Perform a range of system administration operations.
SYS_BOOT - Use reboot(2) and kexec_load(2), reboot and load a new kernel for later execution.
SYS_MODULE - Load and unload kernel modules.
SYS_PTRACE - Trace arbitrary processes using ptrace(2).
SYS_RAWIO - Perform I/O port operations (iopl(2) and ioperm(2)).
SYSLOG - Perform privileged syslog(2) operations.

### False positive analysis

- While these capabilities are not included by default in containers, some legitimate images may need to add them. This rule leaves space for the exception of trusted container images. To add an exception, add the trusted container image name to the query field, kubernetes.audit.requestObject.spec.containers.image.

## Setup

The Kubernetes Fleet integration with Audit Logs enabled or similarly structured data is required to be compatible with this rule.
