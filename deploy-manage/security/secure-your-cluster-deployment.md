---
applies_to:
  deployment:
    self: ga
    eck: all
    ece: all
    ess: all
---

# Secure your cluster or deployment

It's important to protect your {{es}} cluster and the data it contains. Implementing a defense in depth strategy provides multiple layers of security to help safeguard your system.

:::{include} /deploy-manage/security/_snippets/complete-security.md
:::

:::{important}
* Never run an {{es}} cluster without security enabled. This principle cannot be overstated. Running {{es}} without security leaves your cluster exposed to anyone who can send network traffic to {{es}}, permitting these individuals to download, modify, or delete any data in your cluster.
* Never try to run {{es}} as the `root` user, which would invalidate any defense strategy and permit a malicious user to do **anything** on your server. You must create a dedicated, unprivileged user to run {{es}}. By default, the `rpm`, `deb`, `docker`, and Windows packages of {{es}} contain an `elasticsearch` user with this scope.
::: 

:::{tip}
You must secure [other {{stack}} components](/deploy-manage/security/secure-clients-integrations.md), as well as [client and integration communications](/deploy-manage/security/httprest-clients-security.md), separately.
:::

You can configure the following aspects of your Elastic cluster or deployment to maintain and enhance security:

## Communication and network security

:::{include} /deploy-manage/security/_snippets/cluster-communication-network.md
:::

## Data security

:::{include} /deploy-manage/security/_snippets/cluster-data.md
:::
 
## User session security

:::{include} /deploy-manage/security/_snippets/cluster-user-session.md
:::

## Security event audit logging

:::{include} /deploy-manage/security/_snippets/audit-logging.md
:::

## Configure security in a self-managed cluster

Since {{es}} 8.0, security is enabled and configured by default. However, security auto configuration [might be skipped](/deploy-manage/security/manually-configure-security-in-self-managed-cluster.md#stack-skip-auto-configuration) in certain scenarios. In these cases, you can [manually configure security](/deploy-manage/security/manually-configure-security-in-self-managed-cluster.md).

## FIPS 140-2 compliant mode
```{applies_to}
deployment:
  self:
  eck:
```

The Federal Information Processing Standard (FIPS) Publication 140-2, (FIPS PUB 140-2), titled "Security Requirements for Cryptographic Modules" is a U.S. government computer security standard used to approve cryptographic modules. You can run a self-managed cluster or {{eck}} cluster in FIPS-compliant mode:

* [Self-managed](/deploy-manage/security/fips-140-2.md)
* [ECK](/deploy-manage/deploy/cloud-on-k8s/deploy-fips-compatible-version-of-eck.md)

% we need to refine this table, but the idea is awesome IMO

## Security features by deployment type [comparison-table]

:::{include} /deploy-manage/security/_snippets/cluster-comparison.md
:::