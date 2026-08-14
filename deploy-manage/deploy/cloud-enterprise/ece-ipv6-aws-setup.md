---
navigation_title: Set up IPv6 on {{aws}}
applies_to:
  deployment:
    ece: ga 4.2
products:
  - id: cloud-enterprise
---

# Set up IPv6 for ECE on {{aws}}

This guide provides an end-to-end example for setting up {{ece}} (ECE) on {{aws}} with IPv6 support, including networking, load balancers, and ECE-specific configuration settings.

The examples demonstrate one way to achieve IPv6 connectivity. Your {{aws}} configuration might vary depending on your environment and requirements, and other cloud providers might require different load balancer configurations and are not covered here. For an overview of IPv6 capabilities and requirements on ECE, refer to [IPv6 support on ECE](./ece-ipv6-support.md).

:::::{note}
This tutorial focuses on new environment setups. If you are working with an existing ECE installation, refer to [Appendix: Integrate IPv6 in existing ECE installations](#existing-installations-summary) to understand the required actions and additional infrastructure changes.
:::::

## Overview

This guide covers two distinct IPv6 traffic flows, ingress and egress, which can be configured independently and have different infrastructure implications:

- **IPv6 ingress (client connectivity)**: Enables IPv4 and IPv6 clients to access ECE endpoints through {{aws}} load balancers. When combined with [IP filtering rules](/deploy-manage/security/ip-filtering-ece.md), this also lets you apply network security policies to IPv6 client addresses. This includes:
  - **Deployment traffic**: Client access to {{es}} and {{kib}} through a dual-stack Network Load Balancer (NLB) and [Proxy Protocol v2](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html#proxy-protocol) used for [client IP propagation](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html#client-ip-preservation).
  - **Control plane traffic**: Optional access to the ECE Admin Console through a dual-stack Application Load Balancer (ALB).

  ::::{note}
  For IPv6 ingress, the {{aws}} load balancers accept IPv6 traffic and forward it to ECE hosts over IPv4. ECE hosts can remain IPv4-only, which makes this approach suitable for existing installations.
  ::::

- **IPv6 egress (outbound connectivity)**: Enables ECE containers to make outbound connections over IPv6. Outbound IPv6 traffic originates directly from ECE hosts, so dual-stack host networking is required.

## Architecture

The following diagram illustrates an IPv6 architecture with ingress and egress support, using dual-stack ECE hosts.

```
                    ┌─────────────────────────────────────────┐
                    │              Internet                   │
                    │         (IPv4 and IPv6 clients)         │
                    └─────────────────┬───────────────────────┘
                                      |
                Deployment traffic    │   Control plane traffic
                    ┌─────────────────┴───────────────────────┐
                    │                                         │
                    ▼                                         ▼
     ┌──────────────────────────┐          ┌──────────────────────────┐
     │   Dual-Stack NLB         │          │   Dual-Stack ALB         │
     │   (Proxy - port 443)     │          │   (Admin - port 443)     │
     │   Proxy Protocol v2      │          │   TLS termination        │
     └────────────┬─────────────┘          └────────────┬─────────────┘
                  │ :9243                               │ :12443
                  ▼                                     ▼
     ┌──────────────────────────────────────────────────────────────┐
     │                      ECE Host (RHEL)                         │
     │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
     │  │ ECE Proxy   │  │ Admin       │  │ Elasticsearch/Kibana│   │
     │  │ :9243       │  │ Console     │  │ (deployments)       │   │
     │  │             │  │ :12443      │  │                     │   │
     │  └─────────────┘  └─────────────┘  └─────────────────────┘   │
     │                                                              │
     │  ┌────────────────────────────────────────────────────────┐  │
     │  │ Dual-stack Podman network (ece-network)                │  │
     │  │ IPv4: 10.89.0.0/24  │  IPv6: fd00:10:89::/64           │  │
     │  └────────────────────────────────────────────────────────┘  │
     └──────────────────────────────────────────────────────────────┘
```

In this architecture, deployment traffic enters through the NLB over IPv4/IPv6 on port 443 and is forwarded to ECE proxies on port 9243 with Proxy Protocol v2 metadata, used to propagate the original client IP. Response traffic returns through the same load balancer path.

Outbound traffic (IPv6 egress) originates directly from ECE hosts and is routed through the configured network gateways.

::::{note}
The ALB for port 12443 is optional and only required to enable IPv6 access to the ECE Admin Console.

Dual-stack ECE hosts are required for IPv6 egress. IPv6 ingress alone does not require IPv6 configuration on the hosts.
::::

## Prerequisites [prereqs-global]

To create a new environment using this tutorial, you need:

- An {{aws}} account with permissions to create VPCs, subnets, EC2 instances, NLBs, ALBs, and ACM certificates.
- A RHEL 8 or RHEL 9 AMI (official Red Hat AMI, not marketplace variants).
- An instance type that meets the [ECE requirements](/deploy-manage/deploy/cloud-enterprise/ece-hardware-prereq.md), with at least 32 GB of RAM for single-node testing.

::::{note}
If you are enabling IPv6 in an existing ECE environment, refer to [Appendix: Integrate IPv6 in existing ECE installations](#existing-installations-summary) for the corresponding requirements.
::::

For detailed ECE host and infrastructure requirements, refer to [Prepare your environment](/deploy-manage/deploy/cloud-enterprise/prepare-environment.md) and [Networking prerequisites](/deploy-manage/deploy/cloud-enterprise/ece-networking-prereq.md).

The examples of this guide use Podman. For Docker-based hosts, replace `podman` with `docker` in all commands. The {{aws}} console steps shown are examples. For details on {{aws}}-specific configuration options, refer to the [{{aws}} documentation](https://docs.aws.amazon.com/).

## Configuration steps

:::::{stepper}

::::{step} Set up {{aws}} infrastructure
:anchor: step-vpc

Follow these steps in the {{aws}} console to create a new VPC or configure an existing one to enable IPv6 support:

1. **VPC** → **Your VPCs** → Select your VPC (or create new) → **Actions** → **Edit CIDRs**
   - Click **Add new IPv6 CIDR**
   - Select **Amazon-provided IPv6 CIDR block**
   - Click **Select CIDR**

2. **Subnets** → Select each subnet → **Actions** → **Edit IPv6 CIDRs**
   - Click **Add IPv6 CIDR**
   - Enter a unique subnet suffix (for example, `00`, `01`, `02`)
   - This creates a `/64` IPv6 subnet from your VPC's `/56` block

3. **Subnets** → Select each subnet → **Actions** → **Edit subnet settings**
   - Enable **Auto-assign IPv6 address**

4. **Route Tables** → Select the route table for your subnets → **Edit routes**
   - Add route: Destination `::/0` → Target: Your Internet Gateway

5. **Security Groups** → Select or create a security group → **Edit inbound rules**
   - Add the following rules for both IPv4 (`0.0.0.0/0`) and IPv6 (`::/0`). These rules cover basic external access for a single-node test environment. For production multi-node deployments, refer to [Networking prerequisites](./ece-networking-prereq.md) for the full list of required ports, including inter-node traffic.

   | Port | Protocol | Purpose |
   |------|----------|---------|
   | 22 | TCP | SSH access |
   | 443 | TCP | NLB/ALB ingress |
   | 9243 | TCP | ECE proxy (direct access) |
   | 12443 | TCP | Admin Console (direct access) |

::::

::::{step} Set up EC2 instances
:anchor: step-vm-launch

Create one or more RHEL instances to host ECE:

:::{note}
This tutorial uses a single-host deployment for simplicity and testing purposes. For production environments, you should deploy multiple hosts across availability zones to ensure high availability and resilience. Refer to [Identify the deployment scenario](/deploy-manage/deploy/cloud-enterprise/identify-deployment-scenario.md) for guidance on recommended architectures.
:::

1. **EC2** → **Launch Instance**

2. **Name and AMI**:
   - Name: `ece-ipv6-host`
   - AMI: Search for "RHEL" and select an official **Red Hat Enterprise Linux 8** or **9** AMI from Red Hat, Inc.
   - Avoid marketplace variants, SQL Server editions, or third-party repackaged images

3. **Instance type**:
   - Select an instance with at least 32GB RAM (for example, `r5.xlarge`, `m5.2xlarge`)
   - `t3` instances are insufficient for ECE

4. **Key pair**: Select or create a key pair for SSH access

5. **Network settings**:
   - **VPC**: Select your dual-stack VPC
   - **Subnet**: Select a subnet with IPv6 enabled
   - **Auto-assign public IP**: Enable
   - **Security group**: Select your security group with IPv6 rules

6. **Advanced network configuration** (click **Edit**):
   - **IPv4 address**: Assigned by {{aws}}
   - **IPv6 address**: Select "Assigned from CIDR" (your subnet's IPv6 range)
   - **IPv6 prefix**: Leave unchecked

7. **Storage**: Add at least 200GB for `/mnt/data` (ECE data directory)

8. In the UI, select **Launch instance**

### Verify IPv6 outbound connectivity

If you plan to enable IPv6 egress, validate host-level IPv6 outbound connectivity. After the instance launches, SSH into the host and verify:

```bash
# Check IPv6 address is assigned
ip -6 addr show scope global

# Test IPv6 connectivity
ping6 -c 3 ipv6.google.com
```

::::

::::{step} Prepare the Host and Install ECE
:anchor: step-install-ece

This step covers a single-node ECE installation. For multi-node deployments, follow the same host preparation steps on each node and refer to the [ECE installation procedures](/deploy-manage/deploy/cloud-enterprise/install-ece-procedures.md) for the full installation sequence.

### Prepare the ECE host

Prepare the host according to the official ECE documentation: [Prepare your environment](/deploy-manage/deploy/cloud-enterprise/prepare-environment.md).

For RHEL hosts, follow [Configure a RHEL host](/deploy-manage/deploy/cloud-enterprise/configure-host-rhel.md). If you need IPv6 egress, that guide includes an optional step to create a dedicated dual-stack Podman network with IPv6 support. Complete it **before** you install ECE.

:::{note}
IPv6 ingress through {{aws}} load balancers does not require dual-stack container networking on the ECE hosts. Dual-stack Podman or Docker configuration is required only for IPv6 egress.
:::

### Install ECE

1. Install ECE with Proxy Protocol v2 support enabled. This is required for the NLB to propagate the client IP addresses.

    ```bash
    sudo su - elastic

    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install \
      --podman \ <1>
      --availability-zone MY_ZONE-1 \
      --proxy-protocol-version 2 \
      --proxy-protocol-lenient \
      --memory-settings '{"runner":{"xms":"1G","xmx":"1G"},"allocator":{"xms":"4G","xmx":"4G"},"zookeeper":{"xms":"4G","xmx":"4G"},"director":{"xms":"1G","xmx":"1G"},"constructor":{"xms":"4G","xmx":"4G"},"admin-console":{"xms":"4G","xmx":"4G"}}'
    ```
    1. For Docker installations, omit the `--podman` flag.

    | Flag | Description |
    |------|-------------|
    | `--proxy-protocol-version 2` | Configures the ECE proxy to parse Proxy Protocol v2 headers. Required for client IP propagation. |
    | `--proxy-protocol-lenient` | Allows connections with or without Proxy Protocol headers. Required because NLB health checks do not send Proxy Protocol headers. |

    For a full list of installation parameters, refer to [elastic-cloud-enterprise.sh install](cloud://reference/cloud-enterprise/ece-installation-script.md).

    :::{note}
    The `--memory-settings` shown in the example are for **example/testing purposes only**. For production deployments, refer to [ECE installation procedures](/deploy-manage/deploy/cloud-enterprise/install-ece-procedures.md) for recommended memory settings based on your deployment size (small/medium/large).
    :::

1. After installation completes on the first node, note the Admin Console URL and credentials displayed.

::::

::::{step} Create the proxy NLB for deployment traffic
:anchor: step-nlb

The Network Load Balancer (NLB) provides IPv6 and IPv4 ingress for {{es}} and {{kib}} deployments, forwarding traffic to the ECE proxies over their IPv4 interfaces.

:::{note}
In this architecture (IPv6 ingress to IPv4 targets), [{{aws}} client IP preservation](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html#client-ip-preservation) at the IP level is not available, so the original client address is propagated using [Proxy Protocol v2](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/edit-target-group-attributes.html#proxy-protocol).
:::

This configuration follows the requirements described in the [ECE load balancers](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) documentation.

### Create the ECE proxies target group

1. Navigate to **EC2** → **Target Groups** → **Create target group**

2. **Basic configuration**:
    - **Target type**: Instances
    - **Target group name**: `ece-proxy-tg-9243`
    - **Protocol**: TCP
    - **Port**: 9243
    - **IP address type**: IPv4
    - **VPC**: Select your dual-stack VPC

3. **Health checks**:
    - **Health check protocol**: HTTPS
    - **Health check path**: `/_health`
    - **Health check port**: Traffic port
    - **Healthy threshold**: 3
    - **Unhealthy threshold**: 3
    - **Interval**: 30 seconds
    - **Timeout**: 10 seconds
    - **Success codes**: `200`

4. Click **Next**

5. **Register targets**:
    - Select your ECE instance (select all your [ECE proxies](/deploy-manage/deploy/cloud-enterprise/ece-roles.md) in a multi-node environment)
    - **Port**: `9243`
    - Click **Include as pending below**
    - Click **Create target group**

6. **Enable Proxy Protocol v2**:
    - Select the target group → **Attributes** tab → **Edit**
    - Enable **Proxy protocol v2**
    - Click **Save changes**

### Create the dual-stack NLB

1. Navigate to **EC2** → **Load Balancers** → **Create Load Balancer**

2. Select **Network Load Balancer**

3. **Basic configuration**:
    - **Name**: `ece-proxy-nlb`
    - **Scheme**: Internet-facing
    - **IP address type**: **Dualstack** (important - not IPv4)

4. **Network mapping**:
    - **VPC**: Select your dual-stack VPC
    - **Availability Zones**: Select the same subnet where your ECE instance is running (the NLB must be in the same subnet as the target instance)

5. **Security groups**: Select a security group that allows inbound TCP 443 from `0.0.0.0/0` and `::/0` (do not use the default security group)

6. **Listeners and routing**:
    - Delete the default TCP:80 listener
    - Add listener:
      - **Protocol**: TCP
      - **Port**: 443
      - **Forward to**: `ece-proxy-tg-9243`

7. Click **Create load balancer**

8. Note the NLB **DNS name**

### Verify Proxy NLB

After the NLB is active, confirm it accepts both IPv4 and IPv6 connections:

```bash
NLB_DNS="your-nlb-dns-name.elb.region.amazonaws.com"

curl -4 -k -s -o /dev/null -w "IPv4: %{http_code}\n" "https://${NLB_DNS}/_health"
curl -6 -k -s -o /dev/null -w "IPv6: %{http_code}\n" "https://${NLB_DNS}/_health"
```

Both commands should return `200`. If IPv6 returns an error, verify that the NLB is configured as dual-stack, that the subnet has an IPv6 CIDR assigned, and that the route table includes a `::/0` route to the Internet Gateway.

::::

::::{step} (Optional) Create the control plane ALB
:anchor: step-alb

If you need IPv6 access to the ECE Admin Console, create an Application Load Balancer (ALB).

This configuration follows the requirements described in the [ECE load balancers](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) documentation for admin console traffic.

### ALB prerequisites

Application Load Balancers require an ACM certificate and subnets in at least two availability zones.

**ACM Certificate:**
1. Navigate to **Certificate Manager** → **Request certificate**
2. Request a public certificate for your domain
3. Complete domain validation
4. Note the certificate ARN

**Two subnets in different AZs:**

ALBs require subnets in at least two availability zones. If you only have one subnet, create a second:

1. Go to **VPC → Subnets → Create subnet**
2. Configuration:
   - **VPC**: Select your VPC
   - **Subnet name**: for example, `ece-subnet-2`
   - **Availability Zone**: Select a **different** AZ from your first subnet
   - **IPv4 CIDR**: An unused range (for example, `10.0.32.0/24`)
3. Click **Create subnet**
4. **Add IPv6 to the new subnet:**
   - Select the new subnet → **Actions → Edit IPv6 CIDRs**
   - Add an IPv6 CIDR with a unique suffix (for example, `2a05:d018:xxx:xx20::/64`)
5. **Associate with route table:**
   - Go to **VPC → Route Tables** → select your route table
   - **Subnet associations → Edit** → Add the new subnet
   - Ensure the route table has routes for `0.0.0.0/0` and `::/0` to the Internet Gateway

### Create the ECE coordinators target group

1. Navigate to **EC2** → **Target Groups** → **Create target group**

2. **Basic configuration**:
   - **Target type**: Instances
   - **Target group name**: `ece-admin-tg-12443`
   - **Protocol**: HTTPS
   - **Port**: 12443
   - **IP address type**: IPv4
   - **VPC**: Select your dual-stack VPC

3. **Health checks**:
   - **Health check protocol**: HTTPS
   - **Health check path**: `/`
   - **Health check port**: Traffic port
   - **Healthy threshold**: 2
   - **Unhealthy threshold**: 2
   - **Timeout**: 5 seconds
   - **Interval**: 30 seconds
   - **Success codes**: `200-399`

4. Click **Next**

5. **Register targets**:
   - Select your ECE instance (select all your [ECE coordinators](/deploy-manage/deploy/cloud-enterprise/ece-roles.md) in a multi-node environment)
   - **Port**: `12443`
   - Click **Include as pending below**
   - Click **Create target group**

### Create the dual-stack ALB

1. Navigate to **EC2** → **Load Balancers** → **Create Load Balancer**

2. Select **Application Load Balancer**

3. **Basic configuration**:
   - **Name**: `ece-admin-alb`
   - **Scheme**: Internet-facing
   - **IP address type**: Dualstack

4. **Network mapping**:
   - **VPC**: Select your dual-stack VPC
   - **Availability Zones**: Select at least **two** subnets in different AZs (required for ALB)

5. **Security groups**: Select your security group

6. **Listeners and routing**:
   - Delete the default HTTP:80 listener
   - Add listener:
     - **Protocol**: HTTPS
     - **Port**: 443
     - **Forward to**: `ece-admin-tg-12443`
   - **Secure listener settings**:
     - **Security policy**: ELBSecurityPolicy-TLS13-1-2-2021-06
     - **Certificate**: Select your ACM certificate

7. Click **Create load balancer**

8. Note the ALB **DNS name**

### Verify Admin Console ALB

After the ALB is active, confirm it accepts both IPv4 and IPv6 connections:

```bash
ALB_DNS="your-alb-dns-name.elb.region.amazonaws.com"

curl -4 -k -s -o /dev/null -w "IPv4: %{http_code}\n" "https://${ALB_DNS}/"
curl -6 -k -s -o /dev/null -w "IPv6: %{http_code}\n" "https://${ALB_DNS}/"
```

Both commands should return `200` or `302` (redirect to login). If IPv6 returns an error, verify that the ALB is configured as dual-stack, that the subnet has an IPv6 CIDR assigned, and that the route table includes a `::/0` route to the Internet Gateway.

::::

::::{step} Verify your installation
:anchor: step-verify-installation

After completing your configuration, confirm end-to-end behavior with the following checks.

1. In the {{aws}} console, check **EC2** → **Target Groups** → **Targets** and confirm all registered targets are healthy.

2. Make a request to one of your deployments through the NLB and verify that the `client_ip` field in the proxy logs shows the real client address, not the load balancer address:

    ```bash
    sudo podman exec frc-proxies-proxyv2 tail -10 /app/logs/proxy.requests.log | grep client_ip
    ```

    The `client_ip` field should show the real client address (IPv4 or IPv6), not an internal address such as `10.89.0.1`.

3. If you enabled IPv6 egress, verify that containers can reach IPv6 endpoints:

    ```bash subs=true
    # List running containers to find an {{es}} container
    sudo podman ps

    # Test IPv6 connectivity from the {{es}} container (replace <container_id> with actual ID)
    sudo podman exec <container_id> curl -6 -s -o /dev/null -w "%{http_code}" https://ipv6.google.com
    ```

    A response of `200` confirms IPv6 egress is working. You can also test from {{kib}} containers using the same approach.

    :::{dropdown} Optional: test IPv6 egress using {{es}} {{watcher}}
    Run this from any existing deployment to perform a connectivity test using [{{watcher}}](/explore-analyze/alerting/watcher.md):

    ```json
    POST _watcher/watch/_execute
    {
      "watch": {
        "trigger": { "schedule": { "interval": "1h" } },
        "input": {
          "http": {
            "request": {
              "scheme": "https",
              "host": "ipv6.google.com",
              "port": 443,
              "method": "head",
              "path": "/"
            }
          }
        },
        "actions": {
          "log": {
            "logging": { "text": "IPv6 test - Status: {{ctx.payload.status}}" }
          }
        }
      }
    }
    ```
    :::

::::

:::::

## Troubleshooting

For troubleshooting and verification commands specific to IPv6 integration on {{aws}}, refer to [Troubleshoot IPv6 integration for ECE on {{aws}}](/troubleshoot/deployments/cloud-enterprise/troubleshoot-ipv6-aws-integration.md).

## Related Documentation

- [IPv6 support on ECE](./ece-ipv6-support.md)
- [Configure Proxy Protocol v2 in the ECE proxies](./configure-proxy-protocol.md)
- [ECE Hardware requirements](/deploy-manage/deploy/cloud-enterprise/ece-hardware-prereq.md)
- [Prepare your environment](/deploy-manage/deploy/cloud-enterprise/prepare-environment.md)
- [Configure a RHEL host](/deploy-manage/deploy/cloud-enterprise/configure-host-rhel.md)
- [ECE installation procedures](/deploy-manage/deploy/cloud-enterprise/install-ece-procedures.md)
- [ECE Load balancers](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md)
- [Networking prerequisites](/deploy-manage/deploy/cloud-enterprise/ece-networking-prereq.md)
- [{{aws}} Elastic Load Balancing documentation](https://docs.aws.amazon.com/elasticloadbalancing/)

## Appendix: Integrate IPv6 in existing ECE installations [existing-installations-summary]

This appendix focuses on existing ECE environments that are currently IPv4-only and explains how to introduce IPv6 for both inbound (ingress) and outbound (egress) traffic.

- **IPv6 ingress**: Enable IPv6 client access to deployments and optionally to the admin console.
- **IPv6 egress**: Enable outbound IPv6 connectivity from ECE containers.

The infrastructure examples are specific to {{aws}}. Other cloud providers might require different load balancer configurations and are not covered here.

### Requirements for existing environments [existing-installations-requirements]

The following requirements apply when integrating IPv6 into an existing ECE installation. Some are specific to ingress or egress traffic.

#### ECE requirements

| Requirement | IPv6 ingress | IPv6 egress | Notes |
|-------------|--------------|--------------|-------|
| Proxy Protocol v2 support in ECE proxies | ✔ | | Required for IPv6 ingress through {{aws}} Network Load Balancers (NLB) for deployment traffic |
| IPv6 interfaces on ECE hosts | | ✔ | Required for outbound IPv6 connectivity |
| Container runtime with IPv6 support (Podman or Docker) | | ✔ | Required for outbound IPv6 connectivity |

#### {{aws}} requirements

| Component | Requirement |
|-----------|-------------|
| **VPC** | An associated IPv6 CIDR block (Amazon-provided or BYOIP) |
| **Subnets** | Dual-stack subnets (IPv4 + IPv6) in at least two Availability Zones (required for Application Load Balancers) |
| **Internet Gateway** | Attached to the VPC with routes for both `0.0.0.0/0` and `::/0` |
| **Route Tables** | IPv4 and IPv6 routes to the Internet Gateway |
| **Security Groups** | Inbound rules allowing traffic on ports `443`, `9243`, and `12443` for both `0.0.0.0/0` and `::/0` |
| **EC2 instances** | ECE hosts running in dual-stack subnets (required only for IPv6 egress) |

:::{note}
If you need to adjust VPC, subnets, route tables, or security group settings before enabling IPv6 ingress or egress in an existing environment, you can use [Set up {{aws}} infrastructure](#step-vpc) as reference.
:::

### IPv6 ingress in existing IPv4 environments

To enable IPv6 ingress in an existing IPv4 ECE environment, complete the following actions:

1. Configure ECE proxies to parse Proxy Protocol v2 headers by reinstalling your proxy hosts one at a time with the `--proxy-protocol-version 2` and `--proxy-protocol-lenient` flags. This is required for client IP propagation through the NLB. Refer to [Configure Proxy Protocol v2](./configure-proxy-protocol.md#ece-proxy-protocol-enable) for details.
1. Configure a dual-stack NLB for deployment traffic ({{es}}/{{kib}}). Refer to [Create the proxy NLB for deployment traffic](#step-nlb).
1. Optionally, configure a dual-stack ALB for admin console UI traffic. Refer to [Create the control plane ALB - Optional](#step-alb).

### IPv6 egress in existing IPv4 environments

To support IPv6 egress in an existing IPv4 ECE environment, you must update both host networking and container networking on every ECE host:

1. Assign IPv6 addresses to existing EC2 instances in {{aws}}

    Existing EC2 instances do not automatically receive IPv6 addresses when you [enable IPv6 on their subnet](#step-vpc). You must assign them manually.

    For each ECE host:

    1. Go to **EC2** → **Instances** and select your instance.
    2. Go to **Actions** → **Networking** → **Manage IP addresses**.
    3. Expand the network interface section.
    4. Under **IPv6 addresses**, select **Assign new IP address**.
    5. Select **Assign** to auto-assign an IPv6 address from your subnet range.
    6. Select **Save**.

    To enable auto-assignment for new instances:

    1. Go to **VPC** → **Subnets** and select the subnet.
    2. Go to **Actions** → **Edit subnet settings**.
    3. Enable **Auto-assign IPv6 address**.

2. Reconfigure host network interfaces for dual-stack connectivity

    After assigning IPv6 addresses in {{aws}}, RHEL 8/9 might not automatically configure IPv6 on the active interface. Configure NetworkManager explicitly:

    ```bash
    # List connections and identify the active one
    nmcli con show

    # Example for a connection named "System eth0"
    sudo nmcli con mod "System eth0" ipv6.method auto

    # Restart the connection
    sudo nmcli con down "System eth0" && sudo nmcli con up "System eth0"

    # Verify host IPv6 connectivity
    ip -6 addr show scope global
    ping6 -c 3 ipv6.google.com
    ```

    If `ping6` returns `Network unreachable`, verify:

    - Route tables include `::/0` to the Internet Gateway.
    - NetworkManager uses `ipv6.method auto` on the active connection.

3. Configure Podman dual-stack network for IPv6

    On existing ECE hosts that were prepared without IPv6, create a dual-stack network in Podman, and configure it as the default network for future containers:

    ```bash
    # Create a dual-stack network
    sudo podman network create \
      --subnet 10.89.0.0/24 \
      --subnet fd00:10:89::/64 \
      --ipv6 \
      ece-network

    # Set as default for future containers
    sudo tee -a /etc/containers/containers.conf > /dev/null <<'EOF'
    [network]
    default_network = "ece-network"
    EOF
    ```

    This is the same dual-stack network configuration described in [Configure a RHEL host](/deploy-manage/deploy/cloud-enterprise/configure-host-rhel.md) for new ECE hosts.

    :::{note}
    For Docker-based hosts, the approach is different: instead of creating a new network, you enable IPv6 on the default bridge by modifying `/etc/docker/daemon.json`. Refer to [Configure an Ubuntu host](/deploy-manage/deploy/cloud-enterprise/configure-host-ubuntu.md#ece-ubuntu-ipv6-egress) or [Configure a SUSE host](/deploy-manage/deploy/cloud-enterprise/configure-host-suse.md#ece-suse-ipv6-egress) for the Docker-specific procedure.
    :::

4. Attach running containers to the new network

    Connect running containers to `ece-network` using Podman:

    ```bash
    for container in $(sudo podman ps -q); do
      sudo podman network connect ece-network "$container" 2>/dev/null || true
    done
    ```

    :::{note}
    This command attaches each running container to `ece-network` as an additional network interface, leaving the original network interface in place. Existing containers will have two network interfaces, while containers on new or reinstalled hosts will only have `ece-network`. If you want a consistent single-network configuration, reinstall ECE on each host one by one following the [Remove and reinstall](/deploy-manage/maintenance/ece/perform-ece-hosts-maintenance.md#ece-perform-host-maintenance-delete-runner) procedure instead.
    :::

5. Verify egress from one container

    Pick any running ECE container and confirm it can reach an IPv6 endpoint:

    ```bash
    sudo podman exec <container_id> curl -6 -s -o /dev/null -w "%{http_code}\n" https://ipv6.google.com
    ```

    A response of `200` confirms IPv6 egress is working from that container.

After completing these changes, refer to [Verify your installation](#step-verify-installation) to validate outbound IPv6 connectivity from ECE workloads.