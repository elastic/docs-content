---
navigation_title: Writing about the UI
description: Guidelines for writing about the user interfaces of our Elastic products.
---

# Writing about the UI
 
This topic covers how to write about the UI, the best verbs and prepositions to use, what to call parts of the UI, and how to guide the user through tasks.

:::::{note}
These guidelines are different from the guidelines for writing UI text. If you're looking for that, refer to [EUI](https://elastic.github.io/eui/#/).
:::::

## General guidelines for writing about the UI

* Describe the prop value and tasks, and provide an example.
* Don't describe the UI piece-by-piece. Focus on use cases instead.
* Write steps for actions users can't figure out themselves.
* Keep the average number of steps between five and nine.
* Write with [active voice](./voice-tone.md). If you can add “by zombies” at the end, it's likely passive.
* Use **bold** for component names and match the capitalization as it appears in the UI.
* Use *x* (italicized) for variable text in UI component names, such as: "Click **Select all *x* rules**, and then select **Activate**."
* Test all procedures before you publish.

## Helpful, minimal, accurate

Keep these principles in mind when writing about the UI.

**Write about use cases.** Describe the purpose of the UI and its use case, and provide an example, if possible. If the UI text is doing its job, you shouldn't 
be writing, "this button does this, this tab shows that."

**Eliminate "duh" procedures.** Write documentation for complex interactions or when you want to convey content that doesn't fit on the screen. Don't write 
obvious steps, such as, "Click Save to save your document." Provide in-product assistance to minimize the number of step-by-step instructions and screen 
captures in the documentation. Both can quickly go out of date.

**Keep it focused.** Explain one way to accomplish the task and let users discover the alternative. Don't provide extraneous details.

**Test your docs as you go.** Push all the buttons and ensure that your content reflects real-world scenarios. Put yourself in your users' shoes, and 
test each step locally. Test your instructions for multiple use cases (and potentially on multiple versions if you plan to backport your changes).

## UI icons 

