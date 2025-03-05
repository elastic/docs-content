---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/get-started-with-apm-server-binary.html
applies_to:
  stack: all
---

# APM Server binary [get-started-with-apm-server-binary]

This guide will explain how to set up and configure the APM Server binary.


## Prerequisites [_prerequisites_7]

First, see the [Elastic Support Matrix](https://www.elastic.co/support/matrix) for information about supported operating systems and product compatibility.

You’ll need:

* **{{es}}** for storing and indexing data.
* **{{kib}}** for visualizing with the Applications UI.

We recommend you use the same version of {{es}}, {{kib}}, and APM Server. See [Installing the {{stack}}](../../../get-started/the-stack.md) for more information about installing these products.

:::{image} ../../../images/observability-apm-architecture-diy.png
:alt: Install Elastic APM yourself
:::


## Step 1: Install [apm-installing]

::::{note}
**Before you begin**: If you haven’t installed the {{stack}}, do that now. See [Learn how to install the {{stack}} on your own hardware](../../../get-started/the-stack.md).
::::


To download and install APM Server, use the commands below that work with your system. If you use `apt` or `yum`, you can [install APM Server from our repositories](#apm-setup-repositories) to update to the newest version more easily.

$$$apm-deb$$$
**deb:**

```shell
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-{{apm_server_version}}-amd64.deb
sudo dpkg -i apm-server-{{apm_server_version}}-amd64.deb
```

$$$apm-rpm$$$
**RPM:**

```shell
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-{{apm_server_version}}-x86_64.rpm
sudo rpm -vi apm-server-{{apm_server_version}}-x86_64.rpm
```

$$$apm-linux$$$
**Other Linux:**

```shell
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-{{apm_server_version}}-linux-x86_64.tar.gz
tar xzvf apm-server-{{apm_server_version}}-linux-x86_64.tar.gz
```

$$$apm-mac$$$
**Mac:**

```shell
curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-{{apm_server_version}}-darwin-x86_64.tar.gz
tar xzvf apm-server-{{apm_server_version}}-darwin-x86_64.tar.gz
```

$$$apm-installing-on-windows$$$
**Windows:**

1. Download the APM Server Windows zip file from the
https://www.elastic.co/downloads/apm/apm-server[downloads page].

1. Extract the contents of the zip file into `C:\Program Files`.

1. Rename the `apm-server-<version>-windows` directory to `APM-Server`.

1. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).
If you are running Windows XP, you may need to download and install PowerShell.

1. From the PowerShell prompt, run the following commands to install APM Server as a Windows service:

$$$apm-docker$$$
**Docker:**

See [Running on Docker](#apm-running-on-docker) for deploying Docker containers.


## Step 2: Set up and configure [apm-server-configuration]

Configure APM by editing the `apm-server.yml` configuration file. The location of this file varies by platform—​see the [Installation layout](installation-layout.md) for help locating it.

A minimal configuration file might look like this:

```yaml
apm-server:
  host: "localhost:8200" <1>
output.elasticsearch:
  hosts: ["localhost:9200"] <2>
  username: "elastic" <3>
  password: "changeme"
```

1. The `host:port` APM Server listens on.
2. The {{es}} `host:port` to connect to.
3. This example uses basic authentication. The user provided here needs the privileges required to publish events to {{es}}. To create a dedicated user for this role, see [Create a *writer* role](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-to-publish-events).


All available configuration options are outlined in [configuring APM Server](configure-apm-server.md).


## Step 3: Start [apm-server-starting]

In a production environment, you would put APM Server on its own machines, similar to how you run {{es}}. You *can* run it on the same machines as {{es}}, but this is not recommended, as the processes will be competing for resources.

To start APM Server, run:

```bash
./apm-server -e
```

::::{note}
The `-e` [global flag](apm-server-command-reference.md#apm-global-flags) enables logging to stderr and disables syslog/file output. Remove this flag if you’ve enabled logging in the configuration file. For Linux systems, see [APM Server status and logs](apm-server-systemd.md).
::::


You should see APM Server start up. It will try to connect to {{es}} on localhost port `9200` and expose an API to agents on port `8200`. You can change the defaults in `apm-server.yml` or by supplying a different address on the command line:

```bash
./apm-server -e -E output.elasticsearch.hosts=ElasticsearchAddress:9200 -E apm-server.host=localhost:8200
```


### Debian Package / RPM [apm-running-deb-rpm]

For Debian package and RPM installations, we recommend the `apm-server` process runs as a non-root user. Therefore, these installation methods create an `apm-server` user which you can use to start the process. In addition, APM Server will only start if the configuration file is [owned by the user running the process](apm-server-systemd.md#apm-config-file-ownership).

To start the APM Server in this case, run:

```bash
sudo -u apm-server apm-server [<argument...>]
```

By default, APM Server loads its configuration file from `/etc/apm-server/apm-server.yml`. See the [deb & rpm default paths](installation-layout.md) for a full directory layout.


## Step 4: Install APM agents [apm-next-steps]

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

## Step 5: View your data [_step_5_view_your_data]

Once you have at least one {{apm-agent}} sending data to APM Server, you can start visualizing your data in the [{{kib}} Applications UI](overviews.md).

:::{image} ../../../images/observability-kibana-apm-sample-data.png
:alt: Applications UI with data
:class: screenshot
:::


## Repositories for APT and YUM [apm-setup-repositories]

We have repositories available for APT and YUM-based distributions. Note that we provide binary packages, but no source packages.

We use the PGP key [D88E42B4](https://pgp.mit.edu/pks/lookup?op=vindex&search=0xD27D666CD88E42B4), {{es}} Signing Key, with fingerprint

```
4609 5ACC 8548 582C 1A26 99A9 D27D 666C D88E 42B4
```
to sign all our packages. It is available from [https://pgp.mit.edu](https://pgp.mit.edu).


### APT [_apt]

Version 9.0.0-beta1 of apm-server has not yet been released.


### YUM [_yum]

Version 9.0.0-beta1 of apm-server has not yet been released.


## Run APM Server on Docker [apm-running-on-docker]

Docker images for APM Server are available from the Elastic Docker registry. The base image is [ubuntu:22.04](https://hub.docker.com/_/ubuntu).

A list of all published Docker images and tags is available at [www.docker.elastic.co](https://www.docker.elastic.co).

These images are free to use under the Elastic license. They contain open source and free commercial features and access to paid commercial features. [Start a 30-day trial](../../../deploy-manage/license/manage-your-license-in-self-managed-cluster.md) to try out all of the paid commercial features. See the [Subscriptions](https://www.elastic.co/subscriptions) page for information about Elastic license levels.


### Pull the image [_pull_the_image]

Obtaining APM Server for Docker is as simple as issuing a `docker pull` command against the Elastic Docker registry and then, optionally, verifying the image.

However, version 9.0.0-beta1 of APM Server has not yet been released, so no Docker image is currently available for this version.


### Configure APM Server on Docker [_configure_apm_server_on_docker]

The Docker image provides several methods for configuring APM Server. The conventional approach is to provide a configuration file via a volume mount, but it’s also possible to create a custom image with your configuration included.


#### Example configuration file [_example_configuration_file]

Download this example configuration file as a starting point:

```sh
curl -L -O https://raw.githubusercontent.com/elastic/apm-server/master/apm-server.docker.yml
```


#### Volume-mounted configuration [_volume_mounted_configuration]

One way to configure APM Server on Docker is to provide `apm-server.docker.yml` via a volume mount. With `docker run`, the volume mount can be specified like this.

```sh
docker run -d \
  -p 8200:8200 \
  --name=apm-server \
  --user=apm-server \
  --volume="$(pwd)/apm-server.docker.yml:/usr/share/apm-server/apm-server.yml:ro" \
  docker.elastic.co/apm/apm-server:9.0.0-beta1 \
  --strict.perms=false -e \
  -E output.elasticsearch.hosts=["elasticsearch:9200"] <1> <2>
```

1. Substitute your {{es}} hosts and ports.
2. If you are using {{ech}}, replace the `-E output.elasticsearch.hosts` line with the Cloud ID and elastic password using the syntax shown earlier.



#### Customize your configuration [_customize_your_configuration]

The `apm-server.docker.yml` downloaded earlier should be customized for your environment. See [Configure APM Server](configure-apm-server.md) for more details. Edit the configuration file and customize it to match your environment then re-deploy your APM Server container.


#### Custom image configuration [_custom_image_configuration]

It’s possible to embed your APM Server configuration in a custom image. Here is an example Dockerfile to achieve this:

```dockerfile
FROM docker.elastic.co/apm/apm-server:9.0.0-beta1
COPY --chmod=0644 --chown=1000:1000 apm-server.yml /usr/share/apm-server/apm-server.yml
```
