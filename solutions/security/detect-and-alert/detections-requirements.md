---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detections-permissions-section.html
  - https://www.elastic.co/guide/en/serverless/current/security-detections-requirements.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Learn how to configure and enable the Detections feature in Elastic Security for your deployment type.
---

# Turn on detections [enable-detections-ui]

Before you can create rules, manage alerts, or use other [detection capabilities](/solutions/security/detect-and-alert.md), you need to enable the Detections feature. This page walks you through the required setup for your deployment type and shows you how to turn on detections.

:::::::{tab-set}

::::::{tab-item} {{serverless-full}}

The detections feature is turned on by default in {{serverless-short}} projects. Your access level depends on your assigned role.

| Access level | Roles |
| --- | --- |
| Full access (manage rules, alerts, exceptions) | Editor, SOC Manager, Detections Eng, Tier 3 Analyst, Platform Engineer |
| Read-only (only view rules and alerts) | Viewer, Tier 1 Analyst, Tier 2 Analyst |

Refer to [Predefined roles](/solutions/security/detect-and-alert/detections-privileges.md#predefined-serverless-roles-detections) for a list of predefined roles with detection privileges.

::::::

::::::{tab-item} {{ecloud}}

The detection engine initializes automatically when a user with [sufficient privileges](/solutions/security/detect-and-alert/detections-privileges.md) visits the **Rules** page. To open the page, find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

No additional configuration is required.

::::::

::::::{tab-item} Self-managed {{stack}}

Complete these steps to turn on the detections feature in your space.

:::::{stepper}

::::{step} Enable HTTPS
Configure HTTPS for communication between [{{es}} and {{kib}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).
::::

::::{step} Configure {{kib}}
In your [`kibana.yml`](/deploy-manage/stack-settings.md) file, add an encryption key with at least 32 alphanumeric characters:

```yaml
xpack.encryptedSavedObjects.encryptionKey: 'fhjskloppd678ehkdfdlliverpoolfcr'
```

:::{important}
After changing the encryption key and restarting {{kib}}, you must restart all detection rules.
:::
::::

::::{step} Configure {{es}}
In your [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) file:

1. Set `xpack.security.enabled` to `true`. Refer to [General security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) for more information.

2. Ensure `search.allow_expensive_queries` is `true` (the default). If it's set to `false`, remove that setting.
::::

::::{step} Enable detections
1. Go to the **Rules** page. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. The detection engine initializes when a user with [sufficient privileges](/solutions/security/detect-and-alert/detections-privileges.md) visits the page.

::::{note}
To enable detections in multiple spaces, visit the **Rules** page in each space.
::::

::::

:::::

::::::

:::::::

## Start detecting threats

With detections enabled, you're ready to create rules and start responding to threats. Do the following:

- **Add detection rules**
   - [Install Elastic prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md): Get started quickly with hundreds of rules that detect common threats
   - [Create custom rules](/solutions/security/detect-and-alert/create-detection-rule.md): Write rules tailored to your environment
   - [Configure {{anomaly-detect}} rules](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md): Use {{ml}} to detect unusual behavior

- **Respond to and manage alerts**
   - [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md): Triage, investigate, and resolve alerts
   - [Set up alert notifications](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications): Send alerts to external systems like Slack, email, or ticketing tools
   - [Tune rules to reduce noise](/solutions/security/detect-and-alert/tune-detection-rules.md): Add exceptions and adjust rules to minimize false positives

::::{tip}
For a complete walkthrough, check out [Quickstart: Detect and respond to threats with SIEM](/solutions/security/get-started/get-started-detect-with-siem.md).
::::