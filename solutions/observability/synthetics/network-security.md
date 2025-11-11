---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-traffic-filters.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Use Synthetics with network security

If you are setting up Synthetics for a deployment configured with [network security](/deploy-manage/security/network-security.md), specifically IP filters or VCP filters, none of your results will be visible in the {{synthetics-app}} until permission to write the results to {{es}} is explicitly granted.

If you don’t configure additional IP filters, the tests will run, but in the UI it will appear like they are not running because the results cannot be written back to {{es}}.

## Obtain the IP address [_obtain_the_ip_address]

The IP address or CIDR block of the hosts running the tests need to be configured in your [IP filters](/deploy-manage/security/ip-filtering.md) to allow inbound connection into your {{es}} instance to store the results.

The IP addresses to be used depend on where the monitors are running, either on Elastic’s global managed testing infrastructure or {{private-location}}s.

### Elastic’s global managed testing infrastructure [_elastics_global_managed_testing_infrastructure]

If you’re running tests on Elastic’s global managed testing infrastructure, you can find the relevant IP CIDR block (a single address or /32 block for each region) in  [this list of egress IPs](https://manifest.synthetics.elastic-cloud.com/v1/ip-ranges.json). This list is a JSON object that contains each region in Elastic’s global managed testing infrastructure and the address that outbound connections will be made from. These will be the connections into your {{es}} cluster.

For example, the `Europe - United Kingdom` region has the following entry:

```json
"europe-west2-a": {
   "ip_prefix": ["34.89.88.187/32"],
   "name": "Europe - United Kingdom"
}
```

To run tests from the `Europe - United Kingdom` region, you need to enable access from the `34.89.88.187/32` CIDR block.

::::{note}
Note that as regions are added, this list will change. Similarly existing region addresses are subject to change.

::::

### {{private-location}}s [_private_locations]

If you’re running tests from [{{private-location}}s](/solutions/observability/synthetics/monitor-resources-on-private-networks.md), you will have the {{agent}} installed on host machines that run the tests. You need to obtain the address ranges for these machines. This needs to be the IP address that the host is making the connection from into the {{es}} cluster. This *might not* be the IP address bound to the network interface of the host machine, but the proxy or other address based on your network configuration.

## Add the IP filter [_add_the_ip_filter]

Once you know the CIDR blocks for your testing sources, add them to your {{es}} deployment. Find detailed instructions in the [](/deploy-manage/security/ip-filtering.md) docs.

For example, if you had a {{private-location}} running with a public CIDR block of `1.2.3.4/32` and were running tests from the `Europe - United Kingdom` region, you would first create an IP filter with the following sources:

* `1.2.3.4/32`
* `34.89.99.187/32`

In ECH, ECE, and {{serverless-short}}, after the IP filter has been created, it needs to be associated with the deployment from which you’re managing monitors from (the deployment containing the {{es}} cluster where your results need to go).
