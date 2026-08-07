---
navigation_title: IPv6 integration on AWS
applies_to:
  deployment:
    ece: ga 4.2
products:
  - id: cloud-enterprise
---

# Troubleshoot IPv6 integration for {{ece}} on {{aws}}

This document provides troubleshooting guidance and verification commands for IPv6 integration with {{ece}} on {{aws}}, including ingress through load balancers and optional container egress.

For setup and architecture details, refer to [Setting up IPv6 for ECE on {{aws}}](/deploy-manage/deploy/cloud-enterprise/ece-ipv6-aws-setup.md).

## Scope and expected outcomes

Use this page to troubleshoot the following traffic flows:

- **IPv6 ingress for deployment traffic**: Clients to deployments through {{aws}} Network Load Balancer (NLB) and ECE proxies.
- **IPv6 ingress for admin console UI traffic**: Clients to admin console endpoints through {{aws}} Application Load Balancer (ALB).
- **IPv6 egress**: Outbound IPv6 from containers.

Success criteria:

- Ingress: dual-stack client requests over IPv4 and IPv6 reach ECE, and client metadata is preserved through Proxy Protocol v2.
- Egress: containers can resolve and reach IPv6 endpoints.

## Diagnostic commands

### Check ECE proxy logs for client IPs and errors

```bash
# List running containers to find the proxy container (look for "frc-proxies-proxyv2")
sudo podman ps

# View recent proxy request logs - replace <proxy_container_id> with actual ID
# Look for the "client_ip" field to verify client IP preservation
sudo podman exec <proxy_container_id> tail -50 /app/logs/proxy.requests.log

# View proxy error logs
sudo podman exec <proxy_container_id> tail -50 /app/logs/proxy.requests.error.log

# Check proxy protocol configuration
sudo podman exec <proxy_container_id> cat /elastic_cloud_apps/proxyv2/proxy.yaml | grep -A5 proxy_protocol

# Verify proxy protocol environment variables
sudo podman exec <proxy_container_id> env | grep -i proxy_proto
```

Expected signals:

- `proxy.requests.log` shows external client addresses in `client_ip`.
- Proxy configuration includes Proxy Protocol v2 settings.
- `proxy.requests.error.log` does not show repeated protocol or upstream connection failures.

### Check container networking

```bash
# List podman networks
sudo podman network ls

# Inspect the dual-stack network
sudo podman network inspect ece-network

# Check which network a container is using
sudo podman inspect <container_id> --format '{{.NetworkSettings.Networks}}'
```

Expected signals:

- The `ece-network` definition includes both IPv4 and IPv6 ranges.
- Containers that need outbound IPv6 are attached to `ece-network`.

### Test connectivity

```bash
# Test IPv6 from host
ping6 -c 3 ipv6.google.com

# Test IPv6 from inside a container
sudo podman exec <container_id> curl -6 -s -o /dev/null -w "%{http_code}" https://ipv6.google.com

# Test NLB connectivity
curl -4 -k -v "https://<nlb-dns-name>/"
curl -6 -k -v "https://<nlb-dns-name>/"
```

Expected signals:

- `curl -4` and `curl -6` to the NLB return an HTTP response (for example `200` or `401`).
- Container `curl -6` reaches external endpoints successfully when egress is enabled.

## Identify ECE vs {{aws}} issues

| Symptom | Likely Cause | Where to Check |
|---------|--------------|----------------|
| Connection hangs before reaching ECE | {{aws}}: Security group, NLB config, or routing | {{aws}} Console: NLB target health, security groups, route tables |
| Connection reaches ECE but returns error | ECE: Proxy configuration or deployment issue | ECE proxy logs (`proxy.requests.error.log`) |
| Client IP shows as internal IP (for example `10.89.0.1`) | {{aws}}: Proxy Protocol not enabled on target group | {{aws}} Console: Target group attributes |
| IPv6 works but IPv4 does not, or IPv4 works but IPv6 does not | {{aws}}: NLB not dual-stack, or missing security group rules | {{aws}} Console: NLB IP address type, security group rules |
| Container cannot reach IPv6 endpoints | ECE: Container not on dual-stack network | Check container network with `podman inspect` |

## Proxy NLB issues

| Issue | Solution |
|-------|----------|
| Health checks failing | Ensure `--proxy-protocol-lenient` was used during ECE install. Health checks must use TCP, not HTTP. |
| Client IPs not preserved | Verify Proxy Protocol v2 is enabled on the target group. Check proxy logs show external IPs for `request_source: external`. |
| IPv6 connections failing | Check NLB has `IpAddressType: dualstack`, security groups allow `::/0`, and route tables have IPv6 routes to IGW. |
| Connection timeouts | Verify target health, security group rules for ports 443 and 9243. Ensure NLB is in the same subnet as the EC2 instance. |
| NLB using wrong security group | Ensure NLB uses a security group allowing inbound 443 (not the default VPC security group). |

## Admin Console ALB issues

| Issue | Solution |
|-------|----------|
| Health checks failing | Verify Admin Console is running (`sudo podman ps \| grep admin`). Health check needs HTTPS, path `/`, success codes `200-399`. |
| 502 Bad Gateway | Security group must allow ALB to reach port 12443 on the instance. |
| Certificate errors | Ensure ACM certificate matches your domain. |
| IPv6 connections failing | Check ALB has `IpAddressType: dualstack` and security groups allow 443 from `::/0`. |
| At least two subnets error | ALBs require subnets in at least two availability zones. Create a second subnet in a different AZ. |

## IPv6 egress issues

| Issue | Solution |
|-------|----------|
| Network unreachable from container | Container not on dual-stack network. Verify `ece-network` exists with IPv6 and is set as default. Containers might need recreation. |
| IPv6 works on host but not in container | Check container network: `sudo podman inspect <container> --format '{{.NetworkSettings.Networks}}'`. Should show `ece-network`. |
| DNS resolution fails | Ensure container can resolve AAAA records. If using the [Netavark](https://docs.podman.io/en/latest/markdown/podman-network.1.html) backend, ensure `aardvark-dns` is installed. |

## Diagnostics collection

When troubleshooting IPv6 issues, the [ECE diagnostic bundle (`ecediag`)](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md) collects proxy logs that include client IP information. Relevant files in the diagnostic bundle:

- `proxy.requests.log` - Contains `client_ip` field showing preserved client IPs
- `proxy.requests.error.log` - Contains failed requests with error reasons
- `proxy.yaml` - Proxy configuration including Proxy Protocol settings

For {{aws}}-side diagnostics (NLB/ALB health, security groups, route tables), use {{aws}} Console or CLI tools. These are not collected by ECE diagnostics.
