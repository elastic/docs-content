---
navigation_title: In ECH or ECE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-ip.html
applies_to:
  deployment:
    ess: ga
    ece: ga
products:
  - id: cloud-enterprise
  - id: cloud-hosted
---

# Manage IP traffic filters in ECH or ECE

Traffic filtering, by IP address or CIDR block, is one of the security layers available in {{ece}} and {{ech}}. It allows you to limit how your deployments can be accessed.

There are types of filters are available for filtering by IP address or CIDR block:

* **Ingress or inbound IP filters**: These restrict access to your deployments from a set of IP addresses or CIDR blocks. These filters are available through the UI.
* **Egress or outbound IP filters** (ECH only): These restrict the set of IP addresses or CIDR blocks accessible from your deployment. These might be used to restrict access to a certain region or service. This feature is in beta and is currently only available through the [Traffic Filtering API](/deploy-manage/security/ec-traffic-filtering-through-the-api.md).

Follow the step described here to set up ingress or inbound IP filters through the {{ecloud}} Console or Cloud UI.

To learn how traffic filter rules work together, refer to [traffic filter rules](/deploy-manage/security/traffic-filtering.md#traffic-filter-rules).

To learn how to manage IP traffic filters using the Traffic Filtering API, refer to [](/deploy-manage/security/ec-traffic-filtering-through-the-api.md).

:::{note}
To learn how to create IP traffic filters for self-managed clusters or {{eck}} deployments, refer to [](ip-filtering-basic.md).
:::

## Prerequisites
```{applies_to}
deployment:
  ece:
```

On {{ece}}, make sure your [load balancer](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) handles the `X-Forwarded-For` header appropriately for HTTP requests to prevent IP address spoofing. Make sure the proxy protocol v2 is enabled for HTTP and transport protocols (9243 and 9343).

This step is not required in {{ech}}.

## Apply an IP filter to a deployment

To apply an IP filter to a deployment, you must first create a rule set at the organization or platform level, and then apply the rule set to your deployment.

### Step 1: Create an IP filter rule set

You can combine any rules into a set, so we recommend that you group rules according to what they allow, and make sure to label them accordingly. Since multiple sets can be applied to a deployment, you can be as granular in your sets as you feel is necessary.

To create a rule set:

1. Navigate to the traffic filters list:

    ::::{tab-set}
    :group: ech-ece

    :::{tab-item} {{ech}}
    :sync: ech
    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Find your deployment on the home page and select **Manage**, or select your deployment from the **Hosted deployments** page.
    3. From the lower navigation menu, select **Traffic filters**.
    :::
    :::{tab-item} {{ece}}
    :sync: ece
    1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    2. From the **Platform** menu, select **Security**.
    :::
    ::::

2. Select **Create filter**.
3. Select **IP filtering rule set**.
4. Create your rule set, providing a meaningful name and description.
5. Select the region for the rule set.
6. Select if this rule set should be automatically attached to new deployments.

    ::::{note}
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

7.  Add one or more rules using IPv4, or a range of addresses with CIDR.

    ::::{note}
    DNS names are not supported in rules.
    ::::

### Step 2: Associate an IP filter rule set with your deployment

After you’ve created the rule set, you’ll need to associate IP filter rules with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters**, select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.

At this point, the traffic filter is active. You can remove or edit it at any time.

## Remove an IP filter rule set association from your deployment [remove-filter-deployment]

If you want to remove any traffic restrictions from a deployment or delete a rule set, you’ll need to remove any rule set associations first. To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.

## Edit an IP filter rule set

You can edit a rule set name or change the allowed traffic sources using IPv4, or a range of addresses with CIDR.

1. Navigate to the traffic filters list:

    ::::{tab-set}
    :group: ech-ece

    :::{tab-item} {{ech}}
    :sync: ech
    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Find your deployment on the home page and select **Manage**, or select your deployment from the **Hosted deployments** page.
    3. From the lower navigation menu, select **Traffic filters**.
    :::
    :::{tab-item} {{ece}}
    :sync: ece
    1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    2. From the **Platform** menu, select **Security**.
    :::
    ::::

2. Find the rule set you want to edit.
5. Select the **Edit** icon.


## Delete an IP filter rule set

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](#remove-filter-deployment).
1. Navigate to the traffic filters list:

    ::::{tab-set}
    :group: ech-ece

    :::{tab-item} {{ech}}
    :sync: ech
    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Find your deployment on the home page and select **Manage**, or select your deployment from the **Hosted deployments** page.
    3. From the lower navigation menu, select **Traffic filters**.
    :::
    :::{tab-item} {{ece}}
    :sync: ece
    1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
    2. From the **Platform** menu, select **Security**.
    :::
    ::::

3. Find the rule set you want to delete.
4. Select the **Delete** icon. The icon is inactive if there are deployments assigned to the rule set.