---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-vector-style-properties.html
description: Customize vector layer appearance in Maps with fill colors, border styles, label formatting, and icon settings. Apply data-driven or static styling properties.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Vector style properties [maps-vector-style-properties]

Point, polygon, and line features support different styling properties.


## Point style properties [point-style-properties]

You can add text labels to your Point features by configuring label style properties.

|     |     |
| --- | --- |
| **Label** | Specifies label content. |
| **Label position** | Place label above, in the center of, or below the Point feature. |
| **Label visibility** | Specifies the zoom range for which labels are displayed. |
| **Label color** | The text color. |
| **Label size** | The size of the text, in pixels. |
| **Label border color** | The color of the label border. |
| **Label border width** | The width of the label border. |

You can symbolize Point features as **Circle markers** or **Icons**.

Use **Circle marker** to symbolize Points as circles.

|     |     |
| --- | --- |
| **Border color** | The border color of the point features. |
| **Border width** | The border width of the point features. |
| **Fill color** | The fill color of the point features. |
| **Symbol size** | The radius of the symbol size, in pixels. |

Use **Icon** to symbolize Points as icons.

|     |     |
| --- | --- |
| **Border color** | The border color of the point features. |
| **Border width** | The border width of the point features. |
| **Fill color** | The fill color of the point features. |
| **Symbol orientation** | The symbol orientation rotating the icon clockwise. |
| **Symbol size** | The radius of the symbol size, in pixels. |

### Available icons

:::{image} /explore-analyze/images/kibana-maki-icons.png
:alt: maki icons
:screenshot:
:::

### Custom Icons

You can also use your own SVG icon to style Point features in your map. In **Layer settings** open the **icon** dropdown, and click the **Add custom icon** button. For best results, your SVG icon should be monochrome and have limited details.

Dynamic styling in **Elastic Maps** requires rendering SVG icons as PNGs using a [signed distance function](https://en.wikipedia.org/wiki/Signed_distance_function). As a result, sharp corners and intricate details may not render correctly. Modifying the settings under **Advanced Options** in the **Add custom icon** modal may improve rendering.

Manage your custom icons in [settings](maps-settings.md).


## Polygon style properties [polygon-style-properties]

|     |     |
| --- | --- |
| **Border color** | The border color of the polygon features. |
| **Border width** | The border width of the polygon features. |
| **Fill color** | The fill color of the polygon features. |
| **Label** | Specifies label content. For polygons, the label is positioned at the polygon centroid. For multi-polygons, the label is positioned at the largest polygon centroid. |
| **Label visibility** | Specifies the zoom range for which labels are displayed. |
| **Label color** | The text color. |
| **Label size** | The size of the text, in pixels. |
| **Label border color** | The color of the label border. |
| **Label border width** | The width of the label border. |


## Line style properties [line-style-properties]

|     |     |
| --- | --- |
| **Border color** | The color of the line features. |
| **Border width** | The width of the line features. |
| **Label** | Specifies label content. For lines, the label is positioned at the center of the line. For multi-lines, the label is positioned at the center of the longest line. |
| **Label visibility** | Specifies the zoom range for which labels are displayed. |
| **Label color** | The text color. |
| **Label size** | The size of the text, in pixels. |
| **Label border color** | The color of the label border. |
| **Label border width** | The width of the label border. |
