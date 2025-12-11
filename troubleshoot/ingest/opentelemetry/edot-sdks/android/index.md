---
navigation_title: EDOT Android
description: Use the information in this section to troubleshoot common problems affecting the Elastic Distribution of OpenTelemetry Android.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_android: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
mapped_pages:
  - https://www.elastic.co/guide/en/apm/SDK/android/current/faq.html
---

# Troubleshooting the EDOT Android SDK

Use the information in this section to troubleshoot common problems. As a first step, make sure your stack is compatible with the [supported technologies](apm-agent-android://reference/edot-android/getting-started.md#requirements) for EDOT Android and the OpenTelemetry SDK.

:::{tip}
If you're sending EDOT SDK telemetry directly to {{apm-server}}'s OTel intake, note that this flow is not supported. Send data to an [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel Intake](opentelemetry://reference/motlp.md) instead.
:::

If you have an Elastic support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). If you don't, post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/apm-agent-android/issues).

## General troubleshooting

The SDK creates logs that allow you to see what it's working on and what might have failed at some point. You can find the logs in [logcat](https://developer.android.com/studio/debug/logcat), filtered by the tag `ELASTIC_AGENT`.

For more information about the SDK's internal logs, as well as how to configure them, refer to the [internal logging policy](apm-agent-android://reference/edot-android/configuration.md#internal-logging-policy) configuration. For more information on enabling debug logging, refer to [Enable debug logging for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).

## Connectivity to the {{stack}}

If after following the [getting started](apm-agent-android://reference/edot-android/getting-started.md) guide and configuring your {{stack}} [endpoint parameters](apm-agent-android://reference/edot-android/configuration.md#export-connectivity), you can't see your application's data in {{kib}}, you can follow the following tips to try and figure out what could be wrong. For more detailed connectivity troubleshooting, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md). If telemetry data isn't appearing in {{kib}}, refer to [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md) or [No data visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

### Check out the logs

The SDK prints debug logs, which can be seen in [logcat](https://developer.android.com/studio/debug/logcat), using the tag `ELASTIC_AGENT`, where you can have a look at your endpoint configuration parameters with a log that reads: _"Initializing connectivity with config [your endpoint configuration]"_. Take a look at those and make sure that the provided configuration matches your {{stack}} endpoint parameters.

### Inspect network traffic

You can take a look at your app's outgoing network requests via Android Studio's [network inspector tool](http://developer.android.com/studio/debug/network-profiler). This tool can show you the SDK's export requests, where you can see if they were successful or not, as well as the request body and the {{stack}} response body for when you need more details of the whole process. 

Apart from that, this tool also provides a way to export a file with the information of all of your app's HTTP requests, which you could share with our support team if needed.

### SSL/TLS error

Sometimes the request to the {{stack}} endpoint won't show up in the [network inspector](#inspect-network-traffic). A common issue when this happens is that there is an SSL/TLS error that occurs when the SDK tries to contact your {{stack}} endpoint. This is often the case when you work with an on-prem {{stack}} that doesn't have trusted CAs, for which you'd need to add custom security configurations to your app to make the export work. Take a look at [how to configure SSL/TLS](#how-ssl) for more information.

## How to configure SSL/TLS? [how-ssl]

Note that the Elastic Agent does not handle SSL/TLS configs internally. Therefore, you should manage these types of configurations as part of your app’s network security configurations, as explained in Android’s official [security guidelines](https://developer.android.com/privacy-and-security/security-ssl). Below we show a set of common use cases and quick tips on what could be done on each one. However, each case might be different, so please refer to Android’s [official docs](https://developer.android.com/privacy-and-security/security-config) on this topic if you need more details.

### Connecting to Elastic Cloud [how-ssl-elastic-cloud]

If your {{stack}} is hosted in {{ecloud}}, you shouldn’t need to add any SSL/TLS config changes in your app. It should work out of the box.

### Connecting to an on-prem server [how-ssl-on-prem]

If your {{stack}} is hosted on-prem, then it depends on the type of CA your host uses to sign its certificates. If it’s a commonly trusted CA, you shouldn’t have to worry about changing your app’s SSL/TLS configuration as it all should work well out of the box. However, if your CAs are unknown/private or your server uses a self-signed certificate, then you would need to configure your app to trust custom CAs by following [Android’s guide](https://developer.android.com/privacy-and-security/security-config).

### Debugging purposes [how-ssl-debug]

If you’re running a local server and need to connect to it without using https in order to run a quick test, then you could temporarily [enable cleartext traffic](https://developer.android.com/guide/topics/manifest/application-element#usesCleartextTraffic) within your `AndroidManifest.xml` file, inside the `<application>` tag. As shown below:

```xml
<application
    ...
    android:usesCleartextTraffic="true">
    ...
</application>
```

::::{note}
You should only enable cleartext traffic for debugging purposes and not for production code.
::::

If enabling cleartext traffic isn’t a valid option for your debugging use case, you should refer to Android’s guide on [configuring CAs for debugging](https://developer.android.com/privacy-and-security/security-config#TrustingDebugCa).

For more information on how Android handles network security, please refer to the official [Android docs](https://developer.android.com/privacy-and-security/security-ssl).

## Desugaring support [why-desugaring]

Android devices with an API level below 26 (older than [Android 8.0](https://developer.android.com/about/versions/oreo/android-8.0)) have limited support for Java 8 features and types, which can cause your app to crash when using those types while running on those older-than-8.0 devices. 

For example, if one of your app's dependencies uses the [Base64](https://docs.oracle.com/javase/8/docs/api/java/util/Base64.html) type ([added in API level 26](https://developer.android.com/reference/java/util/Base64)), and your app is installed on an Android device with OS version 7.0 ([API level 24](https://developer.android.com/about/versions/nougat/android-7.0)), a crash will happen when the code that uses said type is executed due to a "class not found" error.

To prevent these kinds of issues on devices using Android OS older than 8.0, you must add [Java 8 desugaring support](https://developer.android.com/studio/write/java8-support#library-desugaring) to your app. This requirement is inherited from the [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java/blob/main/VERSIONING.md#language-version-compatibility), which this project is built upon, where several of the unsupported types for Android versions older than 8.0 are used.

## App referred to as service [why-service]

For historic reasons, `service` has been the default way of referring to "an entity that produces telemetry". This term made its way into OpenTelemetry to a point where it was marked as one of the first "stable" resource names, meaning that it was no longer possible/feasible to make a change to another name that would better represent any kind of telemetry source. This has been debated several times within the community. A recent discussion attempts to [explain the `service` description](https://github.com/open-telemetry/semantic-conventions/pull/630) and what it should represent in an effort to reduce confusion. However, there doesn't seem to be a consensus.

## Get your Android application instance [get-application]

Your [Application](https://developer.android.com/reference/android/app/Application) instance is needed to initialize the agent. There are a couple of ways you can get yours.

#### From within your custom Application implementation (Recommended)

The agent should get initialized as soon as your application is launched to make sure that it can start collecting telemetry from the very beginning.

An ideal place to do so is from within your own custom [Application.onCreate](https://developer.android.com/reference/android/app/Application#onCreate()) method implementation, as shown in the following snippet:

```kotlin
package my.app

class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        val agent = ElasticApmAgent.builder(this) // <1>
            //...
            .build()
    }
}
```
1. `this` is your application.

:::{important}
You must register your custom application in your `AndroidManifest.xml` file, like so:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:name="my.app.MyApp"
        ...
    </application>
</manifest>
```
:::

### From an Activity

You can get your application from an [Activity](https://developer.android.com/reference/android/app/Activity) by calling its [getApplication()](https://developer.android.com/reference/android/app/Activity#getApplication()) method.

### From a Fragment

From a [Fragment](https://developer.android.com/reference/androidx/fragment/app/Fragment.html) instance, you can get the [Activity](https://developer.android.com/reference/android/app/Activity) that it is associated to by calling its [requireActivity()](https://developer.android.com/reference/androidx/fragment/app/Fragment.html#requireActivity()) method. After you get the Activity object, you can get your application from it as [explained above](#from-an-activity).

## Get your {{stack}} export endpoint [get-export-endpoint]

The export endpoint is where your app's telemetry is sent. The endpoint is required to initialize the agent. The way to find the endpoint in your {{stack}} depends on the type of deployment you use.

### Serverless deployments

On a [Serverless deployment](https://www.elastic.co/guide/en/serverless/current/intro.html), follow these steps:

1. Open {{kib}} and find **Add data** in the main menu. Alternatively, you can use the [global search field](../../../../../explore-analyze/find-and-organize/find-apps-and-objects.md) and search for `Observability Onboarding`.
2. Select **Application**, **OpenTelemetry**.
3. Select the **OpenTelemetry** tab, followed by **Managed OTLP Endpoint** under **Configure the OpenTelemetry SDK**.

Your export endpoint URL is the value for the `OTEL_EXPORTER_OTLP_ENDPOINT` configuration setting.

### Cloud hosted and self-managed deployments

For Elastic Cloud Hosted (ECH) and self-managed deployments, the export endpoint, also known as [EDOT Collector](elastic-agent://reference/edot-collector/index.md), is not available out of the box at the moment. You can still create your own service by [downloading](elastic-agent://reference/edot-collector/download.md) and [configuring an EDOT Collector](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode).

### Local testing deployment

You can quickly launch a local [EDOT Collector](elastic-agent://reference/edot-collector/index.md) service and use it as your export endpoint for testing by running the EDOT Collector launcher from the [Demo application](https://github.com/elastic/android-agent-demo/tree/main/edot-collector).

## Create an API key [create-api-key]

API keys are the recommended way of authenticating the agent with your {{stack}}. There's a couple of ways you can create one.

### Use {{kib}}'s Applications UI

Follow [this quick guide](../../../../../deploy-manage/api-keys/elasticsearch-api-keys.md#create-api-key) and leave all the settings with their default values.

### Use REST APIs

Follow [this guide](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) to create an API Key using REST APIs.

## Missing general attributes

Some [general attributes](https://opentelemetry.io/docs/specs/semconv/general/attributes/) require Android permissions to be granted for the host app; otherwise, they cannot be collected. The ones affected are the following:

| Attribute                    | Required permission                                                                                      |
|------------------------------|----------------------------------------------------------------------------------------------------------|
| `network.connection.subtype` | [READ_PHONE_STATE](https://developer.android.com/reference/android/Manifest.permission#READ_PHONE_STATE) |
