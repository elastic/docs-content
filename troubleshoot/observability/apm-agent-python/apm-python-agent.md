---
navigation_title: "APM Python Agent"
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/python/current/troubleshooting.html
---

# Troubleshoot APM Python Agent [troubleshooting]

Below are some resources and tips for troubleshooting and debugging the python agent.

* [Easy Fixes](#easy-fixes)
* [Django `check` and `test`](#django-test)
* [Agent logging](#agent-logging)
* [Disable the Agent](#disable-agent)


## Easy Fixes [easy-fixes]

Before you try anything else, go through the following sections to ensure that the agent is configured correctly. This is not an exhaustive list, but rather a list of common problems that users run into.


### Debug Mode [debug-mode]

Most frameworks support a debug mode. Generally, this mode is intended for non-production environments and provides detailed error messages and logging of potentially sensitive data. Because of these security issues, the agent will not collect traces if the app is in debug mode by default.

You can override this behavior with the [`DEBUG`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-debug) configuration.

Note that configuration of the agent should occur before creation of any `ElasticAPM` objects:

```python
app = Flask(__name__)
app.config["ELASTIC_APM"] = {"DEBUG": True}
apm = ElasticAPM(app, service_name="flask-app")
```


### `psutil` for Metrics [psutil-metrics]

To get CPU and system metrics on non-Linux systems, `psutil` must be installed. The agent should automatically show a warning on start if it is not installed, but sometimes this warning can be suppressed. Install `psutil` and metrics should be collected by the agent and sent to the APM Server.

```bash
python3 -m pip install psutil
```


### Credential issues [apm-server-credentials]

In order for the agent to send data to the APM Server, it may need an [`API_KEY`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-api-key) or a [`SECRET_TOKEN`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-secret-token). Double check your APM Server settings and make sure that your credentials are configured correctly. Additionally, check that [`SERVER_URL`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-server-url) is correct.


## Django `check` and `test` [django-test]

When used with Django, the agent provides two management commands to help debug common issues. Head over to the [Django troubleshooting section](asciidocalypse://docs/apm-agent-python/docs/reference/django-support.md#django-troubleshooting) for more information.


## Agent logging [agent-logging]

To get the agent to log more data, all that is needed is a [Handler](https://docs.python.org/3/library/logging.html#handler-objects) which is attached either to the `elasticapm` logger or to the root logger.

Note that if you attach the handler to the root logger, you also need to explicitly set the log level of the `elasticapm` logger:

```python
import logging
apm_logger = logging.getLogger("elasticapm")
apm_logger.setLevel(logging.DEBUG)
```


### Django [django-agent-logging]

The simplest way to log more data from the agent is to add a console logging Handler to the `elasticapm` logger. Here’s a (very simplified) example:

```python
LOGGING = {
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'elasticapm': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    },
}
```


### Flask [flask-agent-logging]

Flask [recommends using `dictConfig()`](https://flask.palletsprojects.com/en/1.1.x/logging/) to set up logging. If you’re using this format, adding logging for the agent will be very similar to the [instructions for Django above](#django-agent-logging).

Otherwise, you can use the [generic instructions below](#generic-agent-logging).


### Generic instructions [generic-agent-logging]

Creating a console Handler and adding it to the `elasticapm` logger is easy:

```python
import logging

elastic_apm_logger = logging.getLogger("elasticapm")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
elastic_apm_logger.addHandler(console_handler)
```

You can also just add the console Handler to the root logger. This will apply that handler to all log messages from all modules.

```python
import logging

logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
```

See the [python logging docs](https://docs.python.org/3/library/logging.html) for more details about Handlers (and information on how to format your logs using Formatters).


## Disable the Agent [disable-agent]

In the unlikely event the agent causes disruptions to a production application, you can disable the agent while you troubleshoot.

If you have access to [dynamic configuration](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#dynamic-configuration), you can disable the recording of events by setting [`recording`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-recording) to `false`. When changed at runtime from a supported source, there’s no need to restart your application.

If that doesn’t work, or you don’t have access to dynamic configuration, you can disable the agent by setting [`enabled`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-enabled) to `false`. You’ll need to restart your application for the changes to take effect.

