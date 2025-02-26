---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-settings-changing-outputs.html
---

# Considerations when changing outputs [fleet-settings-changing-outputs]

{{fleet}} provides the capability to update your [output settings](/reference/ingestion-tools/fleet/fleet-settings.md#output-settings) to add new outputs, and then to assign those new outputs to an {{agent}} policy. However, changing outputs should be done with caution.

When you change the output configuration within a policy applied to one or more agents, there’s a high likelihood of those agents re-ingesting previously processed logs:

* Changing the output will cause the agents to remove and recreate all existing integrations associated with the new output, which as a result of the change receives a new UUID.
* As a consequence of the newly generated output UUID, the agents will retransmit all events and logs they have been configured to collect, since the data registry will be re-created.

In cases when an update to an output is required, it’s generally preferable to update your existing output rather than create a new one.

An example of an update being needed would be when switching from a static IP address to a global load balancer (where both endpoints point to the same underlying cluster). In this type of situation, changing to a new output would result in data being re-collected, while updating the existing output would not.

