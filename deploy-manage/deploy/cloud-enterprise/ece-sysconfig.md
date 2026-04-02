---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-sysconfig.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# System configuration [ece-sysconfig]

Check the following requirements before installing ECE.


## Time synchronization [ece-sysconfig-time] 

A time synchronization daemon such as NTP or Chrony must be functioning on the system to keep the time in sync. This is especially critical for virtualized and cloud-hosted machine instances.

::::{warning} 
ECE currently requires setting server hosts to UTC time. If you use non-UTC time on your hosts, some areas of the ECE UI will not function correctly.
::::



## Disabled nscd daemon [ece-sysconfig-nscd] 

On Linux systems, the [name service cache daemon (nscd)](https://linux.die.net/man/8/nscd) can prevent ECE from installing successfully. For example, it might block various networking components from functioning properly, including the container’s ability to resolve connections to its host. Before running the ECE install process this service should be disabled on your system. The nscd daemon needs to be permanently stopped, even after ECE installation.

