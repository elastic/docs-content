The following diagrams show the reference architecture for OpenTelemetry with Elastic, depending on your deployment model.

:::::{applies-switch}

::::{applies-item} serverless:

:::{image} /solutions/images/observability-apm-otel-distro-serverless.png
:alt: APM data ingest path (Serverless)
:::

::::

::::{applies-item} ess:

- {applies_to}`stack: preview 9.2`

   :::{image} /solutions/images/ech-preview-motlp.png
   :alt: APM data ingest path (ECH)
   :::

- {applies_to}`stack: ga 9.1`

   :::{image} /solutions/images/observability-apm-otel-distro-ech.png
   :alt: APM data ingest path (ECH)
   :::

::::

::::{applies-item} self:

:::{image} /solutions/images/observability-apm-otel-distro-self-managed.png
:alt: APM data ingest path (Self-managed)
:::

::::
:::::
