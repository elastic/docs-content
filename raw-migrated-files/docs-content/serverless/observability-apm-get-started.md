# Get started with traces and APM [observability-apm-get-started]

<titleabbrev>Get started<titleabbrev>
::::{admonition} Required role
:class: note

The **Admin** role or higher is required to send APM data to Elastic. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


In this guide you’ll learn how to collect and send Application Performance Monitoring (APM) data to Elastic, then explore and visualize the data in real time.


## Step 1: Add data [add-apm-integration-agents]

You’ll use APM agents to send APM data from your application to Elastic. Elastic offers APM agents written in several languages and supports OpenTelemetry. Which agent you’ll use depends on the language used in your service.

To send APM data to Elastic, you must install an APM agent and configure it to send data to your project:

1. [Create a new {{obs-serverless}} project](../../../solutions/observability/get-started/create-an-observability-project.md), or open an existing one.
2. To install and configure one or more APM agents, do one of following:

    * In your Observability project, go to **Add data** → **Monitor my application performance** → **Elastic APM** and follow the prompts.
    * Use the following instructions:

        <div class="tabs" data-tab-group="apm-apm-get-started">
          <div role="tablist" aria-label="apm-apm-get-started">
            <button role="tab" aria-selected="true" aria-controls="apm-apm-get-started-go-panel" id="apm-apm-get-started-go-button">
              Go
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-java-panel" id="apm-apm-get-started-java-button" tabindex="-1">
              Java
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-net-panel" id="apm-apm-get-started-net-button" tabindex="-1">
              .NET
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-nodejs-panel" id="apm-apm-get-started-nodejs-button" tabindex="-1">
              Node.js
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-php-panel" id="apm-apm-get-started-php-button" tabindex="-1">
              PHP
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-python-panel" id="apm-apm-get-started-python-button" tabindex="-1">
              Python
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-ruby-panel" id="apm-apm-get-started-ruby-button" tabindex="-1">
              Ruby
            </button>
            <button role="tab" aria-selected="false" aria-controls="apm-apm-get-started-opentelemetry-panel" id="apm-apm-get-started-opentelemetry-button" tabindex="-1">
              OpenTelemetry
            </button>
          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-go-panel" aria-labelledby="apm-apm-get-started-go-button">
        **1. Install the agent**

        Install the {{apm-agent}} package using `go get`:

        ```go
        go get -u go.elastic.co/apm/v2
        ```

        **2. Configure the agent**

        To simplify development and testing, the agent defaults to sending data to Elastic at `http://localhost:8200`. To send data to an alternative location, you must configure `ELASTIC_APM_SERVER_URL`.

        ```go
        # The APM integration host and port
        export ELASTIC_APM_SERVER_URL=

        # If you do not specify `ELASTIC_APM_SERVICE_NAME`, the Go agent will use the
        # executable name. For example, if your executable is called "my-app.exe", then your
        # service will be identified as "my-app".
        export ELASTIC_APM_SERVICE_NAME=

        # API keys are used to authorize requests to the APM integration
        export ELASTIC_APM_API_KEY=
        ```

        **3. Instrument your application**

        Instrumentation is the process of extending your application’s code to report trace data to Elastic APM. Go applications must be instrumented manually at the source code level. To instrument your applications, use one of the following approaches:

        * [Built-in instrumentation modules](apm-agent-go://reference/builtin-modules.md).
        * [Custom instrumentation](apm-agent-go://reference/custom-instrumentation.md) and context propagation with the Go Agent API.

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](apm-agent-go://reference/supported-technologies.md)
        * [Advanced configuration](apm-agent-go://reference/configuration.md)
        * [Detailed guide to instrumenting Go source code](apm-agent-go://reference/set-up-apm-go-agent.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-java-panel" aria-labelledby="apm-apm-get-started-java-button" hidden="">
        Manually set up and configure the agent with the `-javaagent` JVM option. No application code change is required, but this requires an application restart. See below for more information on this setup method.

        **1. Download the {{apm-agent}}**

        The first step in getting started with the Elastic APM Java agent is to retrieve a copy of the agent JAR. Java agent releases are published to [Maven central](https://repo.maven.apache.org/maven2/). In order to get a copy you can either:

        * download the [latest agent](https://oss.sonatype.org/service/local/artifact/maven/redirect?r=releases&g=co.elastic.apm&a=elastic-apm-agent&v=LATEST) or a [previous release](https://mvnrepository.com/artifact/co.elastic.apm/elastic-apm-agent) from Maven central.
        * download with `curl`:

            ```bash
            curl -o 'elastic-apm-agent.jar' -L 'https://oss.sonatype.org/service/local/artifact/maven/redirect?r=releases&g=co.elastic.apm&a=elastic-apm-agent&v=LATEST'
            ```


        **2. Add `-javaagent` flag**

        When starting your application, add the JVM flag: `-javaagent:/path/to/elastic-apm-agent-<version>.jar`.

        **3. Configure**

        Different application servers have different ways of setting the `-javaagent` flag and system properties. Start your application (for example a Spring Boot application or other embedded servers) and add the `-javaagent` JVM flag. Use the `-D` prefix to configure the agent using system properties:

        ```bash
        java -javaagent:/path/to/elastic-apm-agent-<version>.jar -Delastic.apm.service_name=my-cool-service -Delastic.apm.application_packages=org.example,org.another.example -Delastic.apm.server_url=http://127.0.0.1:8200 -jar my-application.jar
        ```

        Refer to [Manual setup with `-javaagent` flag](apm-agent-java://reference/setup-javaagent.md) to learn more.

        **Alternate setup methods**

        * **Automatic setup with `apm-agent-attach-cli.jar`** Automatically set up the agent without needing to alter the configuration of your JVM or application server. This method requires no changes to application code or JVM options, and allows attaching to a running JVM. Refer to the [Java agent documentation](apm-agent-java://reference/setup-attach-cli.md) for more information on this setup method.
        * **Programmatic API setup to self-attach** Set up the agent with a one-line code change and an extra `apm-agent-attach` dependency. This method requires no changes to JVM options, and the agent artifact is embedded within the packaged application binary. Refer to the [Java agent documentation](apm-agent-java://reference/setup-attach-api.md) for more information on this setup method.

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-net-panel" aria-labelledby="apm-apm-get-started-net-button" hidden="">
        **Set up the {{apm-agent}}**

        * **Profiler runtime instrumentation**: The agent supports auto instrumentation without any code change and without any recompilation of your projects. See [Profiler auto instrumentation](apm-agent-dotnet://reference/setup-auto-instrumentation.md).
        * **NuGet packages**: The agent ships as a set of [NuGet packages](apm-agent-dotnet://reference/nuget-packages.md) available on [nuget.org](https://nuget.org). You can add the Agent and specific instrumentations to a .NET application by referencing one or more of these packages and following the package documentation.
        * **Host startup hook**: On .NET Core 3.0+ or .NET 5+, the agent supports auto instrumentation without any code change and without any recompilation of your projects. See [Zero code change setup on .NET Core](apm-agent-dotnet://reference/setup-dotnet-net-core.md) for more details.

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](apm-agent-dotnet://reference/supported-technologies.md)
        * [Advanced configuration](apm-agent-dotnet://reference/configuration.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-nodejs-panel" aria-labelledby="apm-apm-get-started-nodejs-button" hidden="">
        **1. Install the {{apm-agent}}**

        Install the {{apm-agent}} for Node.js as a dependency to your application.

        ```js
        npm install elastic-apm-node --save
        ```

        **2. Initialization**

        It’s important that the agent is started before you require *any* other modules in your Node.js application - i.e. before `http` and before your router etc.

        This means that you should probably require and start the agent in your application’s main file (usually `index.js`, `server.js` or `app.js`).

        Here’s a simple example of how Elastic APM is normally required and started:

        ```js
        // Add this to the VERY top of the first file loaded in your app
        var apm = require('elastic-apm-node').start({
          // Override service name from package.json
          // Allowed characters: a-z, A-Z, 0-9, -, _, and space
          serviceName: '',

          // API keys are used to authorize requests to the APM integration
          apiKey: '',

          // Set custom APM integration host and port (default: http://127.0.0.1:8200)
          serverUrl: '',
        })
        ```

        The agent will now monitor the performance of your application and record any uncaught exceptions.

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](asciidocalypse://docs/apm-agent-nodejs/docs/reference/supported-technologies.md)
        * [Babel/ES Modules](asciidocalypse://docs/apm-agent-nodejs/docs/reference/advanced-setup.md)
        * [Advanced configuration](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuring-agent.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-php-panel" aria-labelledby="apm-apm-get-started-php-button" hidden="">
        **1. Install the agent**

        Install the PHP agent using one of the [published packages](https://github.com/elastic/apm-agent-php/releases/latest).

        To use the RPM Package (RHEL/CentOS and Fedora):

        ```php
        rpm -ivh <package-file>.rpm
        ```

        To use the DEB package (Debian and Ubuntu):

        ```php
        dpkg -i <package-file>.deb
        ```

        To use the APK package (Alpine):

        ```php
        apk add --allow-untrusted <package-file>.apk
        ```

        If you can’t find your distribution, you can install the agent by building it from the source. The following instructions will build the APM agent using the same docker environment that Elastic uses to build our official packages.

        ::::{note}
        The agent is currently only available for Linux operating system.

        ::::


        1. Download the [agent source](https://github.com/elastic/apm-agent-php/).
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

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](asciidocalypse://docs/apm-agent-php/docs/reference/supported-technologies.md)
        * [Configuration](apm-agent-python://reference/configuration.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-python-panel" aria-labelledby="apm-apm-get-started-python-button" hidden="">
        Django and Flask are two of several frameworks that the Elastic APM Python Agent supports. For a complete list of supported technologies, refer to the [Elastic APM Python Agent documentation](apm-agent-python://reference/supported-technologies.md).

        *Django*

        ```python
        $ pip install elastic-apm
        ```

        **1. Install the {{apm-agent}}**

        Install the {{apm-agent}} for Python as a dependency.

        ```python
        $ pip install elastic-apm
        ```

        **2. Configure the {{apm-agent}}**

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

          # API keys are used to authorize requests to the APM integration
          'API_KEY': '',

          # Set custom APM integration host and port (default: http://localhost:8200)
          'SERVER_URL': '',
        }

        # To send performance metrics, add our tracing middleware:
        MIDDLEWARE = (
          'elasticapm.contrib.django.middleware.TracingMiddleware',
          #...
        )
        ```

        *Flask*

        **1. Install the {{apm-agent}}**

        Install the {{apm-agent}} for Python as a dependency.

        ```python
        $ pip install elastic-apm[flask]
        ```

        **2. Configure the {{apm-agent}}**

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

          # API keys are used to authorize requests to the APM integration
          'API_KEY': '',

          # Set custom APM integration host and port (default: http://localhost:8200)
          'SERVER_URL': '',
        }

        apm = ElasticAPM(app)
        ```

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](apm-agent-python://reference/supported-technologies.md)
        * [Advanced configuration](apm-agent-python://reference/configuration.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-ruby-panel" aria-labelledby="apm-apm-get-started-ruby-button" hidden="">
        **1. Install the {{apm-agent}}**

        Add the agent to your Gemfile.

        ```ruby
        gem 'elastic-apm'
        ```

        **2. Configure the agent**

        *Ruby on Rails*

        APM is automatically started when your app boots. Configure the agent by creating the config file `config/elastic_apm.yml`:

        ```ruby
        # config/elastic_apm.yml:

        # Set service name - allowed characters: a-z, A-Z, 0-9, -, _ and space
        # Defaults to the name of your Rails app
        service_name: 'my-service'

        # API keys are used to authorize requests to the APM integration
        api_key: ''

        # Set custom APM integration host and port (default: http://localhost:8200)
        server_url: 'http://localhost:8200'
        ```

        *Rack*

        For Rack or a compatible framework, like Sinatra, include the middleware in your app and start the agent.

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

        Create a config file `config/elastic_apm.yml`:

        ```ruby
        # config/elastic_apm.yml:

        # Set service name - allowed characters: a-z, A-Z, 0-9, -, _ and space
        # Defaults to the name of your Rack app's class.
        service_name: 'my-service'

        # API keys are used to authorize requests to the APM integration
        api_key: ''

        # Set custom APM integration host and port (default: http://localhost:8200)
        server_url: 'http://localhost:8200'
        ```

        **Learn more in the {{apm-agent}} reference**

        * [Supported technologies](asciidocalypse://docs/apm-agent-ruby/docs/reference/supported-technologies.md)
        * [Advanced configuration](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md)

          </div>
          <div tabindex="0" role="tabpanel" id="apm-apm-get-started-opentelemetry-panel" aria-labelledby="apm-apm-get-started-opentelemetry-button" hidden="">
        Elastic integrates with OpenTelemetry, allowing you to reuse your existing instrumentation to easily send observability data to Elastic.

        For more information on how to combine Elastic and OpenTelemetry, refer to [OpenTelemetry](../../../solutions/observability/apps/use-opentelemetry-with-apm.md).

          </div>
        </div>
        While there are many configuration options, all APM agents require:

        * **Service name**: The APM integration maps an instrumented service’s name — defined in each {{apm-agent}}'s configuration — to the index where its data is stored. Service names are case-insensitive and must be unique.

            For example, you cannot have a service named `Foo` and another named `foo`. Special characters will be removed from service names and replaced with underscores (`_`).

        * **Server URL**: The host and port that the managed intake service listens for events on.

            To find the URL for your project:

            1. Go to the [Cloud console](https://cloud.elastic.co/).
            2. Next to your project, select **Manage**.
            3. Next to *Endpoints*, select **View**.
            4. Copy the *APM endpoint*.

        * **API key**: Authentication method for communication between {{apm-agent}} and the managed intake service.

            You can create and delete API keys in Applications Settings:

            1. Go to any page in the *Applications* section of the main menu.
            2. Click **Settings** in the top bar.
            3. Go to the **Agent keys** tab.

        * **Environment**: The name of the environment this service is deployed in, for example "production" or "staging".

            Environments allow you to easily filter data on a global level in the UI. It’s important to be consistent when naming environments across agents.

3. If you’re using the step-by-step instructions in the UI, after you’ve installed and configured an agent, you can click **Check Agent Status** to verify that the agent is sending data.

To learn more about APM agents, including how to fine-tune how agents send traces to Elastic, refer to [Collect application data](../../../solutions/observability/apps/collect-application-data.md).


## Step 2: View your data [view-apm-integration-data]

After one or more APM agents are installed and successfully sending data, you can view application performance monitoring data in the UI.

In the *Applications* section of the main menu, select **Service Inventory**. This will show a high-level overview of the health and general performance of all your services.

Learn more about visualizing APM data in [View and analyze data](../../../solutions/observability/apps/view-analyze-data.md).

::::{tip}
Not seeing any data? Find helpful tips in [Troubleshooting](../../../troubleshoot/observability/apm/common-problems.md).

::::



## Next steps [observability-apm-get-started-next-steps]

Now that data is streaming into your project, take your investigation to a deeper level. Learn how to use [Elastic’s built-in visualizations for APM data](../../../solutions/observability/apps/view-analyze-data.md), [alert on APM data](../../../solutions/observability/incident-management/alerting.md), or [fine-tune how agents send traces to Elastic](../../../solutions/observability/apps/collect-application-data.md).
