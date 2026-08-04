---
description: Reference for the field formatters available for string, date, geographic point, and numeric fields in a Kibana data view.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Format data view fields [managing-fields]

{{kib}} uses the same field types as {{es}}, however, some {{es}} field types are unsupported in {{kib}}. To customize how {{kib}} displays data view fields, use the formatting options.

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the field you want to change.
3. Find the field, then open the edit options (![Data field edit icon](/explore-analyze/images/kibana-edit_icon.png "")).
4. Select **Set custom label**, then enter a **Custom label** for the field.
5. Select **Set format**, then enter the **Format** for the field.

::::{note}
For numeric fields, the default field formatters are based on the `meta.unit` field. The unit is associated with a [time unit](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units), percent, or byte. The convention for percents is to use value 1 to mean 100%.
::::

## String field formatters [string-field-formatters]

String fields support **String** and **Url** formatters.

The **String** field formatter enables you to apply transforms to the field.

Supported transformations include:

* Convert to lowercase
* Convert to uppercase
* Convert to title case
* Apply the short dots transformation, which replaces the content before the `.` character with the first character of the content. For example:

**Original**
:   **Becomes**

`com.organizations.project.ClassName`
:   `c.o.p.ClassName`

    * Base64 decode
    * URL param decode

You can specify the following types to the `Url` field formatter:

* **Link** — Converts the contents of the field into an URL. You can specify the width and height of the image, while keeping the aspect ratio. When the image is smaller than the specified parameters, the image is unable to upscale.
* **Image** — Specifies the image directory.
* **Audio** — Specify the audio directory.

To customize URL field formats, use templates. An **URL template** enables you to add values to a partial URL. To add the contents of the field to a fixed URL, use the `{{value}}` string.

For example, when:

* A field contains a user ID
* A field uses the `Url` field formatter
* The URI template is `http://company.net/profiles?user_id={­{{value}}­}`

The resulting URL replaces `{{value}}` with the user ID from the field.

The `{{value}}` template string URL-encodes the contents of the field. When a field encoded into a URL contains non-ASCII characters, the characters are replaced with a `%` character and the appropriate hexadecimal code. For example, field contents `users/admin` result in the URL template adding `users%2Fadmin`.

When the formatter type is **Image**, the `{{value}}` template string specifies the name of an image at the specified URI.

You can render base64 images from data within a document by using the following **URL template**:

```text
data:image/png;base64,{{value}}
```

For example:
![Data view editing to load base64 encoded PNG data](/explore-analyze/images/kibana-data_view_format_url_image_base64.png "")

This configuration renders a PNG file in Discover as follows:
![Sample output of PNG loading in Discover](/explore-analyze/images/kibana-discover-render_base64_image.png "")

When the formatter type is **Audio**, the `{{value}}` template string specifies the name of an audio file at the specified URI.

To pass unescaped values directly to the URL, use the `{{rawValue}}` string.

A **Label template** enables you to specify a text string that appears instead of the raw URL. You can use the `{{value}}` template string normally in label templates. You can also use the `{{url}}` template string to display the formatted URL.

## Date field formatters [field-formatters-date]

Date fields support **Date**, **String**, and **Url** formatters.

