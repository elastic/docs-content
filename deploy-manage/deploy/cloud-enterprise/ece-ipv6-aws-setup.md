---
navigation_title: Proxy Protocol v2 for IPv6 ingress on AWS
applies_to:
  deployment:
    ece: ga 4.2
products:
  - id: cloud-enterprise
---

# Setting up IPv6 at the edge for ECE on AWS

This guide explains how to enable IPv6 ingress traffic for {{ece}} (ECE) on AWS using a dual-stack Network Load Balancer (NLB) with Proxy Protocol v2 for [client IP propagation](./ece-load-balancers.md#ece-client-ip-preservation).

## Overview

"IPv6 at the edge" refers to accepting IPv6 traffic at the network boundary (the load balancer) while the internal ECE infrastructure continues to use IPv4. This allows IPv6 clients to connect to your {{es}} and {{kib}} deployments without requiring changes to ECE internal networking.

This configuration provides:

- IPv4 and IPv6 ingress traffic support using a dual-stack NLB
- Client IP propagation (including IPv6 addresses) using Proxy Protocol v2
- No changes required to ECE host networking or container configuration

::::{note}
In this architecture (IPv6 ingress to IPv4 targets), [AWS client IP preservation](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html#client-ip-preservation) at the IP level is not available, so the original client address is propagated using Proxy Protocol v2.
::::

## Architecture

Traffic flows bidirectionally through the NLB. Client requests enter over IPv4/IPv6 on port 443 and are forwarded to ECE proxies on port 9243 with Proxy Protocol v2 metadata. This makes the original client IP available to ECE.

```
                    ┌─────────────────────────────────────────┐
                    │              Internet                   │
                    │         (IPv4 and IPv6 clients)         │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │       AWS Dual-Stack NLB                │
                    │  - Accepts IPv4 and IPv6 traffic        │
                    │  - Listener on port 443                 │
                    │  - Proxy Protocol v2 enabled            │
                    └─────────────────┬───────────────────────┘
                                      │ (forwards to port 9243
                                      │  with Proxy Protocol v2)
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │          ECE Proxy Nodes                │
                    │  - Listening on port 9243               │
                    │  - Configured for Proxy Protocol v2     │
                    │  - Lenient mode for health checks       │
                    │  - Routes to Elasticsearch/Kibana       │
                    └─────────────────────────────────────────┘
```

Response traffic returns through the same established NLB connection path.

## AWS Infrastructure Requirements

Before configuring ECE for IPv6 at the edge, ensure your AWS environment has the following components:

| Component | Requirement |
|-----------|-------------|
| **VPC** | IPv6 CIDR block associated (Amazon-provided or BYOIP) |
| **Subnets** | Dual-stack subnets (IPv4 + IPv6) in at least 2 availability zones (AWS NLB requirement) |
| **Internet Gateway** | Attached to VPC with routes for both `0.0.0.0/0` and `::/0` |
| **Route Tables** | IPv4 and IPv6 routes to the Internet Gateway |
| **Security Groups** | Inbound rules allowing traffic on ports 443 and 9243 for both `0.0.0.0/0` and `::/0` |
| **EC2 Instances** | ECE hosts running in the dual-stack subnets |

For detailed ECE host requirements, refer to [Prepare your environment](docs-content://deploy-manage/deploy/cloud-enterprise/prepare-environment.md) and [Networking prerequisites](docs-content://deploy-manage/deploy/cloud-enterprise/ece-networking-prereq.md).

---

## Step 1: Create the Dual-Stack NLB

Create an NLB with Proxy Protocol v2 enabled to propagate client IP metadata.

### Using AWS CLI

```bash
# Set variables for your environment
VPC_ID="vpc-xxxxxxxxx"
SUBNET1_ID="subnet-xxxxxxxxx"
SUBNET2_ID="subnet-yyyyyyyyy"
INSTANCE_ID="i-xxxxxxxxxxxxxxxxx"
NLB_NAME="ece-ipv6-nlb"

# Create the dual-stack NLB
NLB_ARN=$(aws elbv2 create-load-balancer \
  --name $NLB_NAME \
  --type network \
  --ip-address-type dualstack \
  --scheme internet-facing \
  --subnets $SUBNET1_ID $SUBNET2_ID \
  --query 'LoadBalancers[0].LoadBalancerArn' \
  --output text)

# Create target group for port 9243
TG_ARN=$(aws elbv2 create-target-group \
  --name ${NLB_NAME}-tg-9243 \
  --protocol TCP \
  --port 9243 \
  --vpc-id $VPC_ID \
  --target-type instance \
  --health-check-protocol TCP \
  --query 'TargetGroups[0].TargetGroupArn' \
  --output text)

# Enable Proxy Protocol v2 on the target group
aws elbv2 modify-target-group-attributes \
  --target-group-arn $TG_ARN \
  --attributes Key=proxy_protocol_v2.enabled,Value=true

# Register ECE proxy instance(s) as targets
aws elbv2 register-targets \
  --target-group-arn $TG_ARN \
  --targets Id=$INSTANCE_ID

# Create listener on port 443 forwarding to port 9243
aws elbv2 create-listener \
  --load-balancer-arn $NLB_ARN \
  --protocol TCP \
  --port 443 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN

# Get NLB DNS name
aws elbv2 describe-load-balancers \
  --load-balancer-arns $NLB_ARN \
  --query 'LoadBalancers[0].DNSName' \
  --output text
```

### Using AWS Console

1. Navigate to **EC2** > **Load Balancers** > **Create Load Balancer**
2. Select **Network Load Balancer**
3. Configure:
   - **Name**: `ece-ipv6-nlb`
   - **Scheme**: Internet-facing
   - **IP address type**: Dualstack
   - **Mappings**: Select subnets in at least 2 availability zones
4. Create a target group:
   - **Target type**: Instances
   - **Protocol**: TCP
   - **Port**: 9243
   - **Health check**: TCP
5. After creation, edit target group attributes and enable **Proxy protocol v2**
6. Register your ECE proxy instances as targets
7. Create a listener on port 443 forwarding to the target group

---

## Step 2: Configure ECE for Proxy Protocol

ECE must be configured to parse Proxy Protocol v2 headers from the NLB.

### New ECE Installations

Include the proxy protocol flags when running the installer. For example:

```bash
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install \
  --podman \
  --availability-zone MY_ZONE-1 \
  --proxy-protocol-version 2 \
  --proxy-protocol-lenient \
  --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"},"zookeeper":{"xms":"4G","xmx":"4G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"4G","xmx":"4G"}}'
```

| Flag | Description |
|------|-------------|
| `--proxy-protocol-version 2` | Configures the ECE proxy to parse Proxy Protocol v2 headers. Required for client IP propagation. |
| `--proxy-protocol-lenient` | Allows connections with or without Proxy Protocol headers. **Required** because NLB health checks do not send Proxy Protocol headers. |

Use these flags on **all nodes** with the `proxy` role.

### Existing ECE Installations (Advanced)

For existing ECE installations, you must update the proxy container configuration using the Container Sets API. This is an advanced procedure that modifies container environment variables directly.

**Prerequisites:**

- Admin access to the ECE API
- The current proxy container configuration (to preserve existing environment variables)
- `jq` installed on the host where you run the commands

**Step 1: Get the current proxy container configuration**

```bash
# Get the admin password from an ECE host
ADMIN_PASSWORD=$(sudo cat /mnt/data/elastic/bootstrap-state/bootstrap-secrets.json | jq -r '.adminconsole_root_password')

# Retrieve current proxyv2 container configuration
curl -k -u "admin:$ADMIN_PASSWORD" \
  "https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/container-sets/proxies/containers/proxyv2" | jq '.config.env'
```

**Step 2: Update the proxy container configuration**

Modify the `env` array to include the following Proxy Protocol settings:

| Environment Variable | Value | Description |
|---------------------|-------|-------------|
| `CLOUD_HTTP_PROXY_PROTO_VERSION` | `2` | Configures the proxy to parse Proxy Protocol v2 headers |
| `CLOUD_HTTP_PROXY_PROTO_LENIENT` | `true` | Allows connections with or without Proxy Protocol headers (required for NLB health checks) |

You must include **all existing environment variables** plus the new ones, as this operation replaces the entire `env` array. For example:

```bash
curl -k -u "admin:$ADMIN_PASSWORD" \
  -X PATCH \
  -H "Content-Type: application/json" \
  "https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/container-sets/proxies/containers/proxyv2" \
  -d '{
    "config": {
      "env": [
        "FOUND_PROXY_ZONE=${RUNNER_AVAILABILITY_ZONE}",
        "PROXY_ID=${RUNNER_ID}",
        "PROXY_NAME=${RUNNER_ID}",
        "PROXY_HOST_IP=${RUNNER_HOST_IP}",
        "PROXY_PUBLIC_HOSTNAME=${RUNNER_HOST_IP}",
        "ROLE=proxyv2",
        "ELASTIC_UID=${ELASTIC_UID}",
        "ELASTIC_GID=${ELASTIC_GID}",
        "RUNNER_SERVICE_PATH=${HOST_STORAGE_PATH}/${RUNNER_ID}/services/proxyv2",
        "CLOUD_PROXY_TRUST_XFF=true",
        "CLOUD_HTTP_PROXY_PROTO_VERSION=2",
        "CLOUD_HTTP_PROXY_PROTO_LENIENT=true"
      ]
    }
  }'
```


**Step 3: Recreate the proxy containers one by one**

The configuration change takes effect after the proxy container is recreated. On each proxy host, remove the container to trigger automatic creation:

```bash
# On each ECE host with the proxy role
sudo podman rm -f frc-proxies-proxyv2
```

The runner usually recreates the proxy container within 30-60 seconds. You can verify that the container has been recreated and is running with:

```bash
sudo podman ps -a | grep frc-proxies-proxyv2
```

If no output is returned, wait a few seconds and run the command again.

::::{important}
Do not remove the next proxy container until the previous one has been recreated and is running. Removing all proxy containers at once can cause a permanent service outage if the updated container set is invalid.

If the container is not recreated or does not reach a running state, stop here and [contact Elastic Support](/troubleshoot/index.md#contact-us).
::::

**Step 4: Verify the configuration**

```bash
sudo podman exec $(sudo podman ps --format '{{.Names}}' | grep frc-proxies-proxyv2) env | grep CLOUD_HTTP_PROXY_PROTO
```

Expected output:

```
CLOUD_HTTP_PROXY_PROTO_VERSION=2
CLOUD_HTTP_PROXY_PROTO_LENIENT=true
```

---

## Troubleshooting

Use the following table to identify common issues and fixes.

| Issue | Solution |
|-------|----------|
| **Health checks failing** | Ensure `--proxy-protocol-lenient` was used. Health checks must use TCP protocol, not HTTP. |
| **Client IPs not propagated** | Verify Proxy Protocol v2 is enabled on the target group and `CLOUD_HTTP_PROXY_PROTO_VERSION=2` is set in the proxy container. |
| **IPv6 connections failing** | Check NLB has `IpAddressType: dualstack`, security groups allow `::/0`, and route tables have IPv6 routes to the IGW. |
| **Connection timeouts** | Verify target health, security group rules for ports 443 and 9243, and that the proxy container is running. |

---

## Related Documentation

- [ECE Load balancers](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md)
- [Networking prerequisites](/deploy-manage/deploy/cloud-enterprise/ece-networking-prereq.md)
- [Install ECE](/deploy-manage/deploy/cloud-enterprise/install.md)
