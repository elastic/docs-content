# IP traffic filters [ech-traffic-filtering-ip]

Traffic filtering, by IP address or CIDR block, is one of the security layers available in Elasticsearch Add-On for Heroku. It allows you to limit how your deployments can be accessed.

Read more about [Traffic Filtering](../../../deploy-manage/security/traffic-filtering.md) for the general concepts behind traffic filtering in Elasticsearch Add-On for Heroku.

Follow the step described here to set up ingress or inbound IP filters through the Elasticsearch Add-On for Heroku console.


## Create an IP filter rule set [ech-create-traffic-filter-ip-rule-set] 

You can combine any rules into a set, so we recommend that you group rules according to what they allow, and make sure to label them accordingly. Since multiple sets can be applied to a deployment, you can be as granular in your sets as you feel is necessary.

To create a rule set:

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Select **Create filter**.
5. Select **IP filtering rule set**.
6. Create your rule set, providing a meaningful name and description.
7. Select the region for the rule set.
8. Select if this rule set should be automatically attached to new deployments.

    ::::{note} 
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

9. Add one or more rules using IPv4, or a range of addresses with CIDR.

    ::::{note} 
    DNS names are not supported in rules.
    ::::


The next step is to [associate one or more rule-sets](../../../deploy-manage/security/ip-traffic-filtering.md#ech-associate-traffic-filter-ip-rule-set) with your deployments.


## Associate an IP filter rule set with your deployment [ech-associate-traffic-filter-ip-rule-set] 

After you’ve created the rule set, you’ll need to associate IP filter rules with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.


## Remove an IP filter rule set association from your deployment [ech-remove-association-traffic-filter-ip-rule-set] 

If you want to remove any traffic restrictions from a deployment or delete a rule set, you’ll need to remove any rule set associations first. To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.


## Edit an IP filter rule set [ech-edit-traffic-filter-ip-rule-set] 

You can edit a rule set name or change the allowed traffic sources using IPv4, or a range of addresses with CIDR.

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Find the rule set you want to edit.
5. Select the **Edit** icon.


## Delete an IP filter rule set [ech-delete-traffic-filter-ip-rule-set] 

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](../../../deploy-manage/security/ip-traffic-filtering.md#ech-remove-association-traffic-filter-ip-rule-set).
2. Under the **Features** tab, open the **Traffic filters** page.
3. Find the rule set you want to edit.
4. Select the **Delete** icon. The icon is inactive if there are deployments assigned to the rule set.

