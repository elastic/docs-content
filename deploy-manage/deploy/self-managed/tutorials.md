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

    - **Objective:** Set up a functional, secure-by-default environment for testing or development.
    - **What you will do:** Install the components of the {{stack}}, including {{es}}, {{kib}}, {{fleet-server}}, and {{agent}}, using automatic security setup for {{es}}, enrolling {{kib}}, and using the Quick Start flow for {{fleet-server}} and {{agent}} to collect system data from a host.
    - **Outcome:** A running multi-node {{es}} deployment with {{kib}}, {{fleet-server}}, and {{agent}} installed and configured, and system data viewable in {{kib}}.
    - **Security overview:** {{es}} uses [automatic security setup](/deploy-manage/security/self-auto-setup.md), generating TLS certificates for the transport and HTTP layers. {{kib}} is enrolled with {{es}}, but browser-to-{{kib}} HTTPS is not configured. {{fleet-server}} uses the Quick Start self-signed certificate flow for {{agent}} enrollment.

 - [Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md)

    - **Objective:** Customize the certificate model for an existing installation.
    - **What you will do:** Replace or adjust the default certificate setup for {{es}}, {{kib}}, {{fleet-server}}, and {{agent}}.
    - **Outcome:** A deployment that uses the certificate authorities and TLS configuration required by your environment.
    - **Security overview:** Create a new CA and certificates for the {{es}} transport layer, create new certificates for the {{es}} HTTP layer, generate and configure certificates for browser-to-{{kib}} HTTPS, and configure certificates for {{fleet-server}}.