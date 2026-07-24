---
navigation_title: Remote output and cross-cluster search
description: Configure Elastic Defend to send endpoint data to a remote Elasticsearch output and read it back using cross-cluster search.
applies_to:
  stack: ga 9.5+
  serverless: unavailable
products:
  - id: security
  - id: fleet
---

# Use {{elastic-defend}} with a remote {{es}} output [use-elastic-defend-remote-output-ccs]

By default, {{elastic-defend}} sends endpoint data to the same cluster that manages the {{agent}}. You can instead configure {{agents}} to send their data to a separate cluster using a [remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md), while still managing those {{agents}} from your main cluster. This is useful when you want to keep endpoint data separate from the deployment where you run {{fleet}} and {{elastic-sec}}.

When {{agents}} use a remote {{es}} output, their endpoint data (metadata, events, policy responses, and response action responses) is written to the remote cluster instead of the management cluster. For {{elastic-sec}} to display and act on this data, the management cluster reads it back using [{{ccs}}](/explore-analyze/cross-cluster-search.md) ({{ccs-init}}).


## How it works [how-it-works]

The setup relies on two independent links between the management cluster and the remote cluster:

* **Write path (remote {{es}} output):** {{agents}} managed by the management cluster ship their data to the remote cluster.
* **Read path ({{ccs}}):** the management cluster's {{kib}} reads that data back from the remote cluster so it can appear in {{elastic-sec}}.

{{agents}} always enroll into and are managed by the management cluster. They send their data directly to the remote cluster, but never enroll into it or receive management instructions from it.

Once configured, the following {{elastic-sec}} endpoint management features can read {{elastic-defend}} data stored on the remote cluster:

* The **Endpoints** page and endpoint details flyout
* Response actions, including response actions history and status
* Policy responses
* Automatic troubleshooting

## Before you begin [before-you-begin]

Make sure you have the following before you start:

* A management cluster running {{fleet}} and {{elastic-sec}}, and a separate remote cluster to receive endpoint data.
* Permission to use {{fleet}} in {{kib}} on the management cluster, so you can create outputs and manage {{agent}} policies.

## Set up {{elastic-defend}} with a remote {{es}} output [setup]

::::::{stepper}

:::::{step} Configure a remote {{es}} output

In the management cluster, create a [remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md) and point an {{agent}} policy at it, so that {{agents}} on that policy send their data to the remote cluster.

To confirm the output is working, go to **{{fleet}} → Settings** and check that the remote {{es}} output appears in the **Outputs** list without connection errors.
:::::

:::::{step} Add {{elastic-defend}} and enroll {{agents}}

[Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md): add the {{elastic-defend}} integration to the {{agent}} policy that uses the remote output, then enroll your {{agents}} into the management cluster. Their endpoint data now lands on the remote cluster.

To confirm enrollment, go to **{{fleet}} → Agents** and check that each {{agent}} shows a **Healthy** status.
:::::

:::::{step} Configure {{ccs}}

Configure {{ccs-init}} so the management cluster can read the endpoint data back from the remote cluster. Follow [Set up {{ccs}} to query remote data](/reference/fleet/remote-elasticsearch-output.md#set-up-ccs).
:::::

::::::

Once the remote output and {{ccs-init}} are configured, {{elastic-sec}} automatically reads {{elastic-defend}} data from the remote cluster.

## Related pages [related-pages]

* [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md)
* [Remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md)
* [{{ccs-cap}}](/explore-analyze/cross-cluster-search.md)
