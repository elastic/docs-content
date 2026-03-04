---
navigation_title: Tutorials
applies_to:
  deployment:
    self:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
---
# Tutorials

This section provides step-by-step instructions to deploy and protect a self-managed {{stack}}. You will learn how to move from an initial installation to a production-ready, secure configuration.

 - [Install a self-managed {{stack}}](tutorial-self-managed-install.md)

    - **Objective:** Set up a functional environment for testing or development.
    - **What you will do:** Install the components of the {{stack}}, including {{es}}, {{kib}}, {{fleet-server}}, and {{agent}} to collect system data from a host.
    - **Outcome:** A running multi-node {{es}} instance with ingested system data viewable in {{kib}}.

 - [Secure a self-managed {{stack}}](tutorial-self-managed-secure.md)

    - **Objective:** Apply security protocols to an existing installation.
    - **What you will do:** Generate SSL/TLS certificates and enable node-to-node encryption between {{es}} components.
    - **Outcome:** A hardened deployment with encrypted traffic and password authentication enabled.