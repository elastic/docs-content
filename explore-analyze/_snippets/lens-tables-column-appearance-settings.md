- **Value format**: Choose to display the value as number, percent, bytes, bits, duration, or with a custom format that you can define.

- **Text alignment**: Align the values in the column to the **Left**, **Center**, or **Right**.

- **Cell decoration** (or **Color by value** in versions before 9.6): Apply a visual decoration to cells based on their values, and choose which cell element to decorate:
  - **None**: No decoration (default).
  - **Background** (or **Cell** in versions before 9.6): Color cell backgrounds.
  - {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` **Badge**: Display cell values as colored badges. Empty, null, and not-a-number (`NaN`) values render as plain text instead.
  - **Text**: Color cell text.
  - {applies_to}`stack: ga 9.6` {applies_to}`serverless: ga` **Progress bar** (numeric metric columns only): Display an in-cell bar alongside the formatted value.
    - **Bar color**: Choose **Single** for one color across all bars, or **Solid**/**Gradient** to map colors to values using the color mapping palette.
    - **Value range**: Choose **Auto** to derive the bar scale from the loaded column values, or **Custom** to set specific minimum and maximum values.
    - When **Progress bar** is selected, **Text alignment** supports only **Left** and **Right**; **Center** alignment is unavailable.

- **Color mapping**: Define the colors to apply to each cell of the column based on its value. Refer to [](/explore-analyze/visualize/lens.md#assign-colors-to-terms) for more details.

- **Hide column**: Hide this column from the table display while keeping it available for sorting or other operations.