---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/get-started-with-fleet-apm-server.html
---

# Fleet-managed APM Server [get-started-with-fleet-apm-server]

This guide will explain how to set up and configure a Fleet-managed APM Server.


## Prerequisites [_prerequisites_6]

You need {{es}} for storing and searching your data, and {{kib}} for visualizing and managing it. When setting these components up, you need:

* {{es}} cluster and {{kib}} (version 9.0) with a basic license or higher. [Learn how to install the {{stack}} on your own hardware](../../../get-started/the-stack.md).
* Secure, encrypted connection between {{kib}} and {{es}}. For more information, see [Start the {{stack}} with security enabled](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md).
* Internet connection for {{kib}} to download integration packages from the {{package-registry}}. Make sure the {{kib}} server can connect to `https://epr.elastic.co` on port `443`. If your environment has network traffic restrictions, there are ways to work around this requirement. See [Air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md) for more information.
* {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}. Since many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces.
* In the {{es}} configuration, the [built-in API key service](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/security-settings.md#api-key-service-settings) must be enabled. (`xpack.security.authc.api_key.enabled: true`)
* In the {{kib}} configuration, the saved objects encryption key must be set. {{fleet}} requires this setting in order to save API keys and encrypt them in {{kib}}. You can either set `xpack.encryptedSavedObjects.encryptionKey` to an alphanumeric value of at least 32 characters, or run the [`kibana-encryption-keys` command](asciidocalypse://docs/kibana/docs/reference/commands/kibana-encryption-keys.md) to generate the key.

**Example security settings**

For testing purposes, you can use the following settings to get started quickly, but make sure you properly secure the {{stack}} before sending real data.

elasticsearch.yml example:

```yaml
xpack.security.enabled: true
xpack.security.authc.api_key.enabled: true
```

kibana.yml example:

```yaml
elasticsearch.username: "kibana_system" <1>
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"
```

1. The password should be stored in the {{kib}} keystore as described in the [{{es}} security documentation](../../../deploy-manage/security/set-up-minimal-security.md).



## Step 1: Set up Fleet [_step_1_set_up_fleet]

Use {{fleet}} in {{kib}} to get APM data into the {{stack}}.

::::{note}
If you already have a {{fleet-server}} set up, you can choose to skip this step.

::::


The first time you use {{fleet}}, you’ll need to set it up and add a {{fleet-server}} using the steps outlined below.

To deploy a self-managed {{fleet-server}}, you install an {{agent}} and enroll it in an agent policy containing the {{fleet-server}} integration.

::::{note}
You can install only a single {{agent}} per host, which means you cannot run {{fleet-server}} and another {{agent}} on the same host unless you deploy a containerized {{fleet-server}}.
::::


1. In {{fleet}}, open the **Settings** tab. For more information about these settings, see [{{fleet}} settings](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-settings.md).
2. Under **Fleet Server hosts**, click **Edit hosts** and specify one or more host URLs your {{agent}}s will use to connect to {{fleet-server}}. For example, `https://192.0.2.1:8220`, where `192.0.2.1` is the host IP where you will install {{fleet-server}}. Save and apply your settings.

    ::::{tip}
    If the **Edit hosts** option is grayed out, {{fleet-server}} hosts are configured outside of {{fleet}}. For more information, refer to [{{fleet}} settings in {{kib}}](asciidocalypse://docs/kibana/docs/reference/configuration-reference/fleet-settings.md).
    ::::

3. In the **{{es}} hosts** field, specify the {{es}} URLs where {{agent}}s will send data. For example, `https://192.0.2.0:9200`. Skip this step if you’ve started the {{stack}} with security enabled (you cannot change this setting because it’s managed outside of {{fleet}}).
4. Save and apply the settings.
5. Click the **Agents** tab and follow the in-product instructions to add a {{fleet}} server:

    :::{image} ../../../images/observability-add-fleet-server.png
    :alt: In-product instructions for adding a {{fleet-server}}
    :class: screenshot
    :::


**Notes:**

* Choose **Quick Start** if you want {{fleet}} to generate a {{fleet-server}} policy and enrollment token for you. The {{fleet-server}} policy will include a {{fleet-server}} integration plus a system integration for monitoring {{agent}}. This option generates self-signed certificates and is not recommended for production use cases.
* Choose **Advanced** if you want to either:

    * Use your own {{fleet-server}} policy. You can create a new {{fleet-server}} policy or select an existing one. Alternatively you can [create a {{fleet-server}} policy without using the UI](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/create-policy-no-ui.md), and select the policy here.
    * Use your own TLS certificates to encrypt traffic between {{agent}}s and {{fleet-server}}. To learn how to generate certs, refer to [Configure SSL/TLS for self-managed {{fleet-server}}s](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/secure-connections.md).

* It’s recommended you generate a unique service token for each {{fleet-server}}. For other ways to generate service tokens, see [`elasticsearch-service-tokens`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/service-tokens-command.md).
* If you are providing your own certificates:

    * Before running the `install` command, make sure you replace the values in angle brackets.
    * Note that the URL specified by `--url` must match the DNS name used to generate the certificate specified by `--fleet-server-cert`.

* The `install` command installs the {{agent}} as a managed service and enrolls it in a {{fleet-server}} policy. For more {{fleet-server}} commands, see [{{agent}} command reference](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/agent-command-reference.md).

If installation is successful, you’ll see confirmation that {{fleet-server}} connected. Click **Continue enrolling Elastic Agent** to begin enrolling your agents in {{fleet-server}}.

::::{note}
If you’re unable to add a {{fleet}}-managed agent, click the **Agents** tab and confirm that the agent running {{fleet-server}} is healthy.
::::


For more information, refer to [{{fleet-server}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-server.md).


## Step 2: Add and configure the APM integration [add-apm-integration]

::::{note}
If you don’t have a {{fleet}} setup already in place, the easiest way to get started is to run the APM integration in the same {{agent}} that acts as the {{fleet-server}}. However, it is *not mandatory* for the APM integration to run in the same {{agent}} that acts as the {{fleet-server}}.

::::


1. In {{kib}}, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Elastic APM**.

    :::{image} ../../../images/observability-kibana-fleet-integrations-apm.png
    :alt: {{fleet}} showing APM integration
    :class: screenshot
    :::

3. Click **Add Elastic APM**.

    :::{image} ../../../images/observability-kibana-fleet-integrations-apm-overview.png
    :alt: {{fleet}} showing APM integration overview
    :class: screenshot
    :::

4. On the **Add Elastic APM integration** page, define the host and port where APM Server will listen. Make a note of this value—​you’ll need it later.

    ::::{tip}
    Using Docker or Kubernetes? Set the host to `0.0.0.0` to bind to all interfaces.
    ::::

5. Under **Agent authorization**, set a Secret token. This will be used to authorize requests from APM agents to the APM Server. Make a note of this value—​you’ll need it later.
6. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains an APM integration policy for the configuration you just specified.
7. To view the new policy, click **Agent policy 1**.

    :::{image} ../../../images/observability-apm-agent-policy-1.png
    :alt: {{fleet}} showing apm policy
    :class: screenshot
    :::

    Any {{agent}}s assigned to this policy will collect APM data from your instrumented services.


::::{tip}
An internet connection is required to install the APM integration via the Fleet UI in Kibana.

::::{dropdown} If you don’t have an internet connection
If your environment has network traffic restrictions, there are other ways to install the APM integration. See [Air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md) for more information.

Option 1: Update `kibana.yml`
:   Update `kibana.yml` to include the following, then restart {{kib}}.

```yaml
xpack.fleet.packages:
- name: apm
  version: latest
```

See [Configure Kibana](../../../deploy-manage/deploy/self-managed/configure.md) to learn more about how to edit the Kibana configuration file.


Option 2: Use the {{fleet}} API
:   Use the {{fleet}} API to install the APM integration. To be successful, this needs to be run against the {{kib}} API, not the {{es}} API.

```yaml
POST kbn:/api/fleet/epm/packages/apm/9.0.0
{ "force": true }
```

See [Kibana API](https://www.elastic.co/guide/en/kibana/current/api.html) to learn more about how to use the Kibana APIs.


::::


::::



## Step 3: Install APM agents [_step_3_install_apm_agents]

APM agents are written in the same language as your service. To monitor a new service, you must install the agent and configure it with a service name, APM Server host, and Secret token.

* **Service name**: The APM integration maps an instrumented service’s name–defined in each {{apm-agent}}'s configuration– to the index that its data is stored in {{es}}. Service names are case-insensitive and must be unique. For example, you cannot have a service named `Foo` and another named `foo`. Special characters will be removed from service names and replaced with underscores (`_`).
* **APM Server URL**: The host and port that APM Server listens for events on. This should match the host and port defined when setting up the APM integration.
* **Secret token**: Authentication method for {{apm-agent}} and APM Server communication. This should match the secret token defined when setting up the APM integration.

::::{tip}
You can edit your APM integration settings if you need to change the APM Server URL or secret token to match your APM agents.
::::


:::::::{tab-set}

::::::{tab-item} Android
**1. Add the agent to your project**

First, add the [Elastic APM agent plugin](https://plugins.gradle.org/plugin/co.elastic.apm.android) to your application’s `build.gradle` file as shown below:

```groovy
// Android app's build.gradle file
plugins {
    id "com.android.application"
    id "co.elastic.apm.android" version "[latest_version]" <1>
}
```

1. The Elastic plugin declaration must be added below the Android app plugin declaration (`com.android.application`) and below the Kotlin plugin declaration (if used).


**2. Configure the agent**

After adding the agent plugin, configure it. A minimal configuration sets the Elastic APM integration endpoint as shown below:

```groovy
// Android app's build.gradle file
plugins {
    //...
    id "co.elastic.apm.android" version "[latest_version]" <1>
}

elasticApm {
    // Minimal configuration
    serverUrl = "https://your.elastic.server"

    // Optional
    serviceName = "your app name" <2>
    serviceVersion = "0.0.0" <3>
    apiKey = "your server api key" <4>
    secretToken = "your server auth token" <5>
}
```

1. You can find the latest version in the [Gradle plugin portal](https://plugins.gradle.org/plugin/co.elastic.apm.android).
2. Defaults to your `android.defaultConfig.applicationId` value.
3. Defaults to your `android.defaultConfig.versionName` value.
4. Defaults to null. More info on API Keys [here](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).
5. Defaults to null.


::::{note}
When both `secretToken` and `apiKey` are provided, apiKey has priority and secretToken is ignored.
::::


**3. Initialize the agent**

After syncing your project with the Gradle changes above, the Elastic APM agent needs to be initialized within your [Application class](https://developer.android.com/reference/android/app/Application). This example shows the simplest way to configure the agent:

```java
// Your Application class

class MyApp extends android.app.Application {

    @Override
    public void onCreate() {
        super.onCreate();
        ElasticApmAgent.initialize(this); <1>
    }
}
```

1. Initialize the Elastic APM agent once.


All that’s left is to compile and run your application. That’s it!

**Learn more in the agent reference**

Read more in the [APM Android Agent Reference](asciidocalypse://docs/apm-agent-android/docs/reference/index.md).
::::::

::::::{tab-item} Go
**1. Install the agent**

Install the Elastic APM Go agent package using `go get`:

```bash
go get -u go.elastic.co/apm/v2
```

**2. Configure the agent**

To simplify development and testing, the agent defaults to sending data to the Elastic APM integration at `http://localhost:8200`. To send data to an alternative location, you must configure `ELASTIC_APM_SERVER_URL`.

```go
# The APM integration host and port
export ELASTIC_APM_SERVER_URL=

# If you do not specify `ELASTIC_APM_SERVICE_NAME`, the Go agent will use the
# executable name. For example, if your executable is called "my-app.exe", then your
# service will be identified as "my-app".
export ELASTIC_APM_SERVICE_NAME=

# Secret tokens are used to authorize requests to the APM integration
export ELASTIC_APM_SECRET_TOKEN=
```

**3. Instrument your application**

Instrumentation is the process of extending your application’s code to report trace data to Elastic APM. Go applications must be instrumented manually at the source code level. To instrument your applications, use one of the following approaches:

* [Built-in instrumentation modules](asciidocalypse://docs/apm-agent-go/docs/reference/builtin-modules.md).
* [Custom instrumentation](asciidocalypse://docs/apm-agent-go/docs/reference/custom-instrumentation.md) and context propagation with the Go Agent API.

**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-go/docs/reference/supported-technologies.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md)
* [Detailed guide to instrumenting Go source code](asciidocalypse://docs/apm-agent-go/docs/reference/set-up-apm-go-agent.md)
::::::

::::::{tab-item} iOS
**1. Add the agent dependency to your project**

Add the Elastic APM iOS Agent to your Xcode project or your `Package.swift`.

Here are instructions for adding a [package dependency](https://developer.apple.com/documentation/swift_packages/adding_package_dependencies_to_your_app) to a standard Xcode project.

Refer to [*Add a Dependency on Another Swift Package*](https://developer.apple.com/documentation/xcode/creating_a_standalone_swift_package_with_xcode#3578941) for details about adding dependencies to your `Package.swift`. Here is a helpful code-snippet:

```swift
Package(
    dependencies:[
         .package(name: "apm-agent-ios", url: "https://github.com/elastic/apm-agent-ios.git", from: "1.0.0"),
    ],
  targets:[
    .target(
        name: "MyApp",
        dependencies: [
            .product(name: "ElasticApm", package: "apm-agent-ios")
        ]
    ),
])
```

**2. Initialize the agent**

If you’re using `SwiftUI` to build your app, add the following to your `App.swift`:

```swift
import SwiftUI
import ElasticApm

class AppDelegate : NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        var config = AgentConfigBuilder()
            .withServerUrl(URL(string:"http://127.0.0.1:8200")) <1>
            .withSecretToken("<SecretToken>") <2>
            .build()

        ElasticApmAgent.start(with: config)
        return true
    }
}

@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    init() {
    }
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

1. The APM integration host and port
2. Secret token for APM integration connection


If you’re not using `SwiftUI`, you can alternatively add the same thing to your `AppDelegate.swift` file:

```swift
import UIKit
import ElasticApm
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
var config = AgentConfigBuilder()
                       .withServerUrl(URL(string:"http://127.0.0.1:8200")) <1>
                       .withSecretToken("<SecretToken>") <2>
                       .build()
        ElasticApmAgent.start(with: config)
        return true
    }
}
```

1. The APM integration host and port
2. Secret token for APM integration connection


**Learn more in the agent reference**

Read more in the [APM iOS Agent Reference](asciidocalypse://docs/apm-agent-ios/docs/reference/index.md).
::::::

::::::{tab-item} Java
Manually set up and configure the agent with the `-javaagent` JVM option. No application code change is required, but this requires an application restart. See below for more information on this setup method.

**1. Download the {{apm-agent}}**

The first step in getting started with the Elastic APM Java agent is to retrieve a copy of the agent JAR. Java agent releases are published to [Maven central](https://repo.maven.apache.org/maven2/). In order to get a copy you can either:

* download the [latest agent](https://oss.sonatype.org/service/local/artifact/maven/redirect?r=releases&g=co.elastic.apm&a=elastic-apm-agent&v=LATEST) or [previous releases](https://mvnrepository.com/artifact/co.elastic.apm/elastic-apm-agent) from Maven central.
* download with `curl`:

    ```bash
    curl -o 'elastic-apm-agent.jar' -L 'https://oss.sonatype.org/service/local/artifact/maven/redirect?r=releases&g=co.elastic.apm&a=elastic-apm-agent&v=LATEST'
    ```


**2. Add `-javaagent` flag**

When starting your application, add the JVM flag `-javaagent:/path/to/elastic-apm-agent-<version>.jar`

**3. Configure**

Different application servers have different ways of setting the `-javaagent` flag and system properties. Start your application (for example a Spring Boot application or other embedded servers) and add the `-javaagent` JVM flag. Use the `-D` prefix to configure the agent using system properties:

```bash
java -javaagent:/path/to/elastic-apm-agent-<version>.jar -Delastic.apm.service_name=my-cool-service -Delastic.apm.application_packages=org.example,org.another.example -Delastic.apm.server_url=http://127.0.0.1:8200 -jar my-application.jar
```

Refer to [Manual setup with `-javaagent` flag](asciidocalypse://docs/apm-agent-java/docs/reference/setup-javaagent.md) to learn more.

**Alternate setup methods**

* **Automatic setup with `apm-agent-attach-cli.jar`**<br> Automatically set up the agent without needing to alter the configuration of your JVM or application server. This method requires no changes to application code or JVM options, and allows attaching to a running JVM. Refer to the [Java agent documentation](asciidocalypse://docs/apm-agent-java/docs/reference/setup-attach-cli.md) for more information on this setup method.
* **Programmatic API setup to self-attach**<br> Set up the agent with a one-line code change and an extra `apm-agent-attach` dependency. This method requires no changes to JVM options, and the agent artifact is embedded within the packaged application binary. Refer to the [Java agent documentation](asciidocalypse://docs/apm-agent-java/docs/reference/setup-attach-api.md) for more information on this setup method.
::::::

::::::{tab-item} .NET
**Set up the {{apm-agent}}**

The .NET agent can be added to an application in a few different ways:

* **Profiler runtime instrumentation**: The agent supports auto instrumentation without any code change and without any recompilation of your projects. See [Profiler auto instrumentation](asciidocalypse://docs/apm-agent-dotnet/docs/reference/setup-auto-instrumentation.md).
* **NuGet packages**: The agent ships as a set of [NuGet packages](asciidocalypse://docs/apm-agent-dotnet/docs/reference/nuget-packages.md) available on [nuget.org](https://nuget.org). You can add the Agent and specific instrumentations to a .NET application by referencing one or more of these packages and following the package documentation.
* **Host startup hook**: On .NET Core 3.0+ or .NET 5+, the agent supports auto instrumentation without any code change and without any recompilation of your projects. See [Zero code change setup on .NET Core](asciidocalypse://docs/apm-agent-dotnet/docs/reference/setup-dotnet-net-core.md) for more details.

**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-dotnet/docs/reference/supported-technologies.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-dotnet/docs/reference/configuration.md)
::::::

::::::{tab-item} Node.js
**1. Install the {{apm-agent}}**

Install the {{apm-agent}} for Node.js as a dependency to your application.

```js
npm install elastic-apm-node --save
```

**2. Initialization**

It’s important that the agent is started before you require **any** other modules in your Node.js application - i.e. before `http` and before your router etc.

This means that you should probably require and start the agent in your application’s main file (usually `index.js`, `server.js` or `app.js`).

Here’s a simple example of how Elastic APM is normally required and started:

```js
// Add this to the VERY top of the first file loaded in your app
var apm = require('elastic-apm-node').start({
  // Override service name from package.json
  // Allowed characters: a-z, A-Z, 0-9, -, _, and space
  serviceName: '',

  // Use if APM integration requires a token
  secretToken: '',

  // Use if APM integration uses API keys for authentication
  apiKey: '',

  // Set custom APM integration host and port (default: http://127.0.0.1:8200)
  serverUrl: '',
})
```

The agent will now monitor the performance of your application and record any uncaught exceptions.

**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-nodejs/docs/reference/supported-technologies.md)
* [Babel/ES Modules](asciidocalypse://docs/apm-agent-nodejs/docs/reference/advanced-setup.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuring-agent.md)
::::::

::::::{tab-item} PHP
**1. Install the agent**

Install the agent using one of the [packages for supported platforms](https://github.com/elastic/apm-agent-php/releases/latest).

To use the RPM Package (RHEL/CentOS and Fedora):

```bash
rpm -ivh <package-file>.rpm
```

To use the DEB package (Debian and Ubuntu):

```bash
dpkg -i <package-file>.deb
```

To use the APK package (Alpine):

```bash
apk add --allow-untrusted <package-file>.apk
```

If you can’t find your distribution, you can install the agent by building it from the source. The following instructions will build the APM agent using the same docker environment that Elastic uses to build our official packages.

::::{note}
The agent is currently only available for Linux operating system.
::::


1. Download the agent source from [https://github.com/elastic/apm-agent-php/](https://github.com/elastic/apm-agent-php/).
2. Execute the following commands to build the agent and install it:

```bash
cd apm-agent-php
# for linux glibc - libc distributions (Ubuntu, Redhat, etc)
export BUILD_ARCHITECTURE=linux-x86-64
# for linux with musl - libc distributions (Alpine)
export BUILD_ARCHITECTURE=linuxmusl-x86-64
# provide a path to php-config tool
export PHP_CONFIG=php-config

# build extensions
make -f .ci/Makefile build

# run extension tests
PHP_VERSION=`$PHP_CONFIG --version | cut -d'.' -f 1,2` make -f .ci/Makefile run-phpt-tests

# install agent extensions
sudo cp agent/native/_build/${BUILD_ARCHITECTURE}-release/ext/elastic_apm-*.so `$PHP_CONFIG --extension-dir`

# install automatic loader
sudo cp agent/native/_build/${BUILD_ARCHITECTURE}-release/loader/code/elastic_apm_loader.so `$PHP_CONFIG --extension-dir`
```

**2. Enable and configure the APM agent**

Enable and configure your agent inside of the `php.ini` file:

```ini
extension=elastic_apm_loader.so
elastic_apm.bootstrap_php_part_file=<repo root>/agent/php/bootstrap_php_part.php
```

**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-php/docs/reference/supported-technologies.md)
* [Configuration](asciidocalypse://docs/apm-agent-php/docs/reference/configuration.md)
::::::

::::::{tab-item} Python
Django
:   **1. Install the {{apm-agent}}**

Install the {{apm-agent}} for Python as a dependency.

```python
$ pip install elastic-apm
```

**2. Configure the agent**

Agents are libraries that run inside of your application process. APM services are created programmatically based on the `SERVICE_NAME`.

```python
# Add the agent to the installed apps
INSTALLED_APPS = (
  'elasticapm.contrib.django',
  # ...
)

ELASTIC_APM = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': '',

  # Use if APM integration requires a token
  'SECRET_TOKEN': '',

  # Set custom APM integration host and port (default: http://localhost:8200)
  'SERVER_URL': '',
}

# To send performance metrics, add our tracing middleware:
MIDDLEWARE = (
  'elasticapm.contrib.django.middleware.TracingMiddleware',
  #...
)
```


Flask
:   **1. Install the {{apm-agent}}**

Install the {{apm-agent}} for Python as a dependency.

```python
$ pip install elastic-apm[flask]
```

**2. Configure the agent**

Agents are libraries that run inside of your application process. APM services are created programmatically based on the `SERVICE_NAME`.

```python
# initialize using environment variables
from elasticapm.contrib.flask import ElasticAPM
app = Flask(__name__)
apm = ElasticAPM(app)

# or configure to use ELASTIC_APM in your application settings
from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': '',

  # Use if APM integration requires a token
  'SECRET_TOKEN': '',

  # Set custom APM integration host and port (default: http://localhost:8200)
  'SERVER_URL': '',
}

apm = ElasticAPM(app)
```


**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-python/docs/reference/supported-technologies.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md)
::::::

::::::{tab-item} Ruby
**1. Install the {{apm-agent}}**

Add the agent to your Gemfile.

```ruby
gem 'elastic-apm'
```

**2. Configure the agent**

Ruby on Rails
:   APM is automatically started when your app boots. Configure the agent by creating the config file `config/elastic_apm.yml`:

```ruby
# config/elastic_apm.yml:

# Set service name - allowed characters: a-z, A-Z, 0-9, -, _ and space
# Defaults to the name of your Rails app
service_name: 'my-service'

# Use if APM integration requires a token
secret_token: ''

# Set custom APM integration host and port (default: http://localhost:8200)
server_url: 'http://localhost:8200'
```


Rack
:   For Rack or a compatible framework, like Sinatra, include the middleware in your app and start the agent.

```ruby
# config.ru

app = lambda do |env|
  [200, {'Content-Type' => 'text/plain'}, ['ok']]
end

# Wraps all requests in transactions and reports exceptions
use ElasticAPM::Middleware

# Start an instance of the Agent
ElasticAPM.start(service_name: 'NothingButRack')

run app

# Gracefully stop the agent when process exits.
# Makes sure any pending transactions are sent.
at_exit { ElasticAPM.stop }
```

**Create a config file**

Create a config file config/elastic_apm.yml:

```ruby
# config/elastic_apm.yml:

# Set service name - allowed characters: a-z, A-Z, 0-9, -, _ and space
# Defaults to the name of your Rack app's class.
service_name: 'my-service'

# Use if APM integration requires a token
secret_token: ''

# Set custom APM integration host and port (default: http://localhost:8200)
server_url: 'http://localhost:8200'
```


**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-ruby/docs/reference/supported-technologies.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md)
::::::

::::::{tab-item} RUM
**1. Enable Real User Monitoring (RUM)**

RUM is disabled by default. Enable it by setting `Enable RUM` to `true`.

**2. Set up the agent**

Set up the agent with `<script>` tags or by using a bundler.

*Synchronous / Blocking Pattern*

Add a <script> tag to load the bundle and use the `elasticApm` global object to initialize the agent:

```html
<script src="https://<your-cdn-host>.com/path/to/elastic-apm-rum.umd.min-<version>.js" crossorigin></script>
<script>
  elasticApm.init({
    serviceName: '<instrumented-app>',
    serverUrl: '<apm-server-url>',
  })
</script>
```

*Asynchronous / Non-Blocking Pattern*

Loading the script asynchronously ensures the agent script will not block other resources on the page, however, it will still block browsers `onload` event.

```html
<script>
  ;(function(d, s, c) {
    var j = d.createElement(s),
      t = d.getElementsByTagName(s)[0]

    j.src = 'https://<your-cdn-host>.com/path/to/elastic-apm-rum.umd.min-<version>.js'
    j.onload = function() {elasticApm.init(c)}
    t.parentNode.insertBefore(j, t)
  })(document, 'script', {serviceName: '<instrumented-app>', serverUrl: '<apm-server-url>'})
</script>
```

*Using Bundlers*

Install the Real User Monitoring APM agent as a dependency to your application:

```bash
npm install @elastic/apm-rum --save
```

Configure the agent:

```js
import { init as initApm } from '@elastic/apm-rum'

const apm = initApm({

  // Set required service name (allowed characters: a-z, A-Z, 0-9, -, _, and space)
  serviceName: '',

  // Set custom APM integration host and port (default: http://localhost:8200)
  serverUrl: 'http://localhost:8200',

  // Set service version (required for sourcemap feature)
  serviceVersion: ''
})
```

**Learn more in the agent reference**

* [Supported technologies](asciidocalypse://docs/apm-agent-rum-js/docs/reference/supported-technologies.md)
* [Advanced configuration](asciidocalypse://docs/apm-agent-rum-js/docs/reference/configuration.md)
::::::

::::::{tab-item} OpenTelemetry
Elastic integrates with OpenTelemetry, allowing you to reuse your existing instrumentation to easily send observability data to the {{stack}}.

For more information on how to combine Elastic and OpenTelemetry, see [OpenTelemetry integration](use-opentelemetry-with-apm.md).
::::::

:::::::

## Step 4: View your data [_step_4_view_your_data]

Back in {{kib}}, under {{observability}}, select APM. You should see application performance monitoring data flowing into the {{stack}}!

:::{image} ../../../images/observability-kibana-apm-sample-data.png
:alt: Applications UI with data
:class: screenshot
:::
