---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-settings.html
description: Configure Maps display settings for auto-fit bounds, browser location, initial view, and tooltip behavior. Customize map interaction and default appearance.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Configure map settings [maps-settings]

Map settings control display behavior, initial view positioning, tooltip preferences, and custom icon management. These settings determine how maps appear when opened and how users interact with layers and features.

This reference covers all available map configuration options, including background colors, zoom behavior, browser location access, and custom icon management.


## Custom icons [maps-settings-custom-icons]

Add, edit, or delete custom icons for the map. Icons added to the map can be used for [styling Point features](maps-vector-style-properties.md#point-style-properties).


## Display [maps-settings-display]

**Background color**
:   Set the map background color.

**Show scale**
:   When enabled, display the map scale.


## Navigation [maps-settings-navigation]

**Auto fit map to bounds**
:   When enabled, the map will automatically pan and zoom to show the filtered data bounds.

**Zoom range**
:   Constrain the map to the defined zoom range.

**Initial map location**
:   Configure the initial map center and zoom.

    * **Map location at save**: Use the map center and zoom from the map position at the time of the latest save.
    * **Auto fit map to bounds**: Set the initial map location to show the filtered data bounds.
    * **Fixed location**: Lock the map center and zoom to fixed values.
    * **Browser location**: Set the initial map center to the browser location.



## Spatial filters [maps-settings-spatial-filters]

Use spatial filter settings to configure how [spatial filters](maps-create-filter-from-map.md#maps-spatial-filters) are displayed.

:::{image} /explore-analyze/images/kibana-spatial_filters.png
:alt: spatial filters
:::

**Show spatial filters on map**
:   Clear the checkbox so [spatial filters](maps-create-filter-from-map.md#maps-spatial-filters) do not appear on the map.

**Opacity**
:   Set the opacity of spatial filters.

**Fill color**
:   Set the fill color of spatial filters.

**Border color**
:   Set the border color of spatial filters.