UI icons can be helpful to include when describing a procedure that requires the user to interact with the UI, for example, if they need to click a button or another UI element. Follow these guidelines:
- Use the approved list of [EUI icons](https://eui.elastic.co/docs/components/display/icons/). 
- Include the tooltip text, image, and alt-text for optimal accessibility. 
- Avoid using parentheses before and after the UI icon image, which can disrupt screen readers' speech and braille outputs. 
:::{dropdown} Example
    ❌ **Don't**: To display the table in fullscreen mode, click the fullscreen icon ({icon}`full_screen`).
    
    ✔️ **Do**: To display the table in fullscreen mode, click the fullscreen icon {icon}`full_screen`. 
:::
  
## Screenshots

Although screenshots can be worth a thousand words, they are also expensive to maintain, especially in an environment with rapid releases.

### When to use screenshots

Screenshots work best in:

- Timebound docs, such as highlights docs and blog posts
- Procedures for a complex UI
- Introductions

The following table can help you decide whether a screenshot is right for your doc.

| Ask yourself | Things to think about |
| ----------- | --------------------- |
| Is this part of the UI complicated enough that it would be difficult to explain with words? | If there are only a few simple actions, then it's not a good candidate for a screen capture.      |
| Am I capturing just what is pertinent to the task?   | You don't want to capture the whole screen, just the area in question and enough of the surrounding area to find it.        |
| Does this contain any confidential information, like user names or IP addresses? | If an IP address, email, or component ID is a part of the capture, it's always a good practice to anonymize it. If the information isn't important, you could blur it or Photoshop over the characters.
| When making animated GIFs, are they longer than 10-15 seconds? | For documentation, a shorter gif works best. Ensure that it's trimmed enough to show the visual and nothing else.

### Aspect ratio, resolution

When taking a screenshot:

- Use a tool like the [Window Resizer Chrome extension](https://chrome.google.com/webstore/detail/window-resizer/kkelicaakdanhinjdeammmilcgefonfh?hl=en)
to set the window's viewport.
  - Set the aspect ratio to 16:9 (1366x768px).
  - If the screenshots are hard to read, set the aspect ratio to 4:3
  (1024x768px) instead.
  - Use the same aspect ratio to capture all screenshots on the page.
- Set your zoom level to 100%.
- If you have made any color adjustments, reset to the default on your monitor or
  select Generic RGB.
- Avoid: drop shadows, jagged edges, and oversized images.
- Include only the essential UI components. The main menu, 
  breadcrumbs, header, toolbar, and search bar often change, so we generally
  exclude them. 
- Add a border around the screenshot to give it definition and ensure it's not "floating" against a white background. Refer to [Screenshots](https://docs-v3-preview.elastic.dev/elastic/docs-builder/tree/main/syntax/images#screenshots) for details about the `:screenshot:` attribute.
- If you need to draw attention to a specific part of the screenshot, you can draw a border or use an annotation, such as an arrow. If you do, keep these in mind:
  - Use Elastic's [brand colors](https://eui.elastic.co/#/theming/colors/values) for the annotation. We recommend the pink accent color, hex `#F04E98`.   
  - Ensure your annotations are no more than 3px in thickness. 

### Callouts on screenshots

If the screen is very complex, it might help to add callouts:

- Number them; do not use letters.
- Order numbers from left to right, top to bottom.
- Make sure that the callout number is readable in the documentation.
- Provide an explanation for each callout.

## Referring to apps and pages

In Kibana, there are multiple ways for users to navigate to apps and pages. Depending on the environment and initial setup, users can be served with different navigations where the structure, interactions, and visible features differ.

When referring to apps or pages in the docs, and especially in tasks and tutorials, it's important that you remain as close as possible to the user's truth. For that, use one of the following solution-agnostic patterns:

- The app is directly available in the main menu: `Find <APP> in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).`

- The app or page is accessible through only the global search field: `To open **APP or PAGE**, find **PARENT** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).`

You can adapt these patterns and the link to the search bar documentation to match your context and scenario. 

## Writing helpful procedures

You don't have to write a procedure for everything in the UI. Procedures are 
good for getting started tutorials and complex procedures. You don't need a 
procedure for tasks users can figure out themselves. Think minimalism.  

### Thinking through your procedure

Follow these guidelines when setting up your procedure.

* Think about prerequisites. If your procedure has prerequisites, mention them 
  before the procedure begins.
* Aim for five to nine steps. If that's not possible, find 
  logical groups of steps and make them substeps.
* Limit each step to one action.
* Give only the best way. Users can figure out the alternatives.

### Writing steps 

* State instructions in the correct sequence. Tell users where in the UI to perform the action, then tell them the 
  action to perform. This is especially important when you're guiding users 
  from one part of the UI to another, for example, when they change views. Once 
  users are working in the same place in the UI, this isn't as necessary.
:::{dropdown} Example
    On the home page, click **Sample data**.
:::
  
* Use arrows (→) to tell the user where to find a command.  
:::{dropdown} Example
    Go to **Management → Elasticsearch → Index lifecycle management**.
:::
    
* In general, don't call out the type of component you're talking about – 
  reference it by name. 
:::{dropdown} Example
    ❌ **Don't**: Click the **New button**.  
    ✔️ **Do**: Click **New**.
:::
  
* Bold the names of elements that you're directing the user to interact with.  
:::{dropdown} Example
    Click **Next step**.
:::
  
  * Use the same labels and capitalization that appear in the UI.
  If an element doesn't have a label or tooltip, use sentence case for the name 
  you give it.   
:::{dropdown} Example
    In **Configure settings**, click **Create index pattern**.
:::
    
* Align screenshots left or beneath the appropriate step.


## Choosing the right word

Looking for the right word? Here you'll find which words to use when writing 
about the UI. You can also refer to [Word choice](word-choice.md) and our [Accessibility guidelines](accessibility.md) for specific words and use cases. 

### Components

Use the language in this table when writing about UI components.

| Component  | Example |
|------------|---------|
| **Buttons** <br> A button is a UI element that is interactive by definition: when users click it, it responds to it by performing an action. <br> Use "click" and refer to a button by its label.    | ✔️ Do: Click **New**. <br> ❌ Don't: Click the "New" button.  |
| **Checkbox and radio button** <br> Checkbox is one word. <br> Use "select" and  "clear" over "check" and "uncheck". <br> Avoid naming the component unless it adds clarity (for example in a complex UI).  | ✔️ Do: Select all index checkboxes. <br> ✔️ Do: Select **Logs**. <br> ✔️ Do: Clear **Metrics**.  |
| **Icon buttons** <br> Include the icon inline to reinforce what the user is interacting with. For the name, use the tooltip text. If the icon doesn't have a name, give it one and make it sentence case.  | ✔️ Do: Click **Apply changes**. <br> ❌ Don't: Click the icon. |
| **Key** <br> Use "press" followed by key name, or "the _Key_ key" if it adds clarity. For a key combination, use "Modifier+Key".  | ✔️ Do: In the query bar, enter your search criteria and press Enter. <br> ✔️ Do: Press Command+Alt+L to expand and collapse the current scope.  |
| **Menus** <br> Use arrows (→) to tell the user where to find the command. <br> A menu always has action items.  | Select **Manage index → Add lifecycle policy**.  |
| **Text field** <br> Use "enter" for the action and code font for user input.   | ✔️ Do: In the **Name** field, enter a unique identifier for this rollup job. <br> ✔️ Do: In **Index pattern**, enter shakes*.   |
| **Toggle ([Switch in EUI](https://elastic.github.io/eui/#/forms/form-controls#switch))** <br> Refer to the UI element as a "toggle". <br> Name it only if it adds clarity for the reader. If the UI is clear enough, stay minimalist and focus on the action. <br> Use "toggle" as a noun rather than a verb. <br> Prefer using "turn on", "turn off" as a verb over "enable" or "disable".  | ✔️ Do: Turn on **Malware protection**. <br> ✔️ Do: Turn off the **Malware protection** toggle in the **Preferences** window. <br> ❌ Don't: Toggle **Malware protection** in the **Preferences** window.  |

### Menus 

* Don't use the verbs _open_ and/or _close_ when a user interacts with a menu. Use _From the menu,..._ instead.
* Refer to it as "menu." Don't call it a "dropdown menu" or "dropdown list."

### Icon vs. button

* If there is no text next to an actionable, visual symbol, it's an icon.
* If there is text next to an actionable visual symbol, it's a button.
* An actionable piece of text without a visual symbol is either a link or a 
  button.
* In the docs, refer to an icon with its symbol. 
:::{dropdown} Example
    From the action menu (...), select _Delete job_.
:::
  In this example, the (...) represents the action menu icon.

### Prepositions

#### At 

| Accompanying verb or noun  | Example  |
|---|---|
| command prompt  | at the command prompt  |

#### From

| Accompanying verb or noun  | Example  |
|---|---|
| command line  | from the command line  |
| list  | from the dropdown list  |

#### In

| Accompanying verb or noun  | Example  |
|---|---|
| cluster  | in the cluster (deployment)  |
| field  | in a field  |
| file  | in the file  |
| menu  | in the menu bar  |
| pane  | in the Metrics pane  |
| section  | in the section  |
| shard  | in a shard  |
| table  | in the table  |
| window | in the window |

#### On 

| Accompanying verb or noun  | Example  |
|---|---|
| install  | install on your hardware   |
| page  | on the Security page  |
| screen  | on the screen  |
| server  | on a web server  |
| tab  | on the APM tab  |
| toolbar  | on the toolbar  |

#### To/into

| Accompanying verb or noun  | Example  |
|---|---|
| deploy  | deploy the agent to the server  |
| ingest  | ingest data into Elasticsearch  |
| send  | send an alert to the contact  |