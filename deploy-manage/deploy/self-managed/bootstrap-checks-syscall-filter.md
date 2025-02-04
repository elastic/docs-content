---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-syscall-filter.html
---

# System call filter check [bootstrap-checks-syscall-filter]

Elasticsearch installs system call filters of various flavors depending on the operating system (e.g., seccomp on Linux). These system call filters are installed to prevent the ability to execute system calls related to forking as a defense mechanism against arbitrary code execution attacks on Elasticsearch. The system call filter check ensures that if system call filters are enabled, then they were successfully installed. To pass the system call filter check you must fix any configuration errors on your system that prevented system call filters from installing (check your logs).

