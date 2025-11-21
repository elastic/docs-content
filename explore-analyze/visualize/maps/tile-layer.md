---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/tile-layer.html
description: Add tile layers to Maps for base map backgrounds and overlays. Configure Elastic Maps Service, custom tile servers, and Web Map Services.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Tile layer [tile-layer]

Tile layers provide base map imagery and overlays from tile servers. You can add street maps, satellite imagery, topographic maps, or custom styled base maps from various tile services including {{ems}}, standard tile servers, vector tile services, and Web Map Services.

Tile layers typically serve as the background for your map, providing geographic context for the data layers displayed above them.

:::{image} /explore-analyze/images/kibana-tile_layer.png
:alt: tile layer
:screenshot:
:::

To add a tile layer to your map, click **Add layer**, then select one of the following:

**Configured Tile Map Service**
:   Tile map service configured in kibana.yml. See map.tilemap.url in [*Configure {{product.kibana}}*](kibana://reference/configuration-reference/general-settings.md) for details.

**EMS Basemaps**
:   Tile map service from [Elastic Maps Service](https://www.elastic.co/elastic-maps-service).

**Tile Map Service**
:   Tile map service configured in interface.

**Vector tiles**
:   Data service implementing the Mapbox vector tile specification.

**Web Map Service**
:   Maps from OGC Standard WMS.

