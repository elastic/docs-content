---
navigation_title: EDOT React Native
description: Resolve setup, build, and startup problems with the EDOT React Native SDK.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_react_native: preview 0.1.0
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshoot the EDOT React Native SDK [troubleshooting]

Use this guide to resolve React Native-specific setup, build, and startup
problems with {{product.edot-react-native}}. Check the
[requirements](elastic-otel-react-native://reference/edot-react-native/getting-started.md#requirements)
before troubleshooting.

In the messages below, placeholders such as `<path>` and `<key>` stand for
values from your project.

## Setup command cannot update the project [setup-layout]

### Symptoms [symptoms-setup-layout]

`setup-android` or `setup-ios` exits with an error and prints:

```text
No file was changed.
```

Android setup reports a missing file or insertion point:

```text
<path> was not found.
<path> has no line <anchor>.
```

iOS setup can report:

```text
The iOS project does not match the supported bare React Native template layout.
```

The following diagnostics identify the layout problem:

```text
package.json must declare a react-native dependency.
Cannot read package.json: <reason>
Expected exactly one iOS Xcode project, found <n>.
Cannot read the iOS Xcode project: <reason>
Missing supported Podfile anchor matching <pattern>.
Cannot read ios/Podfile: <reason>
```

An unreadable project structure or an unexpected number of application targets
can also produce:

```text
Cannot parse <project>: <reason>
Expected exactly one application target in <project>, found <n>.
```

### Causes [causes-setup-layout]

The command is running outside the application root, a required file is
missing, or the project differs from the supported bare React Native template.

### Resolution [resolution-setup-layout]

Run the command from the application's root directory. Check the named file
and diagnostic. For a customized project, follow
[Manual host setup fallback](elastic-otel-react-native://reference/edot-react-native/getting-started.md#manual-host-setup-fallback)
and the manual steps printed by the command. Review your changes before
building the app.

## Setup command cannot write a file [setup-write]

### Symptoms [symptoms-setup-write]

The setup command prints:

```text
Failed to update <path>: <reason>
```

### Causes [causes-setup-write]

The command cannot write the named file. The reason in the message identifies
the filesystem error.

### Resolution [resolution-setup-write]

Resolve the reported filesystem error, check `git diff` for any edits already
made, and rerun the setup command. If you apply the edits yourself, use
[Manual host setup fallback](elastic-otel-react-native://reference/edot-react-native/getting-started.md#manual-host-setup-fallback).

## Android build fails on the minimum API level [android-api-level]

### Symptoms [symptoms-android-api-level]

The Android build stops with:

```text
EDOT React Native: variant '<variant>' has minSdk <n> without Java 8 library desugaring. Raise minSdk to 26, or keep minSdk at 24 or higher and enable Java 8 library desugaring with coreLibraryDesugaringEnabled and a coreLibraryDesugaring dependency.
```

Below API level 24, the Android manifest merger reports a minimum SDK conflict.

### Causes [causes-android-api-level]

The affected variant does not meet the
[Android API requirements](elastic-otel-react-native://reference/edot-react-native/getting-started.md#requirements).

### Resolution [resolution-android-api-level]

Raise the app's `minSdk` to 26, or use API level 24 or later with
[Java 8 library desugaring](../android/index.md#why-desugaring).
Check the `minSdk` for the variant named in the error.

## Configuration file is missing [missing-configuration]

### Symptoms [symptoms-missing-configuration]

The Android build warns:

```text
EDOT React Native: <path>/elastic-otel-config.json was not found. ElasticOtelReactNative.initialize(this) fails at startup without it.
```

At startup, initialization throws one of these messages:

```text
elastic-otel-config.json was not found in the app assets. Create it at the React Native project root and apply the bridge's Gradle script in android/app/build.gradle.
elastic-otel-config.json was not found in the app bundle. Create it at the React Native project root, run setup-ios, and check that the file is in the app target's Copy Bundle Resources build phase.
```

`npx expo prebuild` can fail with:

```text
elastic-otel-config.json was not found. Create it at the project root, next to package.json.
```

### Causes [causes-missing-configuration]

The configuration file is absent from the application root or was not included
in the app build.

### Resolution [resolution-missing-configuration]

Create the file as described in
[Configuration file](elastic-otel-react-native://reference/edot-react-native/configuration.md#configuration-file).
For a bare app, complete `setup-android` or `setup-ios` and the
[manual host setup](elastic-otel-react-native://reference/edot-react-native/getting-started.md#manual-host-setup-fallback)
as needed. For Expo, follow
[Set up an Expo app](elastic-otel-react-native://reference/edot-react-native/getting-started.md#set-up-an-expo-app).
Rebuild the app after correcting the file or project setup.

## Initialization rejects configuration [invalid-configuration]

### Symptoms [symptoms-invalid-configuration]

`initialize()` throws `BootstrapException`. JSON structure, key, and type
errors include:

```text
elastic-otel-config.json must contain one JSON object: <detail>
elastic-otel-config.json contains the unknown key <key>.
elastic-otel-config.json is missing the required key exportUrl.
elastic-otel-config.json key <key> must be a string.
elastic-otel-config.json key <key> must be a number.
elastic-otel-config.json key exportProtocol must be "http" or "grpc", not "<value>".
elastic-otel-config.json key resourceAttributes must be an object.
elastic-otel-config.json key resourceAttributes.<key> must be a string.
```

Export URL errors include:

```text
An OTLP export URL is required.
The OTLP export URL is invalid.
The OTLP export URL must use http or https.
The OTLP export URL must include a host.
The OTLP base URL must not include a query or fragment.
The OTLP base URL must not include a signal-specific path.
```

Sampling, service identity, resource attribute, and API key errors include:

```text
The session sample rate must be between 0 and 1.
The resource attribute service.name is required.
Resource attribute keys must not be blank.
The resource attribute <key> must not be blank.
The resource attribute key <key> must be at most 255 printable ASCII characters.
The API key must not be blank.
```

### Causes [causes-invalid-configuration]

The configuration file or configuration supplied in code does not satisfy the
validation rules. Initialization stops before telemetry starts.

### Resolution [resolution-invalid-configuration]

Correct the setting named in the error using the
[configuration reference](elastic-otel-react-native://reference/edot-react-native/configuration.md).
See [Initialization and errors](elastic-otel-react-native://reference/edot-react-native/configuration.md#initialization-and-errors)
for error handling. Rebuild the app after changing its configuration file.

## Initialization runs more than once or fails on iOS [initialization]

### Symptoms [symptoms-initialization]

Initialization throws one of these messages:

```text
EDOT Android has already been initialized.
EDOT iOS has already been initialized.
EDOT iOS was initialized outside @elastic/otel-react-native.
EDOT iOS failed to initialize.
```

### Causes [causes-initialization]

The first two messages indicate a duplicate initialization call. On iOS, the
third indicates that the app also initializes EDOT iOS separately. The last
message indicates that iOS initialization did not succeed.

### Resolution [resolution-initialization]

Check the app's startup code against
[Bootstrap before React Native](elastic-otel-react-native://reference/edot-react-native/getting-started.md#bootstrap-before-react-native)
and [Initialization and errors](elastic-otel-react-native://reference/edot-react-native/configuration.md#initialization-and-errors).
Keep one EDOT React Native initialization call and remove separate EDOT iOS
initialization. If iOS initialization fails, inspect the startup logs and use
the [iOS troubleshooting guide](../ios/index.md) for native SDK problems.

## JavaScript cannot access the SDK [javascript-startup]

### Symptoms [symptoms-javascript-startup]

A JavaScript call throws:

```text
@elastic/otel-react-native is unavailable. Native autolinking must be enabled and the app rebuilt.
```

Manual telemetry calls can also reject with code `E_ELASTIC_OTEL_REACT_NATIVE`
and one of these messages:

```text
EDOT Android is not initialized. Bootstrap it in Application.onCreate.
EDOT iOS is not initialized. Bootstrap it in AppDelegate before React Native starts.
```

### Causes [causes-javascript-startup]

The app build does not include the package's native module, or initialization
has not completed successfully before the JavaScript call.

### Resolution [resolution-javascript-startup]

Enable native autolinking, complete the platform's
[getting-started steps](elastic-otel-react-native://reference/edot-react-native/getting-started.md),
and rebuild the native app. Reloading JavaScript does not rebuild the app.
For an initialization rejection, check the startup logs for a configuration
error and confirm that
[bootstrap runs before React Native starts](elastic-otel-react-native://reference/edot-react-native/getting-started.md#bootstrap-before-react-native).

## Expo config plugin cannot edit a generated file [expo-layout]

### Symptoms [symptoms-expo-layout]

`npx expo prebuild` fails with:

```text
<file> has no <anchor>.
<file> is not Kotlin. Add the bootstrap lines from the getting-started guide manually.
<file> is not Swift. Add the bootstrap lines from the getting-started guide manually.
```

### Causes [causes-expo-layout]

A generated file lacks a line that the package's config plugin inserts after,
`MainApplication` is not Kotlin, or `AppDelegate` is not Swift. The config
plugin edits only the Kotlin `MainApplication` and Swift `AppDelegate` that the
Expo template generates, and checks the language before it edits either file.

### Resolution [resolution-expo-layout]

For a missing line in a Gradle file, add the lines from
[Manual host setup fallback](elastic-otel-react-native://reference/edot-react-native/getting-started.md#manual-host-setup-fallback)
to the named file. For a missing line in `MainApplication` or `AppDelegate`,
add the lines from
[Bootstrap before React Native](elastic-otel-react-native://reference/edot-react-native/getting-started.md#bootstrap-before-react-native).
The config plugin skips lines that are already present.

For a `MainApplication` that is not Kotlin or an `AppDelegate` that is not
Swift, restore the Kotlin or Swift file that the Expo template generates.
Adding the bootstrap lines by hand does not resolve this error while the
package's config plugin is listed in `expo.plugins`.

## Babel plugin options stop the Metro transform [babel-options]

### Symptoms [symptoms-babel-options]

Metro reports a `TypeError` naming a Babel plugin option, for example:

```text
Unknown option interactions.<name>.
interactions.components must be an array.
interactions.components[0].name is required.
interactions.components[0] must list an instrumentation in instrumentations or set enabled: false.
interactions.widgetId[1] follows @component, which always has a value, so it is never used.
```

### Causes [causes-babel-options]

The plugin options contain an unknown key, an invalid type, an incomplete or
duplicate component entry, an unsupported instrumentation or macro, or a
source listed after `@component`.

### Resolution [resolution-babel-options]

Correct the option named in the error using the
[Babel plugin configuration](elastic-otel-react-native://reference/edot-react-native/automatic-instrumentation.md#configuration).
Restart Metro with a cleared cache after changing the options.

## Widget taps are missing [missing-taps]

### Symptoms [symptoms-missing-taps]

Tapping a component produces no widget tap event.

### Causes [causes-missing-taps]

The bundle does not include the Babel plugin changes, tap instrumentation is
turned off, or the element does not match the plugin's instrumentation rules.

### Resolution [resolution-missing-taps]

Check the [widget tap setup and supported components](elastic-otel-react-native://reference/edot-react-native/automatic-instrumentation.md#widget-tap-events).
Reset the Metro cache with `npx react-native start --reset-cache` or
`npx expo start --clear`. Use the
[`debug: true` report](elastic-otel-react-native://reference/edot-react-native/automatic-instrumentation.md#report-skipped-elements)
to identify skipped elements.

## Next steps [next-steps]

For problems outside React Native setup and startup, use these guides:

* Native SDK problems: [Android troubleshooting](../android/index.md) and
  [iOS troubleshooting](../ios/index.md).
* Export and connectivity:
  [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md),
  [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md),
  and [No data visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).
* Diagnostics:
  [Enable SDK debug logging](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).
* Kibana visualizations:
  [Android dashboard troubleshooting](integration-docs://reference/otel_android_dashboards.md#troubleshooting)
  and [iOS dashboard troubleshooting](integration-docs://reference/otel_ios_dashboards.md#troubleshooting).

If the problem persists, existing Elastic customers with a support contract
can open a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/).
Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm).
