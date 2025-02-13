---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/vector-tooltip.html
---

# Vector tooltips [vector-tooltip]

Vector tooltips display attributes for the features at your mouse location. These tooltips give users an in-depth insight into what’s going on in the map.

If more than one feature exists at a location, the tooltip displays the attributes for the top feature, and notes the number of features at that location. The following image has a tooltip with three features at the current location: a green circle from the **Total Sales Revenue** layer, a blue New York State polygon from **United States** layer, and a red United States Country polygon from the **World Countries** layer. The tooltip displays attributes for the top feature, the green circle, from the **Total Sales Revenue** layer.

:::{image} ../../../images/kibana-multifeature_tooltip.png
:alt: multifeature tooltip
:class: screenshot
:::


## Format tooltips [maps-vector-tooltip-formatting]

You can format the attributes in a tooltip by adding [field formatters](../../find-and-organize/data-views.md#managing-fields) to your data view. You can use field formatters to round numbers, provide units, and even display images in your tooltip.


## Lock a tooltip at the current location [maps-vector-tooltip-locking]

You can lock a tooltip in place by clicking a location on the map. With locked tooltips you can:

* Page through features.
* Create a [phrase filter](maps-create-filter-from-map.md#maps-phrase-filter) from a feature attribute value.
* Create a [spatial filter](maps-create-filter-from-map.md#maps-spatial-filters) from a feature’s geometry.

This image shows a locked tooltip with features from three layers. The tooltip displays attributes for the second feature, the blue New York State polygon.  The tooltip includes controls for paging through the features and a dropdown menu for filtering the features by layer.

:::{image} ../../../images/kibana-locked_tooltip.png
:alt: locked tooltip
:class: screenshot
:::

