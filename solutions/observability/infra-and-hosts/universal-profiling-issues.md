---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-known-issues.html
applies_to:
  stack: 
---

# Universal Profiling issues [profiling-known-issues]

Universal Profiling has the following known issues:


## Helm chart `profiling-collector` faulty binary location [_helm_chart_profiling_collector_faulty_binary_location] 

*Affected: 8.16.0, 8.16.1, 8.16.2, 8.17.0* *Fixed in: 8.16.3+, 8.17.1+*

The installation of Universal Profiling collector using the Helm chart `profiling-collector` produces a Deployment with the wrong binary path set in `spec.template.spec.containers['pf-elastic-collector'].command`.

The correct path should be `/home/nonroot/pf-elastic-collector` while the `command` field references the deprecated path `/root/pf-elastic-collector`. This issue prevents the collector from starting and as a result, the Deployment has Pods in `CrashLoopBackoff` status.

To fix this issue, a manual edit of the Deployment manifest should be performed, removing entirely the `command` field from the `spec` section.

This can be performed by either manipulating the Deployment template emitted by Helm or by using the `kubectl edit` command.

