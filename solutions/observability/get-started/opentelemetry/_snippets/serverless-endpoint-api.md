Follow these steps to retrieve the {{motlp}} URL and the API key for your Serverless project:

1. In {{serverless-full}}, open your Observability project.
2. Go to **Add data** and select **OpenTelemetry** under **Applications**. If you can't find **Add data** in the navigation menu, search for **Observability Onboarding** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. In **Configure the OpenTelemetry SDK**, copy the `OTEL_EXPORTER_OTLP_ENDPOINT` value. This is your endpoint.
4. In the same step, find the `OTEL_EXPORTER_OTLP_HEADERS` value. It has the form `Authorization=ApiKey <key>`, where `<key>` is an API key that Elastic generated for you. Copy only the `<key>` part, without the `ApiKey` prefix. The {{agent}} configurations in these guides add the prefix for you.
