---
navigation_title: Self-hosted infrastructure
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---



# Run Universal Profiling on self-hosted Elastic stack [profiling-self-managed]


::::{important}
To run Universal Profiling on self-hosted Elastic stack, you need an [appropriate license](https://www.elastic.co/subscriptions).
::::


Here you’ll find information on running Universal Profiling when hosting the Elastic stack on your own infrastructure.

Universal Profiling consists of a client part (the Universal Profiling Agent) and a server part (the backend). This documentation focuses on the server part.


## Prerequisites [profiling-self-managed-supported-platforms]

* Elastic stack: minimum version 8.12.0, on any Linux distribution (x86_64 or ARM64 architectures), with a Kernel 4.x or higher.
* [ECE](https://www.elastic.co/ece): minimum version 3.7.0, using the 8.12.0 stackpack or higher.
* Kubernetes: version 1.22+, using Helm charts.

::::{note}
For Elastic Cloud on Kubernetes (ECK), the Universal Profiling backend can be installed using helm charts in standalone mode. Once installed, you can connect the profiling backend to an existing ECK-managed stack. Currently, we do not have Profiling Operators and the CRDs necessary for running the Profiling backend natively in ECK.
::::



### Supported platforms [profiling-self-managed-backend-support-matrix]

The following platforms were tested and successfully ran the Universal Profiling backend.

| Platform | OS | Details |
| --- | --- | --- |
| Linux x86_64, ARM64 | Ubuntu 20.04 LTS | Tested DEB package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | Ubuntu 22.04 LTS | Tested DEB package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | Debian Bullseye | Tested DEB package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | Debian Bookworm | Tested DEB package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | Fedora 37 | Tested YUM package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | Fedora 38 | Tested YUM package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | RHEL 9.3 | Tested YUM package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | RHEL 8.9 | Tested YUM package from the repository, Docker, and Binary |
| Linux x86_64, ARM64 | openSUSE Leap | Tested Docker and Binary |
| Linux x86_64, ARM64 | SUSE Linux Enterprise 15 | Tested Docker and Binary |
| Kubernetes 1.25, 1.26, 1.27 | Linux x86_64/ARM64 | Tested Helm charts |


## Architecture overview [profiling-self-managed-architecture-overview]

The backend is made up of two services: the collector and the symbolizer.

* The collector receives profiling data from the Universal Profiling Agents and sends it to {{es}}. It listens on an HTTP server and serves a gRPC endpoint.
* The symbolizer processes debug symbols that are not available on the Universal Profiling Agent, and symbolizes native frames from OS packages. It also listens on an HTTP server and serves an endpoint to upload private debug symbols. Refer to [Adding symbols](add-symbols-for-native-frames.md) for more information on the importance of adding symbols.

:::{image} /solutions/images/observability-profiling-self-managed-ingestion-architecture.png
:alt: profiling self managed ingestion architecture
:screenshot:
:::