The **Date** formatter enables you to choose the display format of date stamps using the [moment.js](https://momentjs.com/) standard format definitions.

The **String** field formatter enables you to apply transforms to the field.

Supported transformations include:

* Convert to lowercase
* Convert to uppercase
* Convert to title case
* Apply the short dots transformation, which replaces the content before the `.` character with the first character of the content. For example:

**Original**
:   **Becomes**

`com.organizations.project.ClassName`
:   `c.o.p.ClassName`

    * Base64 decode
    * URL param decode

You can specify the following types to the `Url` field formatter:

* **Link** — Converts the contents of the field into an URL. You can specify the width and height of the image, while keeping the aspect ratio. When the image is smaller than the specified parameters, the image is unable to upscale.
* **Image** — Specifies the image directory.
* **Audio** — Specify the audio directory.

To customize URL field formats, use templates. An **URL template** enables you to add values to a partial URL. To add the contents of the field to a fixed URL, use the `{{value}}` string.

For example, when:

* A field contains a user ID
* A field uses the `Url` field formatter
* The URI template is `http://company.net/profiles?user_id={­{{value}}­}`

The resulting URL replaces `{{value}}` with the user ID from the field.

The `{{value}}` template string URL-encodes the contents of the field. When a field encoded into a URL contains non-ASCII characters, the characters are replaced with a `%` character and the appropriate hexadecimal code. For example, field contents `users/admin` result in the URL template adding `users%2Fadmin`.

When the formatter type is **Image**, the `{{value}}` template string specifies the name of an image at the specified URI.

When the formatter type is **Audio**, the `{{value}}` template string specifies the name of an audio file at the specified URI.

To pass unescaped values directly to the URL, use the `{{rawValue}}` string.

A **Label template** enables you to specify a text string that appears instead of the raw URL. You can use the `{{value}}` template string normally in label templates. You can also use the `{{url}}` template string to display the formatted URL.

## Geographic point field formatters [field-formatters-geopoint]

Geographic point fields support the **String** formatter.

The **String** field formatter enables you to apply transforms to the field.

Supported transformations include:

* Convert to lowercase
* Convert to uppercase
* Convert to title case
* Apply the short dots transformation, which replaces the content before the `.` character with the first character of the content. For example:

**Original**
:   **Becomes**

`com.organizations.project.ClassName`
:   `c.o.p.ClassName`

    * Base64 decode
    * URL param decode

## Number field formatters [field-formatters-numeric]

Numeric fields support **Bytes and Bits**, **Color**, **Duration**, **Histogram**, **Number**, **Percentage**, **String**, and **Url** formatters.

The **Bytes and Bits**, **Number**, and **Percentage** formatters enable you to choose the display formats of numbers in the field using the [Elastic numeral pattern](/explore-analyze/numeral-formatting.md) syntax that {{kib}} maintains.

The **Histogram** formatter is used only for the [histogram field type](elasticsearch://reference/elasticsearch/mapping-reference/histogram.md). When you use the **Histogram** formatter, you can apply the **Bytes and Bits**, **Number**, or **Percentage** format to aggregated data.

You can specify the following types to the `Url` field formatter:

* **Link** — Converts the contents of the field into an URL. You can specify the width and height of the image, while keeping the aspect ratio. When the image is smaller than the specified parameters, the image is unable to upscale.
* **Image** — Specifies the image directory.
* **Audio** — Specify the audio directory.

To customize URL field formats, use templates. An **URL template** enables you to add values to a partial URL. To add the contents of the field to a fixed URL, use the `{{value}}` string.

For example, when:

* A field contains a user ID
* A field uses the `Url` field formatter
* The URI template is `http://company.net/profiles?user_id={­{{value}}­}`

The resulting URL replaces `{{value}}` with the user ID from the field.

The `{{value}}` template string URL-encodes the contents of the field. When a field encoded into a URL contains non-ASCII characters, the characters are replaced with a `%` character and the appropriate hexadecimal code. For example, field contents `users/admin` result in the URL template adding `users%2Fadmin`.

When the formatter type is **Image**, the `{{value}}` template string specifies the name of an image at the specified URI.

When the formatter type is **Audio**, the `{{value}}` template string specifies the name of an audio file at the specified URI.

To pass unescaped values directly to the URL, use the `{{rawValue}}` string.

A **Label template** enables you to specify a text string that appears instead of the raw URL. You can use the `{{value}}` template string normally in label templates. You can also use the `{{url}}` template string to display the formatted URL.

The **String** field formatter enables you to apply transforms to the field.

Supported transformations include:

* Convert to lowercase
* Convert to uppercase
* Convert to title case
* Apply the short dots transformation, which replaces the content before the `.` character with the first character of the content. For example:

**Original**
:   **Becomes**

`com.organizations.project.ClassName`
:   `c.o.p.ClassName`

    * Base64 decode
    * URL param decode

The **Duration** field formatter displays the numeric value of a field in the following increments:

* Picoseconds
* Nanoseconds
* Microseconds
* Milliseconds
* Seconds
* Minutes
* Hours
* Days
* Weeks
* Months
* Years

You can specify these increments with up to 20 decimal places for input and output formats.

The **Color** field formatter enables you to specify colors with ranges of values for a number field.

When you select the **Color** formatter, select **Add Color**, then specify the **Range**, **Text color**, and **Background color**.

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
