---
navigation_title: Privileges and API keys
description: Learn which roles can view and edit the Streams Map and create sources and destinations, and how source API keys and destination credentials are stored.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Privileges and API keys in Streams

Streams separates three kinds of access. A {{kib}} privilege decides who can view and change the Streams Map. A source API key decides which shippers can write to a source. A destination's credentials decide what it's allowed to write. This page explains each one and what you need to do about it. Nothing here changes how your existing shippers authenticate to {{es}} or to the project's existing managed endpoints.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Who can view and edit streams [streams-security-view-edit]

Access to the Streams Map, the **Sources** tab, and the **Destinations** tab is controlled by a dedicated {{kib}} feature privilege, shown as **Streams V2** under **Management** when you edit a custom role. It's separate from the **Streams** privilege that governs classic streams, so a role that has **Streams: All** today doesn't get access to the Map automatically. The privilege is listed only on projects where the preview is enabled.

| Privilege | What it allows |
| --- | --- |
| **Read** | Open the Map and the **Sources** and **Destinations** tabs and see every source, pipeline, router, and destination. The Map and the tabs show a **You have read-only access** callout, and the toolbar, the plus icon on connections, **Add source**, **Add destination**, **Generate key**, and **Delete** aren't offered. |
| **All** | Everything in **Read**, plus saving changes to the Map, creating and deleting sources and destinations, and generating, listing, and deleting source API keys. |

The privilege is granted per {{kib}} space, but a project has one Streams configuration shared by all spaces. A role that grants **All** in any space can change the project's streams.

Creating a source or a Local Elasticsearch destination also needs {{es}} privileges of your own, because Streams creates their API keys as the signed-in user. The **Admin** predefined role has the **All** privilege and those {{es}} privileges, so use it to build and change streams. The **Viewer** predefined role has the **Read** privilege. What you see about a destination's indices depends on your own {{es}} privileges on them. Indices you can't view are left out of the list, and the destination panel names the privilege that's missing.

Treat **All** as an administrative privilege. Anyone who can connect a source to a destination can direct that source's data anywhere the destination is allowed to write.

## Source API keys [streams-security-source-keys]

Each source has its own API keys. A source key is an {{es}} API key that grants permission to write to that source. It can't write to any other source, and it has no index privileges, so a shipper that holds it can't read or write {{es}} directly.

* Streams generates a key when you create the source and shows it once, so copy it then. If you lose it, open the source from the Streams Map or the **Sources** tab and select **Generate key**. A source can have several keys at once, so generating a new one doesn't stop the shippers that use an older one. Delete keys you no longer use from the same panel.
* Shippers send the key in every request as the HTTP header `Authorization: ApiKey <key>`. The source is identified by its URL path, and the key must belong to that source.
* A key is created as the user who generated it and can't do more than that user could. It keeps working if the user's role changes or the user leaves, so delete keys as part of offboarding. Any user with the **All** privilege can delete any source key.
* All shippers writing to the same source share everything downstream of it. There's no per-shipper isolation inside a source. If two sets of data must be kept apart, give them separate sources and separate destinations.

For the request shapes and shipper configuration, refer to [Sources](sources.md). If a shipper gets `401` or `403` from a source endpoint, refer to [Troubleshooting](troubleshooting.md#streams-troubleshoot-401).

## Destination credentials [streams-security-destinations]

A destination holds the credentials used to write to it. How they're created depends on the [destination type](destinations.md#streams-destinations-types). A destination can't be edited after you create it, so to change its credentials or its write patterns you create a new destination, reconnect the routing rules, and delete the old one.

### Local Elasticsearch [streams-security-local]

When you create a **Local Elasticsearch** destination, Streams creates an {{es}} API key for it as you. The key grants only `create_doc` and `auto_configure` on the destination's write patterns, which default to `logs-*-*`, `metrics-*-*`, and `traces-*-*`, one per signal. {{es}} limits the key to the intersection of those privileges and yours at creation time, so you can't create a destination that writes where you can't.

* Write patterns bound what the key can write to. They don't route data. A record whose target falls outside the patterns is rejected by {{es}} and dropped, not redirected.
* Deleting the destination invalidates its key.
* You never see or manage this key. Streams stores it encrypted, and the configuration refers to it by name only.

For how write patterns interact with Auto and Fixed index modes, refer to [Local Elasticsearch destination](destinations/elasticsearch.md).

### Remote Elasticsearch and Amazon S3 [streams-security-remote-s3]

For a [Remote Elasticsearch](destinations/remote-elasticsearch.md) destination, you supply an API key for the remote deployment. For an [Amazon S3](destinations/s3.md) destination, you supply an AWS access key ID and secret access key with write access to the bucket. In both cases, Streams encrypts what you enter when you save it. The credential is never shown again, and the running configuration refers to it by name only.

Streams can't narrow a credential you supply. Create it with the least privilege the destination needs, which is write access to the target indices on the remote deployment, or `s3:PutObject` on the bucket and prefix.

## What a failed authorization looks like [streams-security-failures]

A source acknowledges data as soon as it's accepted, before processing and delivery finish. If a destination's credential is later rejected, or a record targets an index outside the destination's write patterns, the records are dropped after the retry window. The shipper that sent them isn't told, and the drop isn't reported in the UI. Refer to [Streams limitations](limitations.md#streams-limitations-data).

## Related pages [streams-security-related]

* [Sources](sources.md): Create sources and configure your shippers with their endpoints and API keys.
* [Local Elasticsearch destination](destinations/elasticsearch.md): Choose an index mode and write patterns for a Local Elasticsearch destination.
* [Remote Elasticsearch destination](destinations/remote-elasticsearch.md): Send data to another Elastic Cloud deployment with credentials you supply.
* [Amazon S3 destination](destinations/s3.md): Write data to an Amazon S3 bucket with an access key pair you supply.
* [Troubleshooting](troubleshooting.md#streams-troubleshoot-401): Find out what to do when a source endpoint returns `401` or `403`.
* [Streams limitations](limitations.md#streams-limitations-operations): Read the current limits on access control and operations.
