---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/d4c-get-started.html
applies_to:
  - stack: beta 9.3
  - serverless: beta
---

# Get started with Defend for Containers for Kubernetes [d4c-get-started]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::

This page describes how to set up Defend for Containers (D4C) for Kubernetes.

::::{admonition} Requirements
* Kubernetes node operating systems must have Linux kernels 5.10.16 or higher.
* {{stack}} version 9.3 or higher.

::::



## Initial setup [_initial_setup]

First, you’ll need to deploy Elastic’s Defend for Containers integration to the Kubernetes clusters you wish to monitor.

1. Find **Container Workload Security** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Click **Add D4C Integration**.
2. Name the integration. The default name, which you can change, is `cloud_defend-1`.
3. Optional: make any desired changes to the integration’s policy by adjusting the **Selectors** and **Responses** sections. (For more information, refer to [Defend for Containers policy](container-workload-protection-policies.md)). You can also change these later.
4. Under **Where to add this integration**, select an existing or new agent policy.
5. Click **Save & Continue**, then **Add {{agent}} to your hosts**.
6. On the {{agent}} policy page, click **Add agent** to open the Add agent flyout.
7. In the flyout, go to step 3 (**Install {{agent}} on your host**) and select the **Kubernetes** tab.
8. Download or copy the manifest (`elastic-agent-managed-kubernetes.yml`).
9. Open the manifest using your favorite editor, and uncomment the `#capabilities` section:

    ```console
    #capabilities:
    #  add:
    #    - BPF # (since Linux 5.8) allows loading of BPF programs, create most map types, load BTF, iterate programs and maps.
    #    - PERFMON # (since Linux 5.8) allows attaching of BPF programs used for performance metrics and observability operations.
    #    - SYS_RESOURCE # Allow use of special resources or raising of resource limits. Used by 'Defend for Containers' to modify 'rlimit_memlock'
    ```

10. From the directory where you saved the manifest, run the command `kubectl apply -f elastic-agent-managed-kubernetes.yml`.
11. Wait for the **Confirm agent enrollment** dialogue to show that data has started flowing from your newly-installed agent, then click **Close**.


## Get started with threat detection [d4c-get-started-threat]

One of the [default D4C policies](container-workload-protection-policies.md#d4c-default-policies) sends process telemetry events (`fork` and `exec`) to {{es}}.

In order to detect threats using this data, you’ll need active [detection rules](../detect-and-alert.md). Elastic has prebuilt detection rules designed for this data. (You can also create your own [custom rules](../detect-and-alert/create-detection-rule.md).)

To install and enable the prebuilt rules:

1. Find **Detection rules (SIEM)** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Click **Add Elastic rules**.
2. Click the **Tags** filter next to the search bar, and search for the `Data Source: Elastic Defend for Containers` tag.
3. Select all the displayed rules, then click **Install *x* selected rule(s)**.
4. Return to the **Rules** page. Click the **Tags** filter next to the search bar, and search for the `Data Source: Elastic Defend for Containers` tag.
5. Select all the rules with the tag, and then click **Bulk actions > Enable**.


## Get started with drift detection and prevention [d4c-get-started-drift]

{{elastic-sec}} defines container drift as the creation or modification of an executable within a container. Blocking drift restricts the number of attack vectors available to bad actors by prohibiting them from using external tools.

To enable drift detection, you can use the default D4C policy:

1. Make sure the [default D4C policy](container-workload-protection-policies.md#d4c-default-policies) is active.
2. Make sure you enabled at least the "Container Workload Protection" rule, by following the steps to install prebuilt rules, above.

To enable drift prevention, create a new policy:

1. Find **Container Workload Security** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select your integration.
2. Under **Selectors**, click **Add selector > File Selector**. By default, it selects the operations `createExecutable` and `modifyExecutable`.
3. Name the selector, for example: `blockDrift`.
4. Scroll down to the **Responses** section and click **Add response > File Response**.
5. Under **Match selectors**, add the name of your new selector, for example: `blockDrift`.
6. Select the **Alert** and **Block** actions.
7. Click **Save integration**.

::::{important}
Before you enable blocking, we strongly recommend you observe a production workload that’s using the default D4C policy to ensure that the workload does not create or modify executables as part of its normal operation.
::::

## Policy validation [d4c-get-started-validation]

To ensure the stability of your production workloads, you should test policy changes before implementing them in production workloads. We also recommend you test policy changes on a simulated environment with workloads similar to production. This approach allows you to test that policy changes prevent undesirable behavior without disrupting your production workloads.