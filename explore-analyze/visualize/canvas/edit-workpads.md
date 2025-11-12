---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/edit-workpads.html
description: Customize Canvas workpads with variables, format settings, and element styling. Create reusable patterns and apply consistent formatting across workpad components.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Edit workpads [edit-workpads]

To create the look and feel that you want, apply format settings to the entire workpad, or individual elements.


## Create variables [create-variables]

When you frequently use copy and paste, create variables to easily reuse strings and patterns. For example, when you clone a large workpad and need to connect your elements to a new index, use variables to update each element instead of updating them manually.

1. Create the variables.

    1. Expand the **Variables** options.
    2. Click **Add a variable**.
    3. Specify the variable options, then click **Save changes**.

2. Apply the variable.

    1. Copy the variable.
    2. Select the element you want to change, then open the expression editor.
    3. Paste the variable.


For example, to change the {{data-source}} for a set of charts:

1. Specify the variable options.

   :::{image} /explore-analyze/images/kibana-specify_variable_syntax.png
   :alt: Variable syntax options
   :screenshot:
   :::

2. Copy the variable, then apply it to each element you want to update in the **Expression editor**.

   :::{image} /explore-analyze/images/kibana-copy_variable_syntax.png
   :alt: Copied variable syntax pasted in the Expression editor
   :screenshot:
   :::



## Apply changes to the entire workpad [apply-changes-to-the-entire-workpad]

With stylesheets, you can change the look of the entire workpad, including fonts, colors, layout, and more.

To get started, enter the changes you want to make in the **Global CSS overrides** text editor, then click **Apply stylesheet**.

For example, to change the background for the entire workpad, enter:

```text
.canvasPage {
background-color: #3990e6;
}
```


## Change the element settings [change-the-element-settings]

Element settings enable you to change the display options at the element level. For example, use the element settings to change the dimensions, style, or location of an element.


### Change the display options [change-the-display-options]

Choose the display options for your elements. The options available depend on the element you select.

To change the element display options, click **Display**, then make your changes in the editor.

To use CSS overrides:

1. Click **+** next to **Element style**, then select **CSS**.
2. In the **CSS** text editor, enter the changes you want to make, then click **Apply stylesheet**.

For example, to center an element, enter:

```text
.canvasRenderEl h1 {
text.align: center;
}
```


### Clone elements [clone-elements]

To use an element with the same functionality and appearance in multiple places, clone the element.

Select the element, then click **Edit > Clone**.


### Move and resize elements [move-and-resize-elements]

Canvas provides you with many options to move and resize the elements on your workpad.

* To move elements, click and hold the element, then drag to the new location.
* To move elements by 1 pixel, select the element, press and hold Shift, then use your arrow keys.
* To move elements by 10 pixels, select the element, then use your arrow keys.
* To resize elements, click and drag the resize handles to the new dimensions.


### Edit elements [edit-elements]

The element editing options allow you to arrange and organize the elements on your workpad page.

To align two or more elements:

1. Press and hold Shift, then select the elements you want to align.
2. Click **Edit > Alignment**, then select the alignment option.

To distribute three or more elements:

1. Press and hold Shift, then select the elements you want to distribute.
2. Click **Edit > Distribution**, then select the distribution option.

To reorder elements:

1. Select the element you want to reorder.
2. Click **Edit > Order**, then select the order option.


### Delete elements [delete-elements]

When you no longer need an element, delete it from your workpad.

1. Select the element you want to delete.
2. Click **Edit > Delete**.

