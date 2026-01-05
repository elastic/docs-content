---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/d4c-overview.html
applies_to:
  - stack: beta 9.3
  - serverless: beta
---

# Cloud workload protection for Kubernetes [d4c-overview]

::::{warning} 
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::

Cloud workload protection for Kubernetes uses Elastic's Defend for Containers (D4C) integration to provide cloud-native runtime protections for containerized environments by identifying and optionally blocking unexpected system behavior in Kubernetes containers.


## Use cases [d4c-use-cases] 


### Threat detection & threat hunting [_threat_detection_threat_hunting] 

D4C for Kubernetes sends system events from your containers to {{es}}. {{elastic-sec}}'s prebuilt security rules include many designed to detect malicious behavior in container runtimes. These can help you detect events that should never occur in containers, such as reverse shell executions, privilege escalation, container escape attempts, and more.


### Drift detection & prevention [_drift_detection_prevention] 

Cloud-native containers should be immutable, meaning that their file systems should not change during normal operations. By leveraging this principle, security teams can detect unusual system behavior with a high degree of accuracy — without relying on more resource-intensive techniques like memory scanning or attack signature detection. Elastic’s Drift Detection mechanism has a low rate of false positives, so you can deploy it in most environments without worrying about creating excessive alerts.


### Workload protection policies [_workload_protection_policies] 

D4C for Kubernetes uses a flexible policy language to restrict container workloads to a set of allowlisted capabilities chosen by you. When employed with Drift and Threat Detection, this can provide multiple layers of defense.


## Support matrix: [_support_matrix] 

|  | EKS 1.24-1.27 (AL2022) | GKE 1.24-1.27 (COS) |
| --- | --- | --- |
| Process event exports | ✓ | ✓ |
| Network event exports | ✓ | ✓ |
| File event exports | ✓ | ✓ |
| File blocking | ✓ | ✓ |
| Process blocking | ✓ | ✓ |
| Network blocking | ✗ | ✗ |
| Drift prevention | ✓ | ✓ |
| Mount point awareness | ✓ | ✓ |


## How D4C for Kubernetes works [_how_cwp_for_kubernetes_works] 

When you set up the D4C integration, it gets deployed by {{agent}}. Specifically, the {{agent}} is installed as a DaemonSet on your Kubernetes clusters, where it enables D4C to use eBPF Linux Security Modules ([LSM](https://docs.kernel.org/bpf/prog_lsm.md)) and tracepoint probes to record system events. Events are evaluated against LSM hook points, enabling {{agent}} to evaluate system activity against your policy before allowing it to proceed.

Your D4C integration policy determines which system behaviors (for example, process execution or file creation or deletion) will result in which actions. *Selectors* and *responses* define each policy. Selectors define the conditions which cause the associated responses to run. Responses are associated with one or more selectors, and specify one or more actions (such as `log`, `alert`, or `block`) that should occur when the conditions defined in an associated selector are met.

The default D4C policy sends data about all running processes to your {{es}} cluster. This data is used by {{elastic-sec}}'s prebuilt detection rules to detect malicious behavior in container workloads.

::::{important} 
To learn more about D4C policies, including how to create your own, refer to the [D4C policies guide](container-workload-protection-policies.md).
::::




