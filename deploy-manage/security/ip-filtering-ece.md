---
navigation_title: In ECE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-ip.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

# Manage IP filters in ECE

Filtering by IP address or CIDR block is one of the security layers available in {{ece}}. It allows you to limit how your deployments can be accessed.

You can only configure ingress or inbound IP filters. These restrict access to your deployments from a set of IP addresses or CIDR blocks.

Follow the steps described here to set up ingress or inbound IP filters through the Cloud UI.

To learn how IP filtering rules work together, refer to [](ece-filter-rules.md).

To learn how to manage IP filters using the Traffic Filtering API, refer to [](/deploy-manage/security/network-security-api.md).

:::{note}
To learn how to create IP filters for {{ech}} deployments or {{serverless-full}} projects, refer to [](ip-filtering-cloud.md).

To learn how to create IP filters for self-managed clusters or {{eck}} deployments, refer to [](ip-filtering-basic.md).
:::

## Prerequisites

Make sure your [load balancer](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) handles the `X-Forwarded-For` header appropriately for HTTP requests to prevent IP address spoofing. Make sure the proxy protocol v2 is enabled for HTTP and transport protocols (ports 9243 and 9343).

## Apply an IP filter to a deployment

To apply an IP filter to a deployment, you must first create a rule set at the platform level, and then apply the rule set to your deployment.

### Step 1: Create an IP filtering rule set

You can combine any rules into a set, so we recommend that you group rules according to what they allow, and make sure to label them accordingly. Since multiple sets can be applied to a deployment, you can be as granular in your sets as you feel is necessary.

To create a rule set:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Select **Create filter**.
4. Select **IP filtering rule set**.
5. Create your rule set, providing a meaningful name and description.
6. Select if this rule set should be automatically attached to new deployments.
7.  Add one or more rules using IPv4, or a range of addresses with CIDR.

    ::::{note}
    DNS names are not supported in rules.
    ::::

### Step 2: Associate an IP filtering rule set with your deployment

After you’ve created the rule set, you’ll need to associate it with your deployment:

:::{include} _snippets/associate-filter-ece.md
:::

At this point, the IP filtering rule set is active. You can remove or edit it at any time.

## Remove an IP filtering rule set association from your deployment [remove-filter-deployment]

If you want to remove any traffic restrictions from a deployment or delete a rule set, you’ll need to remove any rule set associations first. To remove an association through the UI:

:::{include} _snippets/detach-filter-ece.md
:::

## Edit an IP filtering rule set

You can edit a rule set name or change the allowed traffic sources using IPv4, or a range of addresses with CIDR.

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
2. Find the rule set you want to edit.
3. Select the **Edit** {icon}`pencil` button.


## Delete an IP filtering rule set

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](#remove-filter-deployment).
2. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
3. From the **Platform** menu, select **Security**.
4. Find the rule set you want to edit.
5. Select the **Delete** {icon}`trash` button. The button is inactive if there are deployments assigned to the rule set.