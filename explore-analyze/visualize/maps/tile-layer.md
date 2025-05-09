---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/tile-layer.html
---

# Tile layer [tile-layer]

Tile layers display image tiles served from a tile server.

:::{image} /explore-analyze/images/kibana-tile_layer.png
:alt: tile layer
:screenshot:
:::

To add a tile layer to your map, click **Add layer**, then select one of the following:

**Configured Tile Map Service**
:   Tile map service configured in kibana.yml. See map.tilemap.url in [*Configure {{kib}}*](kibana://reference/configuration-reference/general-settings.md) for details.

**EMS Basemaps**
:   Tile map service from [Elastic Maps Service](https://www.elastic.co/elastic-maps-service).

**Tile Map Service**
:   Tile map service configured in interface.

**Vector tiles**
:   Data service implementing the Mapbox vector tile specification.

**Web Map Service**
:   Maps from OGC Standard WMS.

