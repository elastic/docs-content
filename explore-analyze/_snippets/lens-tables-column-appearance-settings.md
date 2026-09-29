- **Value format**: Choose to display the value as number, percent, bytes, bits, duration, or with a custom format that you can define.

- **Text alignment**: Align the values in the column to the **Left**, **Center**, or **Right**.
  - {applies_to}`stack: ga 9.6` {applies_to}`serverless: ga` **Center** isn't available when **Cell decoration** is set to **Progress bar**. If a column was set to **Center**, switching to **Progress bar** changes its alignment to **Right**.

- **Cell decoration** or **Color by value** (depending on your {{kib}} version): Apply a color or a progress bar to cells based on their values, and choose which cell element to decorate:
  - **None**: No decoration (default).
  - **Background** or **Cell** (depending on your {{kib}} version): Color cell backgrounds.
  - {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` **Badge**: Display cell values as colored badges. Empty, null, and not-a-number (`NaN`) values render as plain text instead.
  - **Text**: Color cell text.
  - {applies_to}`stack: ga 9.6` {applies_to}`serverless: ga` **Progress bar**: Display the value as an in-cell progress bar. Available for numeric metric columns only. Empty, null, and not-a-number (`NaN`) values render as plain text instead.
    - **Bar color**: **Single** applies one color that you pick. **Solid** and **Gradient** use the same color mapping as **Badge** and **Text**, and **Gradient** is selected by default.
    - **Value range**: **Auto** sizes the bar using the loaded values for the column. **Custom** lets you set your own minimum and maximum, including negative values.
    - Supports **Left** or **Right** text alignment only.

- **Color mapping**: Define the colors to apply to each cell of the column based on its value. Refer to [](/explore-analyze/visualize/lens.md#assign-colors-to-terms) for more details.

- **Hide column**: Hide this column from the table display while keeping it available for sorting or other operations.