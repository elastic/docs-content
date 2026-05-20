---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Overview of Elastic's prebuilt detection rules library mapped to MITRE ATT&CK.
---

# Prebuilt rules

Elastic maintains a library of prebuilt detection rules mapped to the MITRE ATT&CK framework. Enabling prebuilt rules is the fastest path to detection coverage and the recommended starting point before building custom rules. You can browse the full [prebuilt rule catalog](detection-rules://index.md) to see what's available.

**[Prebuilt rule components](/solutions/security/detect-and-alert/prebuilt-rule-components.md)**
:   Learn how prebuilt rules are organized with tags, what data sources they need, and how to use their investigation guides.

**[Install prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md)**
:   Start here to install and enable prebuilt rules. Includes a subscription capability matrix showing which features are available at each tier.

**[Update prebuilt rules](/solutions/security/detect-and-alert/update-prebuilt-rules.md)**
:   Apply Elastic's rule updates to keep your detection coverage current. Explains how to review updates, handle modified rules, and resolve conflicts (Enterprise only).

**[Handle deprecated prebuilt rules](/solutions/security/detect-and-alert/manage-detection-rules.md#deprecated-prebuilt-rules)** {applies_to}`stack: ga 9.4+`
:   Find deprecated prebuilt rules on the {{rules-ui}} page or a rule's details page, then delete them or duplicate and delete them so they are no longer tied to the prebuilt package.

**[Prebuilt rules in air-gapped environments](/solutions/security/detect-and-alert/prebuilt-rules-airgapped.md)**
:   Install and update prebuilt rules in air-gapped environments without internet access.

**[Customize prebuilt rules](/solutions/security/detect-and-alert/customize-prebuilt-rules.md)**
:   Adapt prebuilt rules to your environment. Edit rules directly or revert to the original Elastic version (Enterprise on {{stack}} 9.1+, or Security Analytics Complete on {{serverless-short}}), duplicate and modify copies, add exceptions, or configure actions.
