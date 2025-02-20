---
navigation_title: "Emergency roles token"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-troubleshooting-emergency.html
---

# Use the emergency roles token [ece-troubleshooting-emergency]

During installation, an emergency token gets generated that enables you to install Elastic Cloud Enterprise on additional hosts with all roles already assigned, except the allocator role. The emergency token can save your installation if all coordinators fail or are removed and you can no longer use the Cloud UI or the RESTful API. As part of the installation instructions, we ask you to keep this token safe.

To use the emergency token:

1. [Install Elastic Cloud Enterprise on an additional host](../../../deploy-manage/deploy/cloud-enterprise/install-ece-on-additional-hosts.md) and specify the emergency token along with the original coordinator host. For example:

    ```
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --coordinator-host 192.168.50.10 --roles-token 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyZGVlYjlkZS01MDkzLTQxNGItYmI5NS0zNmJhZTQxMWI0YzgiLCJyb2xlcyI6WyJjb29yZGluYXRvciIsInByb3h5IiwiZGlyZWN0b3IiXSwiaXNzIjoiY3VycmVudCIsInBlcnNpc3RlbnQiOnRydWV9.5tIVQxEluSjtJ7qiwE8OWzy5O4l1GJ0urTFs_l1x5bU'
    ```

2. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md) on the newly created coordinator. The URL you use is the IP address of the host that you installed Elastic Cloud Enterprise on in Step 1 (`http://10.142.0.4:12400`, for example).
3. Verify that the Cloud UI works as expected.
4. Optional: Prevent a recurrence of the issue by enabling high availability for the administration console:

    1. Repeat Step 1 to create two additional coordinators in two additional availability zones. [Examples of the installation commands](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-enterprise/ece-installation-script.md#ece-installation-script-examples) you need to run are available.
    2. [Change the configuration for the `admin-console-elasticsearch` and `logging-and-metrics` deployments](../../../deploy-manage/deploy/cloud-enterprise/working-with-deployments.md) to use three availability zones and resize the nodes to use at least 4 GB of RAM. This change makes sure that the clusters used by the administration console are highly available and provisioned sufficiently.


