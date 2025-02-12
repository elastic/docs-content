---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-settings.html
---

# Configure map settings [maps-settings]

Maps offers settings that let you configure how a map is displayed. To access these settings, click **Settings** in the application toolbar.


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

:::{image} ../../../images/kibana-spatial_filters.png
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

